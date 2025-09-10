import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- SMTP CONFIGURATION (Outlook) ---
SMTP_SERVER = "smtp.office365.com"  # Outlook/Office365 SMTP server
SMTP_PORT = 587  # TLS port for Outlook
SMTP_USERNAME = "information@analyticacoreai.ie"  # Your Outlook email address
SMTP_PASSWORD = "YOUR_EMAIL_PASSWORD"  # Set this securely, e.g., with environment variables
FROM_EMAIL = "information@analyticacoreai.ie"

def send_confirmation_email(to_email: str, customer_id: str):
    subject = "Your Analytica Core AI Trial Submission"
    body = f"""
    Hello,

    Thank you for trying Analytica Core AI! Your trial request (ID: {customer_id}) has been received.
    Our AI is processing your data and you will receive your insights soon.

    If you have any questions, reply to this email: information@analyticacoreai.ie

    Best regards,
    Analytica Core AI Team
    """
    msg = MIMEMultipart()
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())
    except Exception as e:
        import logging
        logging.error(f"Failed to send confirmation email: {e}")
"""
Simple FastAPI server for handling trial form submissions with file uploads
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
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

# Create FastAPI app
app = FastAPI(
    title="DataSight AI Trial Form Handler",
    description="Backend API for processing trial form submissions with file uploads",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "DataSight AI Trial Form Handler",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "DataSight AI Trial Form Handler",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/api/trial/submit-with-file"
        ]
    }

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
        logger.info(f"New trial submission from {email} at {company}")
        
        # Generate unique customer ID for tracking
        customer_id = f"TRIAL-{datetime.now().strftime('%Y%m%d')}-{abs(hash(email)) % 10000:04d}"
        
        # Handle file upload if present
        file_info = {}
        if businessData and businessData.filename:
            # Create uploads directory if it doesn't exist
            upload_dir = "uploads"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save the uploaded file
            safe_filename = f"{customer_id}_{businessData.filename}"
            file_path = os.path.join(upload_dir, safe_filename)
            
            content = await businessData.read()
            with open(file_path, "wb") as buffer:
                buffer.write(content)
            
            file_info = {
                "filename": businessData.filename,
                "size": len(content),
                "path": file_path,
                "content_type": businessData.content_type
            }
            
            logger.info(f"✅ File uploaded: {businessData.filename} ({len(content)} bytes)")
        
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
            "file_info": file_info
        }
        
        # Log the trial submission
        logger.info(f"🎯 Trial submission: {customer_id} - {company} ({industry})")
        if file_info:
            logger.info(f"📁 With file: {file_info['filename']} ({file_info['size']} bytes)")
        
        # Add background task for email notifications (mock for now)
        background_tasks.add_task(log_trial_processing, customer_id, submission_data)
        
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
            "file_received": bool(file_info),
            "file_info": file_info if file_info else None
        }
        
    except Exception as e:
        logger.error(f"❌ Error processing trial submission: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error processing trial submission. Please try again or contact support."
        )

async def log_trial_processing(customer_id: str, submission_data: dict):
    """
    Background task to log trial processing
    In production, this would send emails, process files, etc.
    """
    try:
        logger.info(f"🔄 Processing trial submission: {customer_id}")
        logger.info(f"👤 Customer: {submission_data['firstName']} {submission_data['lastName']}")
        logger.info(f"🏢 Company: {submission_data['company']} ({submission_data['industry']})")
        logger.info(f"📧 Email: {submission_data['email']}")

        if submission_data.get('file_info'):
            file_info = submission_data['file_info']
            logger.info(f"📊 Dataset: {file_info['filename']} - {file_info['size']} bytes")
            logger.info(f"💾 Saved to: {file_info['path']}")

        # Send confirmation email to customer
        send_confirmation_email(submission_data['email'], customer_id)

        # (Optional) Send notification to your team, process file, etc.
        
        logger.info(f"✅ Trial processing completed for {customer_id}")
        
    except Exception as e:
        logger.error(f"❌ Error in background processing: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting DataSight AI Trial Form Handler...")
    uvicorn.run(
        "trial_server:app",
        host="0.0.0.0", 
        port=8001,
        reload=False,
        log_level="info"
    )
