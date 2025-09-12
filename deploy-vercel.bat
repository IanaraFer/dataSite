@echo off
echo 🚀 Deploying to Vercel...
echo.

REM Check if Vercel CLI is installed
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Vercel CLI not found. Installing...
    npm install -g vercel
    if %errorlevel% neq 0 (
        echo ❌ Failed to install Vercel CLI
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
) else (
    echo.
    echo ❌ Vercel deployment failed
    echo Check the error messages above
)

echo.
pause
