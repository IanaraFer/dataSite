"""
Simple FastAPI server for handling trial form submissions
Minimal dependencies - focused on form processing and email notifications
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
import logging
import uvicorn
import os
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="DataSight AI - Trial Form Handler",
    description="Simple form submission handler for trial requests",
    version="1.0.0"
)

# CORS configuration for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8002",
        "http://localhost:8009",
        "http://127.0.0.1:8002",
        "http://127.0.0.1:8009",
        "http://localhost:8001",
        "http://127.0.0.1:8001"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Pydantic models
class TrialSubmission(BaseModel):
    """Request model for free trial form submission"""
    firstName: str = Field(..., description="Customer first name")
    lastName: str = Field(..., description="Customer last name")
    email: str = Field(..., description="Business email address")
    phone: str = Field(..., description="Contact phone number")
    company: str = Field(..., description="Company name")
    industry: str = Field(..., description="Business industry")
    revenue: str = Field(..., description="Annual revenue range")
    challenge: str = Field(default="", description="Main business challenge")
    datasetName: str = Field(default="", description="Uploaded dataset filename")
    datasetSize: str = Field(default="", description="Dataset file size")

class TrialResponse(BaseModel):
    """Response model for trial submission"""
    success: bool
    message: str
    customer_id: str = None
    timestamp: str

# Endpoints
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "DataSight AI Trial Handler",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/trial/submit", response_model=TrialResponse)
async def submit_trial(
    submission: TrialSubmission,
    background_tasks: BackgroundTasks
):
    """
    Handle free trial form submissions
    Processes customer information and triggers notifications
    """
    try:
        logger.info(f"New trial submission from {submission.email} at {submission.company}")
        
        # Generate unique customer ID for tracking
        customer_id = f"TRIAL-{datetime.now().strftime('%Y%m%d')}-{hash(submission.email) % 10000:04d}"
        
        # Prepare data for processing
        trial_data = {
            "customer_id": customer_id,
            "submission_time": datetime.now().isoformat(),
            "customer_info": submission.dict(),
            "priority_level": "high" if submission.datasetName else "standard",
            "status": "processing"
        }
        
        # Log trial submission for business tracking
        logger.info(f"Trial submission: {customer_id} - {submission.company} ({submission.industry})")
        
        # Add background tasks for email processing
        background_tasks.add_task(
            log_trial_notification,
            trial_data
        )
        
        background_tasks.add_task(
            log_customer_confirmation,
            submission.email,
            submission.firstName,
            submission.company,
            bool(submission.datasetName)
        )
        
        response_message = (
            f"Trial request received successfully! "
            f"{'Priority processing initiated for your uploaded dataset. ' if submission.datasetName else ''}"
            f"You'll receive a comprehensive report within "
            f"{'2 hours' if submission.datasetName else '24 hours'}."
        )
        
        return TrialResponse(
            success=True,
            message=response_message,
            customer_id=customer_id,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error processing trial submission: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error processing trial submission. Please try again or contact support."
        )

@app.post("/api/trial/submit-with-file")
async def submit_trial_with_file(
    firstName: str = Form(...),
    lastName: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    company: str = Form(...),
    industry: str = Form(...),
    revenue: str = Form(...),
    challenge: str = Form(""),
    businessData: Optional[UploadFile] = File(None),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Handle trial submissions with file uploads
    Accepts multipart form data including files
    """
    try:
        logger.info(f"New trial submission with file from {email} at {company}")
        
        # Generate unique customer ID for tracking
        customer_id = f"TRIAL-{datetime.now().strftime('%Y%m%d')}-{hash(email) % 10000:04d}"
        
        # Handle file upload if present
        file_info = {}
        if businessData and businessData.filename:
            # Create uploads directory if it doesn't exist
            upload_dir = "uploads"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save the uploaded file
            file_path = os.path.join(upload_dir, f"{customer_id}_{businessData.filename}")
            
            with open(file_path, "wb") as buffer:
                content = await businessData.read()
                buffer.write(content)
            
            file_info = {
                "filename": businessData.filename,
                "size": len(content),
                "path": file_path,
                "content_type": businessData.content_type
            }
            
            logger.info(f"File uploaded: {businessData.filename} ({len(content)} bytes)")
        
        # Prepare submission data
        submission_data = {
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "phone": phone,
            "company": company,
            "industry": industry,
            "revenue": revenue,
            "challenge": challenge,
            "datasetName": file_info.get("filename", ""),
            "datasetSize": f"{file_info.get('size', 0) // 1024}KB" if file_info else ""
        }
        
        # Prepare data for processing
        trial_data = {
            "customer_id": customer_id,
            "submission_time": datetime.now().isoformat(),
            "customer_info": submission_data,
            "file_info": file_info,
            "priority_level": "high" if file_info else "standard",
            "status": "processing"
        }
        
        # Log trial submission for business tracking
        logger.info(f"Trial submission with file: {customer_id} - {company} ({industry})")
        
        # Add background tasks for processing
        background_tasks.add_task(
            log_trial_notification,
            trial_data
        )
        
        background_tasks.add_task(
            log_customer_confirmation,
            email,
            firstName,
            company,
            bool(file_info)
        )
        
        response_message = (
            f"Trial request received successfully! "
            f"{'Priority processing initiated for your uploaded dataset. ' if file_info else ''}"
            f"You'll receive a comprehensive report within "
            f"{'2 hours' if file_info else '24 hours'}."
        )
        
        return {
            "success": True,
            "message": response_message,
            "customer_id": customer_id,
            "timestamp": datetime.now().isoformat(),
            "file_received": bool(file_info)
        }
        
    except Exception as e:
        logger.error(f"Error processing trial submission with file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error processing trial submission. Please try again or contact support."
        )

# Background task functions
async def log_trial_notification(trial_data: dict):
    """
    Log trial notification for business team
    In production, this would send actual emails
    """
    try:
        logger.info(f"TRIAL NOTIFICATION: {trial_data['customer_id']}")
        
        customer_info = trial_data['customer_info']
        priority = "🔥 PRIORITY" if trial_data['priority_level'] == "high" else "📋 NEW"
        
        # Log detailed notification that can be monitored
        notification_details = f"""
================================================================================
{priority} TRIAL SUBMISSION NOTIFICATION
================================================================================
Customer ID: {trial_data['customer_id']}
Submission Time: {trial_data['submission_time']}

CUSTOMER INFORMATION:
Name: {customer_info['firstName']} {customer_info['lastName']}
Company: {customer_info['company']}
Email: {customer_info['email']}
Phone: {customer_info['phone']}

BUSINESS DETAILS:
Industry: {customer_info['industry']}
Annual Revenue: {customer_info['revenue']}
Main Challenge: {customer_info.get('challenge', 'Not specified')}

{'DATASET UPLOADED: ' + customer_info['datasetName'] + ' (' + customer_info['datasetSize'] + ')' if customer_info.get('datasetName') else 'No dataset uploaded'}

ACTION REQUIRED:
{'🔥 HIGH PRIORITY - Call within 15 minutes: ' + customer_info['phone'] if customer_info.get('datasetName') else '📞 Call within 24 hours: ' + customer_info['phone']}
📧 Send report to: {customer_info['email']}

Contact: datasightai.founders@gmail.com
================================================================================
        """
        
        logger.info(notification_details)
        
    except Exception as e:
        logger.error(f"Error logging trial notification: {str(e)}")

async def log_customer_confirmation(
    customer_email: str, 
    first_name: str, 
    company: str, 
    has_dataset: bool
):
    """
    Log customer confirmation details
    In production, this would send confirmation emails
    """
    try:
        logger.info(f"CUSTOMER CONFIRMATION: {customer_email}")
        
        confirmation_details = f"""
================================================================================
CUSTOMER CONFIRMATION EMAIL LOG
================================================================================
To: {customer_email}
Customer: {first_name}
Company: {company}
Has Dataset: {has_dataset}

Expected Timeline:
{('- Dataset Analysis: 10-15 minutes\\n- Custom Report: Within 2 hours\\n- Strategy Call: Within 4 hours' if has_dataset else '- AI Analysis: 5-10 minutes\\n- Email Delivery: Within 24 hours\\n- Optional Call: Next 24 hours')}

Report Includes:
✅ Revenue Forecast
✅ Customer Segments  
✅ Growth Opportunities
✅ Action Plan
✅ ROI Estimates
✅ Executive Summary

Contact Info:
📧 datasightai.founders@gmail.com
📞 +353 874502058
================================================================================
        """
        
        logger.info(confirmation_details)
        
    except Exception as e:
        logger.error(f"Error logging customer confirmation: {str(e)}")

# Server startup
if __name__ == "__main__":
    logger.info("Starting DataSight AI Trial Form Handler...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        reload=False,  # Disable reload to prevent shutdowns
        log_level="info"
    )
