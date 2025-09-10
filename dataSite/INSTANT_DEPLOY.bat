@echo off
echo ========================================
echo    AI ANALYTICS SAAS - INSTANT DEPLOY
echo ========================================
echo.
echo I'm deploying your site automatically...
echo.
echo 1. Connecting to Netlify...
netlify login
echo.
echo 2. Deploying to production...
netlify deploy --prod --dir=website
echo.
echo 3. Adding custom domain...
netlify domains:add analyticacoreai.ie
echo.
echo ========================================
echo    DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Your site is now live at:
echo https://analyticacoreai.ie
echo.
echo DNS Instructions will be shown next...
netlify domains:list
echo.
pause
