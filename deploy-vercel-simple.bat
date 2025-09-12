@echo off
echo 🚀 Deploying to Vercel (Alternative to Azure)
echo.

REM Check if Vercel CLI is installed
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing Vercel CLI...
    npm install -g vercel
    if %errorlevel% neq 0 (
        echo ❌ Failed to install Vercel CLI
        echo Please install Node.js first: https://nodejs.org
        pause
        exit /b 1
    )
)

echo ✅ Vercel CLI ready
echo.

REM Deploy to Vercel
echo 📤 Deploying to Vercel...
vercel --prod

if %errorlevel% equ 0 (
    echo.
    echo ✅ Vercel deployment successful!
    echo 🌐 Your site is now live on Vercel
    echo.
    echo 📊 Current Deployments:
    echo • Netlify: https://analyticacoreai.netlify.app
    echo • Vercel: [Your Vercel URL will be shown above]
    echo.
    echo 🎉 You now have TWO working deployments!
) else (
    echo.
    echo ❌ Vercel deployment failed
    echo But don't worry - Netlify is already working perfectly!
)

echo.
pause
