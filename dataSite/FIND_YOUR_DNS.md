# 🔍 How to Find Your DNS Management

## 📍 Where Did You Register Your Domain?

To find your DNS settings, you need to access your domain registrar's control panel. Here are the most common Irish domain registrars:

### 🇮🇪 Irish Registrars

#### **1. Blacknight Solutions**
- **Website**: https://cp.blacknight.com
- **DNS Location**: Login → Domains → Manage → DNS Management
- **Login**: Use the email/password from your registration

#### **2. Register365 (Hosting Ireland)**
- **Website**: https://www.register365.com
- **DNS Location**: Control Panel → Domain Management → DNS
- **Login**: Check your registration email for login details

#### **3. IE Domain Registry Direct**
- **Website**: https://www.iedr.ie
- **Note**: If registered directly, you'll need to transfer to a registrar for DNS management

#### **4. Domain.ie**
- **Website**: https://www.domain.ie
- **DNS Location**: Customer Area → Domains → DNS Management

#### **5. GoDaddy Ireland**
- **Website**: https://ie.godaddy.com
- **DNS Location**: My Products → Domains → DNS → Manage

### 🌐 International Registrars (also serve Ireland)

#### **Namecheap**
- **Website**: https://ap.www.namecheap.com
- **DNS Location**: Domain List → Manage → Advanced DNS

#### **Cloudflare Registrar**
- **Website**: https://dash.cloudflare.com
- **DNS Location**: Websites → Select Domain → DNS → Records

## 🔍 How to Find Your Registrar

### Method 1: Check Your Email
Look for the domain registration confirmation email. It will contain:
- Registrar name
- Login credentials
- Management panel link

### Method 2: WHOIS Lookup
```powershell
# Run this command to see registrar info
nslookup -type=NS analyticacoreai.ie
```

### Method 3: Online WHOIS Tools
- Visit: https://who.is/whois/analyticacoreai.ie
- Look for "Registrar" field

## 📋 What You'll Need to Set Up

Once you find your DNS panel, you'll configure these records:

### **For Website Hosting (Vercel Recommended)**
```
Type: CNAME
Name: @
Value: cname.vercel-dns.com

Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

### **For Professional Email (SendGrid)**
```
Type: CNAME
Name: em123.analyticacoreai.ie
Value: u[your-number].wl[number].sendgrid.net

Type: CNAME
Name: s1._domainkey.analyticacoreai.ie
Value: s1.domainkey.u[your-number].wl[number].sendgrid.net

Type: CNAME
Name: s2._domainkey.analyticacoreai.ie  
Value: s2.domainkey.u[your-number].wl[number].sendgrid.net

Type: TXT
Name: @
Value: v=spf1 include:sendgrid.net ~all
```

## 🚀 Quick Steps to Get Started

1. **Find your registrar** (check email confirmation)
2. **Log into DNS management** 
3. **Deploy to Vercel first** (I'll help you)
4. **Get DNS values from Vercel**
5. **Add DNS records**
6. **Wait for propagation** (up to 48 hours)

## 💡 Pro Tip: Start with Vercel

**Don't wait for DNS!** Deploy to Vercel now:
```powershell
npm install -g vercel
cd C:\Users\35387\Desktop\dataSite
vercel --prod
```

You'll get a temporary URL immediately, then add your custom domain later!

---

**Which registrar did you use for analyticacoreai.ie?** I can give you specific instructions once I know!
