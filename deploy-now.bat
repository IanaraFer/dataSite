@echo off
echo ==========================================
echo   DEPLOYING TO NETLIFY NOW
echo ==========================================
echo.
echo Connecting to Netlify...
netlify login
echo.
echo Deploying production site...
netlify deploy --prod --dir=website
echo.
echo Adding custom domain...
netlify domains:add analyticacoreai.ie
echo.
echo ==========================================
echo   DEPLOYMENT COMPLETE!
echo ==========================================
echo.
echo Your site is live at: analyticacoreai.ie
echo DNS records will be shown below:
echo.
netlify domains:list
echo.
pause
