"""
Local Test Server for AnalyticaCore AI API
"""

import uvicorn
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

# Import the FastAPI app from api/index.py
from api.index import app

if __name__ == "__main__":
    print("🚀 Starting AnalyticaCore AI API Server...")
    print("📡 API will be available at: http://localhost:8002")
    print("📋 Health check: http://localhost:8002/api/health")
    print("💳 Payment endpoint: http://localhost:8002/api/payment/subscribe")
    print("📧 Trial endpoint: http://localhost:8002/api/trial/submit")
    
    uvicorn.run(
        "api.index:app", 
        host="0.0.0.0", 
        port=8002,
        reload=False,
        log_level="info"
    )
