"""
Vercel Entry Point for AnalyticaCore AI
Minimal FastAPI handler for serverless deployment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import os

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

class PaymentRequest(BaseModel):
    planName: str
    email: str
    amount: int

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AnalyticaCore AI API",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AnalyticaCore AI API is running"}

# Trial submission endpoint (simplified)
@app.post("/api/trial/submit")
async def submit_trial(submission: TrialSubmission):
    """Submit trial form (simplified for testing)"""
    try:
        # In production, this would save to database and send emails
        return {
            "success": True,
            "message": "Trial submission received",
            "submissionId": f"trial_{submission.email}_{int(__import__('time').time())}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Payment endpoint (simplified)
@app.post("/api/payment/subscribe")
async def create_subscription(payment: PaymentRequest):
    """Create subscription (simplified for testing)"""
    try:
        # In production, this would create Stripe subscription
        return {
            "success": True,
            "message": f"Subscription created for {payment.planName}",
            "subscriptionId": f"sub_{payment.email}_{int(__import__('time').time())}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Configuration endpoint
@app.get("/api/config")
async def get_config():
    """Get client configuration"""
    return {
        "environment": os.getenv("ENVIRONMENT", "production"),
        "api_version": "1.0.0"
    }

# This is the entry point for Vercel
# Vercel automatically detects FastAPI apps
