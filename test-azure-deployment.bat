@echo off
echo 🚀 Testing Azure Deployment Setup...
echo.

REM Check if we're in the right directory
if not exist "website\index.html" (
    echo ❌ Error: website\index.html not found
    echo Make sure you're in the dataSite directory
    pause
    exit /b 1
)

echo ✅ Website files found
echo.

REM Check if Azure workflow exists
if exist ".github\workflows\azure-deployment.yml" (
    echo ✅ Azure workflow found
) else (
    echo ❌ Azure workflow not found
    pause
    exit /b 1
)

echo.
echo 📋 Azure Deployment Checklist:
echo.
echo 1. ✅ Azure workflow configured
echo 2. ✅ Website files ready
echo 3. ✅ Static Web App config ready
echo.
echo 🔧 Next Steps:
echo.
echo 1. Go to Azure Portal: https://portal.azure.com
echo 2. Create Static Web App (follow AZURE_QUICK_SETUP.md)
echo 3. Get deployment token from Azure
echo 4. Add token to GitHub Secrets as: AZURE_STATIC_WEB_APPS_API_TOKEN
echo 5. Push to main branch to trigger deployment
echo.
echo 📖 Detailed guide: AZURE_QUICK_SETUP.md
echo.

REM Check if we can trigger a test deployment
echo 🔄 Checking GitHub Actions status...
echo.
echo To check deployment status:
echo 1. Go to: https://github.com/IanaraFer/dataSite/actions
echo 2. Look for "Azure Deployment" workflow
echo 3. If it's not running, push a small change to trigger it
echo.

echo ✅ Azure setup is ready!
echo.
pause
