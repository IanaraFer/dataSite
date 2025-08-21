# DataSight AI - Trial Form Submission Flow

## Overview
This document explains where the trial form data goes and how you can access customer submissions.

## Current Setup

### 1. Form Location
- **Trial Form**: `http://localhost:8002/free-trial-simple.html`
- **Main Website**: `http://localhost:8002/index.html`

### 2. Backend Server
- **API Server**: Running on `http://localhost:8000`
- **Form Endpoint**: `POST http://localhost:8000/api/trial/submit`
- **Health Check**: `GET http://localhost:8000/api/health`

### 3. Form Submission Flow

```
Customer Fills Form → Frontend JavaScript → Backend API → Email Logs → Thank You Page
```

**Step-by-step:**
1. Customer fills out the trial form with their information
2. JavaScript submits data to backend API (`/api/trial/submit`)
3. Backend processes submission and creates customer ID
4. Background tasks log detailed notifications for your team
5. Customer is redirected to thank-you page with confirmation

### 4. Where Form Data Goes

#### A. Server Logs (Primary)
All form submissions are logged to the backend server console with detailed information:

**Location**: Check the terminal running `trial_server.py`

**Log Format**:
```
================================================================================
🔥 PRIORITY TRIAL SUBMISSION NOTIFICATION
================================================================================
Customer ID: TRIAL-20250821-1234
Submission Time: 2025-08-21T00:45:34.123456

CUSTOMER INFORMATION:
Name: Ianara Fernandes
Company: DataCorp
Email: ianara@datacorp.com
Phone: +353 874502058

BUSINESS DETAILS:
Industry: Technology
Annual Revenue: €1M - €5M
Main Challenge: Need better sales forecasting

DATASET UPLOADED: sales_data.csv (156KB)

ACTION REQUIRED:
🔥 HIGH PRIORITY - Call within 15 minutes: +353 874502058
📧 Send report to: ianara@datacorp.com

Contact: datasightai.founders@gmail.com
================================================================================
```

#### B. Fallback Email (If API Fails)
If the backend API is down, the form automatically falls back to opening your email client with the lead information.

**Recipient**: `datasightai.founders@gmail.com`

## How to Monitor Submissions

### Option 1: Real-time Monitoring (Recommended)
1. Keep the backend server terminal open while your website is live
2. Watch for new trial submissions in real-time
3. Each submission creates detailed logs with customer information

### Option 2: API Access
You can also check the API directly:
- **Health Check**: `GET http://localhost:8000/api/health`
- **Documentation**: `GET http://localhost:8000/docs` (FastAPI auto-docs)

### Option 3: Log Files (Future Enhancement)
Currently logs to console. Can be enhanced to write to files:
- Trial submissions log file
- Customer confirmation log file
- Error log file

## Customer Experience

### What Customers See:
1. **Form Submission**: Professional loading state with progress indication
2. **Success Message**: Confirmation with timeline for report delivery
3. **Thank You Page**: Detailed next steps and contact information
4. **Email Confirmation**: (Currently logged, can be automated)

### Timeline Promises:
- **With Dataset**: Report within 2 hours, call within 4 hours
- **Without Dataset**: Report within 24 hours, call within 24 hours

## Production Recommendations

### For Live Deployment:
1. **Email Integration**: Replace logging with actual email sending via:
   - Azure Communication Services
   - SendGrid
   - Mailgun

2. **Database Storage**: Store submissions in:
   - Azure SQL Database
   - PostgreSQL
   - MongoDB

3. **CRM Integration**: Connect to:
   - HubSpot
   - Salesforce
   - Pipedrive

4. **Monitoring**: Add:
   - Application Insights
   - Error tracking
   - Performance monitoring

## Server Commands

### To Start the System:
```powershell
# Terminal 1: Start Backend API
cd "C:\Users\35387\Desktop\dataSite\backend"
C:/Users/35387/Desktop/dataSite/Activate/Scripts/python.exe trial_server.py

# Terminal 2: Start Website
cd "C:\Users\35387\Desktop\dataSite\website"
python -m http.server 8002
```

### To Stop the System:
- Press `Ctrl+C` in both terminals

## Troubleshooting

### If Form Submissions Fail:
1. Check if backend server is running on port 8000
2. Check browser console for JavaScript errors
3. Form automatically falls back to email method

### If Backend Won't Start:
1. Ensure Python environment is activated
2. Check if required packages are installed:
   ```powershell
   pip install fastapi uvicorn python-multipart
   ```

### Common Issues:
- **CORS Errors**: Backend includes localhost:8002 in allowed origins
- **Port Conflicts**: Change ports in both servers if needed
- **Network Errors**: Check firewall settings

## Contact for Support
- **Email**: datasightai.founders@gmail.com
- **Phone**: +353 874502058

---
**Note**: This is the current development setup. For production, you'll need proper email integration and database storage.
