# 🎯 EXACT BLACKNIGHT DNS SETUP - analyticacoreai.ie

## ✅ Your Current Configuration

**Domain**: analyticacoreai.ie  
**Registrar**: Blacknight Solutions  
**Status**: Finalized and Ready  
**Nameservers**: 
```
ns1.blacknightdns.com ✅
ns2.blacknightdns.com ✅  
ns3.blacknightdns.com ✅
ns4.blacknightdns.com ✅
```

**Perfect!** Your domain is properly configured with Blacknight DNS.

## 🔧 EXACT DNS RECORDS TO ADD

### Step 1: Login to Blacknight
- **URL**: https://cp.blacknight.com
- **Navigate**: Domains → Manage → analyticacoreai.ie → DNS Management

### Step 2: Add These Exact Records

#### For Website Hosting (Vercel):
```
Record Type: CNAME
Name: @ (or leave blank for root domain)
Points to: cname.vercel-dns.com
TTL: 3600

Record Type: CNAME  
Name: www
Points to: cname.vercel-dns.com
TTL: 3600
```

#### For Professional Email (SendGrid):
```
Record Type: CNAME
Name: em7602
Points to: u42139136.wl134.sendgrid.net
TTL: 3600

Record Type: CNAME
Name: s1._domainkey  
Points to: s1.domainkey.u42139136.wl134.sendgrid.net
TTL: 3600

Record Type: CNAME
Name: s2._domainkey
Points to: s2.domainkey.u42139136.wl134.sendgrid.net  
TTL: 3600

Record Type: TXT
Name: @ (root domain)
Value: v=spf1 include:sendgrid.net ~all
TTL: 3600

Record Type: TXT  
Name: _dmarc
Value: v=DMARC1; p=none; rua=mailto:contact@analyticacoreai.ie
TTL: 3600
```

## 📋 Blacknight DNS Interface Guide

### How to Add Records in Blacknight:

1. **Login**: https://cp.blacknight.com
2. **Find Your Domain**: Click on "analyticacoreai.ie"
3. **DNS Management**: Look for "DNS" or "Manage DNS" button
4. **Add Record**: Click "Add New Record" or similar
5. **Fill Fields**:
   - **Type**: Select CNAME or TXT from dropdown
   - **Name/Host**: Enter exactly as shown above
   - **Value/Points to**: Enter exactly as shown above  
   - **TTL**: Set to 3600 (1 hour)
6. **Save**: Click Save/Apply/Submit

### ⚠️ Important Blacknight Notes:

- **Root Domain (@)**: If Blacknight doesn't accept "@", leave the Name field blank
- **TTL**: Use 3600 (1 hour) for faster propagation during setup
- **CNAME Limitation**: Some systems don't allow CNAME for root domain, use A record instead if needed:
  ```
  Type: A
  Name: @ (or blank)
  Value: 76.76.21.21
  TTL: 3600
  ```

## ⏰ Propagation Timeline

- **Blacknight DNS**: 15 minutes - 2 hours  
- **Global Propagation**: 2-24 hours
- **SSL Certificate**: Automatic once domain verifies

## ✅ Verification Steps

### Check DNS Propagation:
```powershell
nslookup analyticacoreai.ie
nslookup www.analyticacoreai.ie
```

### Check in Vercel:
- Dashboard → Settings → Domains → analyticacoreai.ie
- Should show "Valid Configuration" when DNS propagates

## 🎯 WHAT HAPPENS NEXT

1. **You add DNS records** in Blacknight (10 minutes)
2. **DNS propagates** (1-4 hours typically)  
3. **Vercel detects domain** and issues SSL certificate
4. **Site goes live** at https://analyticacoreai.ie
5. **Email authentication** activates
6. **Professional SaaS platform** fully operational

## 🚀 READY TO ADD DNS RECORDS?

**Your task**: Add the CNAME and TXT records above in your Blacknight control panel.

**My task**: Guide you through any issues and configure the email system once DNS is working.

**Login here to start**: https://cp.blacknight.com

Need help with any step? Just ask!
