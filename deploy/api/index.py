"""
Vercel Entry Point for AnalyticaCore AI
Simplified FastAPI handler for serverless deployment with Stripe payments
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uuid
import os
import stripe
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json

# Create FastAPI app
app = FastAPI(title="AnalyticaCore AI API", version="1.0.0")

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_placeholder")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_placeholder")

# Initialize SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "contact@analyticacoreai.ie")
FROM_NAME = os.getenv("FROM_NAME", "AnalyticaCore AI")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TrialSubmission(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    company: str
    industry: str
    revenue: str
    challenge: Optional[str] = ""
    datasetName: Optional[str] = ""
    datasetSize: Optional[str] = ""

class PaymentSubscription(BaseModel):
    plan: str
    amount: float
    currency: str = "EUR"
    customer_email: Optional[str] = None
    customer_name: Optional[str] = None

class EmailNotification(BaseModel):
    to_email: str
    customer_name: str
    plan: Optional[str] = "trial"
    company: Optional[str] = ""

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AnalyticaCore AI API", "status": "running", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2025-08-21"}

@app.get("/api/status")
async def status():
    """Status endpoint"""
    return {
        "service": "AnalyticaCore AI",
        "status": "operational",
        "environment": "production"
    }

@app.post("/api/trial/submit")
async def submit_trial(submission: TrialSubmission):
    """Handle free trial submissions with email notifications"""
    try:
        # Process the trial submission
        submission_id = f"trial_{submission.email.replace('@', '_').replace('.', '_')}"
        
        response_data = {
            "success": True,
            "message": "Trial submission received successfully",
            "submissionId": submission_id,
            "data": {
                "firstName": submission.firstName,
                "company": submission.company,
                "email": submission.email,
                "hasDataset": bool(submission.datasetName)
            }
        }
        
        # Send confirmation email
        try:
            await send_trial_confirmation_email(submission)
        except Exception as email_error:
            print(f"Email sending failed: {email_error}")
            # Don't fail the entire request if email fails
        
        return JSONResponse(content=response_data, status_code=200)
        
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)}, 
            status_code=500
        )

@app.post("/api/payment/subscribe")
async def create_subscription(subscription: PaymentSubscription):
    """Handle subscription payments with Stripe"""
    try:
        # Create Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': subscription.currency.lower(),
                    'product_data': {
                        'name': f'AnalyticaCore AI - {subscription.plan.title()} Plan',
                        'description': f'Monthly subscription to {subscription.plan} plan'
                    },
                    'unit_amount': int(subscription.amount * 100),  # Stripe expects cents
                    'recurring': {
                        'interval': 'month'
                    }
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url='https://data-site-zucu.vercel.app/success.html?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://data-site-zucu.vercel.app/pricing.html',
            customer_email=subscription.customer_email,
            metadata={
                'plan': subscription.plan,
                'customer_name': subscription.customer_name or 'Unknown'
            }
        )
        
        return JSONResponse(content={
            "success": True,
            "checkout_url": checkout_session.url,
            "session_id": checkout_session.id,
            "plan": subscription.plan,
            "amount": subscription.amount
        }, status_code=200)
        
    except stripe.error.StripeError as e:
        return JSONResponse(
            content={"success": False, "error": f"Stripe error: {str(e)}"}, 
            status_code=400
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)}, 
            status_code=500
        )

@app.post("/api/stripe/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    try:
        payload = await request.body()
        sig_header = request.headers.get('stripe-signature')
        
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
        )
        
        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # Handle successful payment
            print(f"Payment successful for session: {session['id']}")
            
            # Send welcome email to customer
            try:
                customer_email = session.get('customer_email')
                if customer_email:
                    await send_welcome_email(customer_email, session.get('metadata', {}).get('plan', 'unknown'))
            except Exception as email_error:
                print(f"Welcome email failed: {email_error}")
        
        return JSONResponse(content={"received": True}, status_code=200)
        
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, 
            status_code=400
        )

async def send_trial_confirmation_email(submission: TrialSubmission):
    """Send trial confirmation email using SendGrid"""
    if not SENDGRID_API_KEY:
        print("SendGrid API key not configured")
        return
    
    try:
        sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
        
        message = Mail(
            from_email=(FROM_EMAIL, FROM_NAME),
            to_emails=submission.email,
            subject=f"🚀 Welcome to AnalyticaCore AI - Trial Activated!",
            html_content=f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #667eea;">Welcome to AnalyticaCore AI, {submission.firstName}! 🎉</h2>
                
                <p>Your free trial has been activated for <strong>{submission.company}</strong>.</p>
                
                <div style="background: #f8f9ff; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h3>📊 What's Next?</h3>
                    <ul>
                        <li>✅ Upload your business data securely</li>
                        <li>🤖 AI analysis begins automatically</li>
                        <li>📈 Receive insights within 24 hours</li>
                        <li>💬 Irish support team available</li>
                    </ul>
                </div>
                
                <p><strong>Industry:</strong> {submission.industry}<br>
                <strong>Revenue Range:</strong> {submission.revenue}</p>
                
                {f'<p><strong>Dataset:</strong> {submission.datasetName} uploaded for analysis!</p>' if submission.datasetName else ''}
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://data-site-zucu.vercel.app/platform.html" 
                       style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; padding: 15px 30px; text-decoration: none; 
                              border-radius: 25px; font-weight: bold;">
                        Access Your Dashboard
                    </a>
                </div>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                
                <p style="font-size: 14px; color: #666;">
                    Need help? Reply to this email or visit our support center.<br>
                    AnalyticaCore AI - Irish AI Solutions for Business Growth
                </p>
            </div>
            """
        )
        
        response = sg.send(message)
        print(f"Trial confirmation email sent to {submission.email}")
        
    except Exception as e:
        print(f"Failed to send trial confirmation email: {e}")
        raise

async def send_welcome_email(customer_email: str, plan: str):
    """Send welcome email for paid subscribers"""
    if not SENDGRID_API_KEY:
        return
    
    try:
        sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
        
        message = Mail(
            from_email=(FROM_EMAIL, FROM_NAME),
            to_emails=customer_email,
            subject=f"🎉 Welcome to AnalyticaCore AI {plan.title()} Plan!",
            html_content=f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #667eea;">Welcome to the {plan.title()} Plan! 🚀</h2>
                
                <p>Thank you for subscribing to AnalyticaCore AI!</p>
                
                <div style="background: #f8f9ff; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h3>🔓 Your Premium Features Are Now Active:</h3>
                    <ul>
                        <li>✅ Advanced AI analytics</li>
                        <li>📊 Custom dashboards</li>
                        <li>📈 Extended forecasting</li>
                        <li>🎯 Priority support</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://data-site-zucu.vercel.app/platform.html" 
                       style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; padding: 15px 30px; text-decoration: none; 
                              border-radius: 25px; font-weight: bold;">
                        Access Your Premium Dashboard
                    </a>
                </div>
                
                <p style="font-size: 14px; color: #666;">
                    Questions? We're here to help - reply to this email anytime!
                </p>
            </div>
            """
        )
        
        response = sg.send(message)
        print(f"Welcome email sent to {customer_email}")
        
    except Exception as e:
        print(f"Failed to send welcome email: {e}")

@app.get("/api/config")
async def get_config():
    """Get client configuration"""
    return {
        "stripe_publishable_key": STRIPE_PUBLISHABLE_KEY,
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# Export the app for Vercel
def handler(request):
    return app
