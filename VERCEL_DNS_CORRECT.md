# 🔧 Vercel DNS Configuration - CORRECT Setup

## 🤔 What You Found vs What You Need

**What you found:**
```
ns1.vercel-dns.com
ns2.vercel-dns.com
```
These are **NAMESERVERS** - different from what we need.

**What we actually need for Blacknight:**
```
CNAME @ cname.vercel-dns.com
CNAME www cname.vercel-dns.com
```

## 📋 CORRECT Blacknight DNS Setup

### Method 1: CNAME Records (RECOMMENDED)
**Login to Blacknight Control Panel: https://cp.blacknight.com**

**Add these DNS records:**
```
Type: CNAME
Name: @
Value: cname.vercel-dns.com
TTL: 3600

Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: 3600
```

### Method 2: A Records (Alternative)
If CNAME doesn't work for root domain (@), use these A records:
```
Type: A
Name: @
Value: 76.76.21.21
TTL: 3600

Type: A
Name: www
Value: 76.76.21.21
TTL: 3600
```

## 🎯 Step-by-Step Blacknight Setup

### Step 1: Deploy to Vercel First
1. Go to https://vercel.com
2. Sign up with GitHub
3. Import project: `IanaraFer/dataSite`
4. Deploy (one click!)

### Step 2: Add Custom Domain in Vercel
1. In Vercel dashboard: Settings → Domains
2. Add: `analyticacoreai.ie`
3. Vercel will show you the DNS values needed

### Step 3: Configure DNS in Blacknight
1. **Login**: https://cp.blacknight.com
2. **Navigate**: Domains → analyticacoreai.ie → DNS Management
3. **Add the CNAME records** shown above

### Step 4: Verify Setup
After adding DNS records, Vercel will automatically:
- ✅ Verify domain ownership
- ✅ Issue SSL certificate
- ✅ Route traffic to your site

## ⚠️ Common Confusion: Nameservers vs CNAME

**Nameservers (ns1.vercel-dns.com):**
- Transfer complete DNS control to Vercel
- Replace Blacknight's nameservers entirely
- More complex setup

**CNAME Records (cname.vercel-dns.com):**
- Keep DNS control with Blacknight
- Just point specific domains to Vercel
- Simpler and recommended approach

## 🚀 IMMEDIATE ACTION PLAN

### Right Now:
1. **Deploy to Vercel** (5 minutes)
2. **Add custom domain** in Vercel dashboard
3. **Note the DNS values** Vercel provides

### Then:
1. **Login to Blacknight**: https://cp.blacknight.com
2. **Add CNAME records**: Use `cname.vercel-dns.com` as the value
3. **Wait for propagation**: Usually 1-4 hours with Blacknight

### Result:
- ✅ Professional site at https://analyticacoreai.ie
- ✅ Automatic SSL certificate
- ✅ Global CDN performance

**The key is using `cname.vercel-dns.com` in your CNAME records, not the nameservers you found!**

Ready to deploy to Vercel first?
