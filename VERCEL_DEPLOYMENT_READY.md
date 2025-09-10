# 🚀 VERCEL DEPLOYMENT GUIDE - AnalyticaCore AI

## ✅ PROJECT READY FOR VERCEL DEPLOYMENT

Your AnalyticaCore AI platform is now properly formatted for Vercel deployment with:

### 📁 Project Structure
```
dataSite/
├── public/                 # Static website files
│   ├── index.html         # Homepage
│   ├── pricing.html       # Payment plans
│   ├── platform.html      # AI analytics platform
│   └── [all other files] # Additional pages and assets
├── api/
│   └── index.py          # FastAPI serverless functions
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── package.json          # Node.js configuration
└── .env.vercel          # Environment variables template
```

## 🔧 DEPLOYMENT STEPS

### 1. Install Vercel CLI
```powershell
npm install -g vercel
```

### 2. Login to Vercel
```powershell
vercel login
```

### 3. Deploy to Vercel
```powershell
cd c:\Users\35387\Desktop\dataSite
vercel
```

### 4. Configure Environment Variables in Vercel Dashboard
Go to your project settings and add these environment variables:

#### Required Stripe Variables:
- `STRIPE_SECRET_KEY` = `sk_test_your_actual_stripe_secret_key`
- `STRIPE_PUBLISHABLE_KEY` = `pk_test_your_actual_stripe_publishable_key`
- `STRIPE_WEBHOOK_SECRET` = `whsec_your_webhook_secret`

#### Required SendGrid Variables:
- `SENDGRID_API_KEY` = `SG.your_actual_sendgrid_api_key`
- `FROM_EMAIL` = `information@analyticacoreai.ie`
- `FROM_NAME` = `AnalyticaCore AI`

#### Optional Variables:
- `GOOGLE_ANALYTICS_ID` = `G-XXXXXXXXXX`
- `ENVIRONMENT` = `production`

### 5. Configure Custom Domain
1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add domain: `analyticacoreai.ie`
3. Add domain: `www.analyticacoreai.ie`
4. Copy the DNS records provided by Vercel
5. Add these to your Blacknight DNS settings:

```
Type: CNAME
Name: www
Value: cname.vercel-dns.com

Type: A
Name: @
Value: 76.76.19.19

Type: A  
Name: @
Value: 76.223.126.88
```

## 🎯 FEATURES WORKING IN DEPLOYMENT

### ✅ Static Website
- Homepage with hero section
- Pricing page with 3 subscription tiers
- Platform upload page
- All Bootstrap/CSS styling
- Responsive design

### ✅ API Endpoints
- `/api/health` - Health check
- `/api/payment/subscribe` - Stripe subscription
- `/api/trial/submit` - Free trial signup
- `/api/webhook/stripe` - Stripe webhooks

### ✅ Payment System
- Email validation
- Stripe integration ready
- Success/error handling
- Google Analytics tracking

### ✅ File Upload System
- CSV/Excel file upload
- Drag & drop interface
- File validation
- Progress indicators

## 🚀 QUICK DEPLOYMENT COMMANDS

### Deploy Now:
```powershell
cd c:\Users\35387\Desktop\dataSite
vercel --prod
```

### Local Testing:
```powershell
cd c:\Users\35387\Desktop\dataSite
vercel dev
```

## 📱 POST-DEPLOYMENT CHECKLIST

1. **✅ Test Homepage**: Visit https://analyticacoreai.ie
2. **✅ Test Payment Flow**: Try subscribing to a plan
3. **✅ Test Upload System**: Upload a CSV file
4. **✅ Test API Endpoints**: Check /api/health
5. **✅ Test Email System**: Submit trial form
6. **✅ SSL Certificate**: Verify HTTPS works
7. **✅ Mobile Responsive**: Test on mobile devices

## 🔧 TROUBLESHOOTING

### If Build Fails:
1. Check requirements.txt syntax
2. Verify Python version compatibility
3. Check vercel.json configuration

### If Routes Don't Work:
1. Verify vercel.json routes section
2. Check file paths in public/ directory
3. Test locally with `vercel dev`

### If API Fails:
1. Check environment variables in Vercel dashboard
2. Verify Stripe/SendGrid credentials
3. Check Python dependencies

## 🎉 SUCCESS INDICATORS

- ✅ Website loads at https://analyticacoreai.ie
- ✅ Payment forms work without errors
- ✅ File upload functions properly
- ✅ API endpoints respond correctly
- ✅ SSL certificate active
- ✅ Custom domain configured

## 📞 SUPPORT

Your platform is ready for professional deployment with:
- Stripe payment processing
- SendGrid email automation
- File upload functionality
- Responsive design
- SSL security
- Custom domain support

**🚀 Ready to launch your AI analytics SaaS business!**
