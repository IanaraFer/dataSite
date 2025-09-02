# 🚀 DEPLOY ANALYTICACORE AI - STEP BY STEP

## ✅ Pre-Flight Check
- [x] Domain registered: `analyticacoreai.ie` ✅
- [x] Code on GitHub: `IanaraFer/dataSite` ✅  
- [x] All files ready ✅
- [x] Local testing complete ✅

## 🎯 DEPLOY TO VERCEL (5 minutes)

### Step 1: Open Vercel
1. Go to: **https://vercel.com**
2. Click **"Sign up"** and choose **"Continue with GitHub"**
3. Authorize Vercel to access your repositories

### Step 2: Import Your Project
1. Click **"Add New Project"** or **"Import Project"**
2. Find and select: **`IanaraFer/dataSite`**
3. Click **"Import"**

### Step 3: Configure Deployment
```
Framework Preset: Other
Root Directory: ./website
Build Command: (leave empty)
Output Directory: (leave empty)  
Install Command: (leave empty)
```

### Step 4: Add Environment Variables
Click **"Environment Variables"** and add:

```
STRIPE_SECRET_KEY=sk_test_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
SENDGRID_API_KEY=SG.your_sendgrid_key
SENDGRID_FROM_EMAIL=contact@analyticacoreai.ie
```

### Step 5: Deploy
1. Click **"Deploy"**
2. Wait 2-3 minutes for build
3. Copy your deployment URL (something like `your-project.vercel.app`)

## 🌐 CONNECT YOUR DOMAIN (10 minutes)

### Step 1: Add Domain in Vercel
1. In your Vercel project dashboard
2. Go to **"Settings"** → **"Domains"**
3. Add: `analyticacoreai.ie`
4. Add: `www.analyticacoreai.ie`
5. Copy the DNS records Vercel shows you

### Step 2: Configure Blacknight DNS
1. Login to: **https://cp.blacknight.com**
2. Go to **"DNS Manager"** for `analyticacoreai.ie`
3. Add these records:

```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: 300

Type: A  
Name: @
Value: [Vercel will give you the IP]
TTL: 300
```

### Step 3: Wait for Propagation
- DNS changes take 5-15 minutes
- Check at: https://whatsmydns.net

## 🎉 FINAL RESULT

Your professional SaaS platform will be live at:
- **https://analyticacoreai.ie**
- **https://www.analyticacoreai.ie**

With features:
- ✅ Stripe payment processing (€199/€399/€799)
- ✅ SendGrid email automation
- ✅ Google Analytics tracking
- ✅ Professional domain
- ✅ SSL certificate
- ✅ Global CDN

## 🆘 Need Help?
If you get stuck, just ask and I'll help troubleshoot!
