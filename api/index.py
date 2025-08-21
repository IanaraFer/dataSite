"""
Vercel Entry Point for AnalyticaCore AI
Simplified FastAPI handler for serverless deployment
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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

# Export the app for Vercel
def handler(request):
    return app
