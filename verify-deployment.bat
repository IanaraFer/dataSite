@echo off
echo 🚀 AnalyticaCore AI - Vercel Deployment Ready!
echo ================================================

echo 📁 Checking project structure...

if exist "vercel.json" (
    echo ✅ vercel.json - Configuration file exists
) else (
    echo ❌ vercel.json - Missing!
)

if exist "requirements.txt" (
    echo ✅ requirements.txt - Python dependencies ready
) else (
    echo ❌ requirements.txt - Missing!
)

if exist "api\index.py" (
    echo ✅ api\index.py - Serverless function ready
) else (
    echo ❌ api\index.py - Missing!
)

if exist "public" (
    echo ✅ public\ - Static files directory exists
    echo    📄 Files in public\:
    dir public\*.html /b
) else (
    echo ❌ public\ - Missing static files directory!
)

echo.
echo 🎯 DEPLOYMENT COMMANDS:
echo 1. vercel login
echo 2. vercel --prod
echo 3. Configure environment variables in Vercel dashboard
echo 4. Add custom domain: analyticacoreai.ie
echo.
echo ✅ Your SaaS platform is ready for production deployment!

pause
