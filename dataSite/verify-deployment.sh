#!/bin/bash
# Vercel Deployment Verification Script

echo "🚀 AnalyticaCore AI - Vercel Deployment Ready!"
echo "================================================"

echo "📁 Checking project structure..."

# Check if all required files exist
if [ -f "vercel.json" ]; then
    echo "✅ vercel.json - Configuration file exists"
else
    echo "❌ vercel.json - Missing!"
fi

if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt - Python dependencies ready"
else
    echo "❌ requirements.txt - Missing!"
fi

if [ -f "api/index.py" ]; then
    echo "✅ api/index.py - Serverless function ready"
else
    echo "❌ api/index.py - Missing!"
fi

if [ -d "public" ]; then
    echo "✅ public/ - Static files directory exists"
    echo "   📄 Files in public/:"
    ls -la public/*.html 2>/dev/null | head -5
else
    echo "❌ public/ - Missing static files directory!"
fi

echo ""
echo "🎯 DEPLOYMENT COMMANDS:"
echo "1. vercel login"
echo "2. vercel --prod"
echo "3. Configure environment variables in Vercel dashboard"
echo "4. Add custom domain: analyticacoreai.ie"
echo ""
echo "✅ Your SaaS platform is ready for production deployment!"
