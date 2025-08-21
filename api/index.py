"""
Vercel Entry Point for AnalyticaCore AI
Simplified FastAPI handler for serverless deployment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uuid

# Create FastAPI app
app = FastAPI(title="AnalyticaCore AI API", version="1.0.0")

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
    """Handle free trial submissions"""
    try:
        # Process the trial submission
        response_data = {
            "success": True,
            "message": "Trial submission received successfully",
            "submissionId": f"trial_{submission.email.replace('@', '_').replace('.', '_')}",
            "data": {
                "firstName": submission.firstName,
                "company": submission.company,
                "email": submission.email,
                "hasDataset": bool(submission.datasetName)
            }
        }
        
        return JSONResponse(content=response_data, status_code=200)
        
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)}, 
            status_code=500
        )

@app.post("/api/payment/subscribe")
async def create_subscription(subscription: PaymentSubscription):
    """Handle subscription payments"""
    try:
        # Generate subscription ID
        subscription_id = f"sub_{uuid.uuid4().hex[:8]}"
        
        # For now, return a mock payment URL
        # In production, integrate with Stripe, Paddle, or preferred payment processor
        payment_data = {
            "success": True,
            "subscriptionId": subscription_id,
            "plan": subscription.plan,
            "amount": subscription.amount,
            "currency": subscription.currency,
            "message": f"Subscription created for {subscription.plan} plan",
            # Mock payment URL - replace with real payment processor
            "paymentUrl": f"https://checkout.stripe.com/pay/cs_test_{subscription_id}#{subscription.plan}"
        }
        
        return JSONResponse(content=payment_data, status_code=200)
        
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)}, 
            status_code=500
        )

# Export the app for Vercel
def handler(request):
    return app
