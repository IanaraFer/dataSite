@echo off
echo ========================================
echo   🚀 DataSiteAI Website Deployment Helper
echo ========================================
echo.
echo Your website files are ready in the 'website' folder!
echo.
echo 📁 Website files location: %cd%\website
echo.
echo 🌐 FASTEST DEPLOYMENT OPTIONS:
echo.
echo 1. NETLIFY (Recommended - 2 minutes):
echo    → Go to: https://netlify.com
echo    → Sign up / Login
echo    → Drag the 'website' folder to deploy
echo    → Get instant URL!
echo.
echo 2. GITHUB PAGES (Free forever):
echo    → Go to: https://github.com
echo    → Create new repository
echo    → Upload files from 'website' folder
echo    → Enable Pages in Settings
echo.
echo 3. VERCEL (Developer friendly):
echo    → Go to: https://vercel.com
echo    → Connect GitHub or drag folder
echo    → Auto-deploy!
echo.
echo ========================================
echo Opening website folder for you...
echo ========================================
explorer "%cd%\website"
echo.
echo 💡 TIP: For Netlify, just drag the 'website' folder
echo    that just opened to netlify.com deploy area!
echo.
pause
