"""
DataSight AI - Payment Processing Server
Handles Stripe subscriptions and customer billing
"""

import os
import json
import logging
import stripe
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# FastAPI app
app = FastAPI(title="DataSight AI Payment API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class CustomerData(BaseModel):
    email: EmailStr
    name: str
    company: Optional[str] = None
    plan: str
    price: int

class SubscriptionRequest(BaseModel):
    payment_method_id: str
    customer_data: CustomerData

class WebhookData(BaseModel):
    type: str
    data: Dict[Any, Any]

# Stripe price IDs for each plan (you'll need to create these in Stripe Dashboard)
PLAN_PRICES = {
    "starter": "price_starter_199_eur",      # Replace with actual Stripe price ID
    "professional": "price_professional_399_eur",  # Replace with actual Stripe price ID
    "enterprise": "price_enterprise_799_eur"       # Replace with actual Stripe price ID
}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "DataSight AI Payment API",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.post("/api/create-subscription")
async def create_subscription(
    request: SubscriptionRequest,
    background_tasks: BackgroundTasks
):
    """
    Create a new Stripe subscription for a customer
    """
    try:
        customer_data = request.customer_data
        payment_method_id = request.payment_method_id
        
        logger.info(f"Creating subscription for {customer_data.email} - {customer_data.plan} plan")
        
        # Create or retrieve Stripe customer
        try:
            # Check if customer already exists
            customers = stripe.Customer.list(email=customer_data.email, limit=1)
            if customers.data:
                customer = customers.data[0]
                logger.info(f"Existing customer found: {customer.id}")
            else:
                # Create new customer
                customer = stripe.Customer.create(
                    email=customer_data.email,
                    name=customer_data.name,
                    metadata={
                        "company": customer_data.company or "",
                        "plan": customer_data.plan,
                        "source": "datasight_ai_website"
                    }
                )
                logger.info(f"New customer created: {customer.id}")
        except Exception as e:
            logger.error(f"Error creating/retrieving customer: {str(e)}")
            raise HTTPException(status_code=400, detail="Failed to create customer")
        
        # Attach payment method to customer
        try:
            stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer.id,
            )
            
            # Set as default payment method
            stripe.Customer.modify(
                customer.id,
                invoice_settings={"default_payment_method": payment_method_id}
            )
        except Exception as e:
            logger.error(f"Error attaching payment method: {str(e)}")
            raise HTTPException(status_code=400, detail="Failed to attach payment method")
        
        # Get the price ID for the selected plan
        price_id = PLAN_PRICES.get(customer_data.plan)
        if not price_id:
            raise HTTPException(status_code=400, detail="Invalid plan selected")
        
        # Create subscription
        try:
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{"price": price_id}],
                payment_behavior="default_incomplete",
                payment_settings={"save_default_payment_method": "on_subscription"},
                expand=["latest_invoice.payment_intent"],
                metadata={
                    "plan": customer_data.plan,
                    "company": customer_data.company or "",
                    "signup_date": datetime.now().isoformat()
                }
            )
            
            logger.info(f"Subscription created: {subscription.id}")
            
        except Exception as e:
            logger.error(f"Error creating subscription: {str(e)}")
            raise HTTPException(status_code=400, detail="Failed to create subscription")
        
        # Generate customer ID for our system
        customer_id = f"CUST-{datetime.now().strftime('%Y%m%d')}-{abs(hash(customer_data.email)) % 10000:04d}"
        
        # Save customer data to our system
        customer_record = {
            "customer_id": customer_id,
            "stripe_customer_id": customer.id,
            "stripe_subscription_id": subscription.id,
            "email": customer_data.email,
            "name": customer_data.name,
            "company": customer_data.company,
            "plan": customer_data.plan,
            "price": customer_data.price,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "trial_end": (datetime.now() + timedelta(days=7)).isoformat(),  # 7-day trial
            "next_billing": subscription.current_period_end
        }
        
        # Save to customers directory
        customers_dir = "customers"
        os.makedirs(customers_dir, exist_ok=True)
        customer_file = os.path.join(customers_dir, f"{customer_id}.json")
        
        with open(customer_file, 'w') as f:
            json.dump(customer_record, f, indent=2)
        
        logger.info(f"Customer record saved: {customer_file}")
        
        # Add background tasks
        background_tasks.add_task(
            send_welcome_email,
            customer_data.email,
            customer_data.name,
            customer_data.plan,
            customer_id
        )
        
        background_tasks.add_task(
            create_customer_dashboard,
            customer_id,
            customer_data.plan
        )
        
        # Check if subscription requires additional authentication
        payment_intent = subscription.latest_invoice.payment_intent
        if payment_intent.status == "requires_action":
            return {
                "success": True,
                "requires_action": True,
                "payment_intent_client_secret": payment_intent.client_secret,
                "customer_id": customer_id,
                "subscription_id": subscription.id
            }
        
        # Subscription is successful
        return {
            "success": True,
            "customer_id": customer_id,
            "subscription_id": subscription.id,
            "status": subscription.status,
            "trial_end": customer_record["trial_end"],
            "message": f"Welcome to DataSight AI {customer_data.plan.title()} plan!"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_subscription: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/webhook")
async def stripe_webhook(request: Request):
    """
    Handle Stripe webhooks for subscription events
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    # Replace with your actual webhook secret
    webhook_secret = "whsec_YOUR_WEBHOOK_SECRET"
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        logger.error("Invalid payload in webhook")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid signature in webhook")
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    if event['type'] == 'invoice.payment_succeeded':
        # Payment succeeded
        invoice = event['data']['object']
        logger.info(f"Payment succeeded for invoice: {invoice['id']}")
        
        # Update customer record
        await handle_payment_success(invoice)
        
    elif event['type'] == 'invoice.payment_failed':
        # Payment failed
        invoice = event['data']['object']
        logger.info(f"Payment failed for invoice: {invoice['id']}")
        
        # Handle payment failure
        await handle_payment_failure(invoice)
        
    elif event['type'] == 'customer.subscription.deleted':
        # Subscription cancelled
        subscription = event['data']['object']
        logger.info(f"Subscription cancelled: {subscription['id']}")
        
        # Handle subscription cancellation
        await handle_subscription_cancellation(subscription)
    
    return {"success": True}

@app.get("/api/customer/{customer_id}")
async def get_customer(customer_id: str):
    """
    Get customer information
    """
    try:
        customer_file = f"customers/{customer_id}.json"
        
        if not os.path.exists(customer_file):
            raise HTTPException(status_code=404, detail="Customer not found")
        
        with open(customer_file, 'r') as f:
            customer_data = json.load(f)
        
        return customer_data
        
    except Exception as e:
        logger.error(f"Error retrieving customer {customer_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving customer")

async def send_welcome_email(email: str, name: str, plan: str, customer_id: str):
    """
    Send welcome email to new customer
    """
    logger.info(f"📧 Sending welcome email to {email} for {plan} plan")
    
    # In a real implementation, you would use an email service like SendGrid, Mailgun, etc.
    # For now, we'll just log the email content
    
    email_content = f"""
    Welcome to DataSight AI, {name}!
    
    Thank you for subscribing to our {plan.title()} plan.
    
    Your Customer ID: {customer_id}
    Plan: {plan.title()}
    
    Next Steps:
    1. Access your dashboard: http://localhost:8002/dashboard.html?customer_id={customer_id}
    2. Upload your first dataset for analysis
    3. Explore AI-powered insights
    
    Questions? Reply to this email or contact our support team.
    
    Best regards,
    The DataSight AI Team
    """
    
    logger.info(f"Email content prepared for {email}")
    # TODO: Integrate with actual email service

async def create_customer_dashboard(customer_id: str, plan: str):
    """
    Set up customer dashboard and resources
    """
    logger.info(f"🏗️ Setting up dashboard for customer {customer_id} - {plan} plan")
    
    dashboard_config = {
        "customer_id": customer_id,
        "plan": plan,
        "dashboard_url": f"http://localhost:8002/dashboard.html?customer_id={customer_id}",
        "features": get_plan_features(plan),
        "created_at": datetime.now().isoformat()
    }
    
    # Save dashboard configuration
    dashboards_dir = "dashboards"
    os.makedirs(dashboards_dir, exist_ok=True)
    
    dashboard_file = os.path.join(dashboards_dir, f"{customer_id}_dashboard.json")
    with open(dashboard_file, 'w') as f:
        json.dump(dashboard_config, f, indent=2)
    
    logger.info(f"Dashboard configured: {dashboard_file}")

def get_plan_features(plan: str) -> Dict[str, Any]:
    """
    Get features for a specific plan
    """
    features = {
        "starter": {
            "datasets_per_month": 5,
            "storage_days": 30,
            "support": "email",
            "forecasting": "basic",
            "reports": "pdf"
        },
        "professional": {
            "datasets_per_month": 20,
            "storage_days": 90,
            "support": "email_phone",
            "forecasting": "advanced",
            "reports": "interactive",
            "alerts": True,
            "collaboration": True
        },
        "enterprise": {
            "datasets_per_month": "unlimited",
            "storage_days": "unlimited",
            "support": "dedicated",
            "forecasting": "custom",
            "reports": "white_label",
            "alerts": True,
            "collaboration": True,
            "api_access": True,
            "custom_models": True
        }
    }
    
    return features.get(plan, {})

async def handle_payment_success(invoice):
    """Handle successful payment"""
    logger.info(f"Processing successful payment for invoice {invoice['id']}")
    # Update customer status, extend service, etc.

async def handle_payment_failure(invoice):
    """Handle failed payment"""
    logger.info(f"Processing failed payment for invoice {invoice['id']}")
    # Send notification, suspend service, etc.

async def handle_subscription_cancellation(subscription):
    """Handle subscription cancellation"""
    logger.info(f"Processing cancellation for subscription {subscription['id']}")
    # Update customer status, schedule data deletion, etc.

if __name__ == "__main__":
    print("🚀 Starting DataSight AI Payment Server...")
    print("💳 Stripe integration enabled")
    print("🔗 Payment endpoint: http://localhost:8001/api/create-subscription")
    print("📧 Webhook endpoint: http://localhost:8001/api/webhook")
    print("✨ Ready to process payments!")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
