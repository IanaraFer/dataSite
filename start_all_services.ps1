# Start All Analytica Core AI Services
# This script launches both the main platform and financial diagnosis API

Write-Host "🚀 Starting Analytica Core AI Platform..." -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Install dependencies if needed
Write-Host "📥 Checking dependencies..." -ForegroundColor Cyan
pip install -q -r requirements.txt

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Blue
Write-Host "  ANALYTICA CORE AI - ALL SERVICES STARTING" -ForegroundColor Blue
Write-Host "=" * 60 -ForegroundColor Blue
Write-Host ""

# Start Financial Diagnosis API in background
Write-Host "🔧 Starting Financial Diagnosis API (Port 5001)..." -ForegroundColor Magenta
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\.venv\Scripts\Activate.ps1; python financial_diagnosis_api.py"

Start-Sleep -Seconds 3

# Start Main Streamlit App
Write-Host "🎨 Starting Main Streamlit Platform (Port 8501)..." -ForegroundColor Magenta
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "  SERVICES RUNNING" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green
Write-Host ""
Write-Host "Main Platform:          http://localhost:8501" -ForegroundColor White
Write-Host "Financial Diagnosis:    http://localhost:8501/financial-diagnosis.html" -ForegroundColor White
Write-Host "Diagnosis API:          http://localhost:5001/api/diagnosis/health" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Yellow
Write-Host ""

streamlit run app.py
