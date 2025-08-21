"""
Vercel Entry Point for AnalyticaCore AI
Simplified FastAPI handler for serverless deployment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

# Create FastAPI app
app = FastAPI(title="AnalyticaCore AI API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        "environment": os.getenv("ENVIRONMENT", "development"),
        "domain": os.getenv("DOMAIN", "localhost")
    }

# Vercel handler
def handler(request):
    """Vercel serverless handler"""
    return app

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
