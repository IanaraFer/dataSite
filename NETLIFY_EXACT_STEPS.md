# 🚀 NETLIFY SETUP - EXACT STEPS FOR ANALYTICACOREAI.IE

## ✅ **PREPARATION COMPLETE:**
- ✅ Your code is on GitHub: `https://github.com/IanaraFer/dataSite`
- ✅ You have Netlify account
- ✅ Website working locally

## 📋 **STEP-BY-STEP NETLIFY DEPLOYMENT:**

### **STEP 1: Access Your Netlify Dashboard**
1. Go to **https://app.netlify.com**
2. Login with your existing account
3. You should see your Netlify dashboard

### **STEP 2: Create New Site**
1. Look for a button that says **"Add new site"** or **"New site from Git"**
2. Click on it
3. You'll see deployment options

### **STEP 3: Connect to GitHub**
1. Click **"Import an existing project"** or **"Deploy with GitHub"**
2. If prompted, authorize Netlify to access your GitHub
3. You'll see a list of your repositories

### **STEP 4: Select Your Repository**
1. Look for **"dataSite"** in the repository list
2. Click on **"dataSite"** to select it
3. Click **"Deploy site"** or similar button

### **STEP 5: Configure Build Settings**
You'll see a form with these fields - **IMPORTANT SETTINGS:**

```
Repository: IanaraFer/dataSite ✅
Branch to deploy: main ✅
Base directory: (LEAVE EMPTY)
Build command: (LEAVE EMPTY)  
Publish directory: website
```

**⚠️ CRITICAL:** Make sure "Publish directory" says **"website"** (not public, not root)

### **STEP 6: Deploy**
1. Click **"Deploy site"** button
2. Netlify will start building your site
3. Wait 2-3 minutes for deployment to complete

### **STEP 7: Get Your Temporary URL**
1. After deployment, you'll get a URL like:
   `https://amazing-unicorn-123456.netlify.app`
2. Click on this URL to test your site
3. **VERIFY:** Check that your website loads correctly

## 🌐 **STEP 8: ADD CUSTOM DOMAIN (analyticacoreai.ie)**

### **In Netlify Dashboard:**
1. Go to **"Site settings"** 
2. Click **"Domain management"** in the left sidebar
3. Click **"Add custom domain"**
4. Enter: **`analyticacoreai.ie`**
5. Click **"Verify"**
6. Netlify will show DNS instructions

### **DNS Records You'll Need:**
Netlify will give you something like:
```
Type: CNAME
Name: www
Value: amazing-unicorn-123456.netlify.app

Type: A  
Name: @
Value: 75.2.60.5
```

## 📡 **STEP 9: UPDATE DNS AT BLACKNIGHT**

### **Access Blacknight DNS:**
1. Login to **blacknight.ie**
2. Go to **"My Services"** → **"Domain Names"**
3. Find **analyticacoreai.ie**
4. Click **"Manage DNS"** or **"DNS Management"**

### **Update DNS Records:**
1. **Delete existing A records** for @ (root domain)
2. **Delete existing CNAME records** for www
3. **Add new records** from Netlify:
   ```
   Type: CNAME
   Name: www  
   Value: [your-netlify-url].netlify.app
   
   Type: A
   Name: @
   Value: 75.2.60.5
   ```
4. **Save changes**

## ⏰ **STEP 10: WAIT FOR DNS PROPAGATION**
- DNS changes take **15-60 minutes**
- Test with: https://dnschecker.org
- Enter: analyticacoreai.ie

## 🔒 **STEP 11: ENABLE SSL (AUTOMATIC)**
- Netlify automatically provides SSL
- Within 24 hours: https://analyticacoreai.ie will work
- No action needed from you

## 🎉 **EXPECTED RESULT:**

### **What Will Work:**
- ✅ **https://analyticacoreai.ie** - Your homepage
- ✅ **https://analyticacoreai.ie/pricing.html** - Payment plans  
- ✅ **https://analyticacoreai.ie/platform.html** - File upload
- ✅ **Mobile responsive** design
- ✅ **SSL security** (HTTPS)
- ✅ **Fast loading** times

### **What You Can Do Immediately:**
- ✅ Accept customer payments (€199/€399/€799)
- ✅ Process file uploads (CSV/Excel)
- ✅ Collect leads through contact forms
- ✅ Professional business presence

## 🔧 **TROUBLESHOOTING:**

### **If Repository Not Found:**
- Make sure GitHub account is connected to Netlify
- Repository must be public or Netlify needs access

### **If Site Doesn't Load:**
- Check "Publish directory" is set to **"website"**
- Look at Netlify build logs for errors

### **If Domain Doesn't Work:**
- DNS propagation takes time (up to 60 minutes)
- Use dnschecker.org to verify
- Use temporary Netlify URL meanwhile

## 📞 **NEED HELP?**

If you get stuck on any step, tell me:
1. **Which step** you're on
2. **What you see** on your screen
3. **Any error messages**

I'll guide you through the exact solution!

## 🎯 **YOUR BUSINESS WILL BE LIVE:**

After completing these steps:
- ✅ **analyticacoreai.ie** will be fully operational
- ✅ **Professional SaaS platform** live
- ✅ **Ready for customers** and payments
- ✅ **Irish AI analytics business** online

**Let's get your platform live! Start with Step 1 and let me know what you see.**
