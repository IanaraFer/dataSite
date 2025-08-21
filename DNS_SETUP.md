# AnalyticaCore AI - DNS Configuration Guide

## 🌐 Domain: analyticacoreai.ie

### SendGrid Email Authentication Records

Add these records to your domain's DNS management panel:

```dns
# SendGrid Domain Authentication
Type    Host                                    Value
----    ----                                    -----
CNAME   url8860.analyticacoreai.ie             sendgrid.net
CNAME   55387076.analyticacoreai.ie            sendgrid.net  
CNAME   em4558.analyticacoreai.ie              u55387076.wl077.sendgrid.net
CNAME   s1._domainkey.analyticacoreai.ie       s1.domainkey.u55387076.wl077.sendgrid.net
CNAME   s2._domainkey.analyticacoreai.ie       s2.domainkey.u55387076.wl077.sendgrid.net
TXT     _dmarc.analyticacoreai.ie              v=DMARC1; p=none;
```

### Vercel Hosting Records (Add these when domain verification completes)

```dns
# Vercel Website Hosting
Type    Host                    Value
----    ----                    ----
A       analyticacoreai.ie      76.76.19.61
CNAME   www                     cname.vercel-dns.com
```

## 🔧 Setup Steps

### 1. DNS Provider Access
- Log into your .ie domain registrar
- Navigate to DNS Management / DNS Zone
- Add the records above

### 2. SendGrid Verification
- After adding DNS records, go to SendGrid Dashboard
- Settings > Sender Authentication
- Verify domain authentication
- Wait 24-48 hours for propagation

### 3. Email Testing
- Send test emails from contact@analyticacoreai.ie
- Check spam folders initially
- Monitor SendGrid delivery statistics

### 4. DMARC Monitoring
- Start with `p=none` (monitoring only)
- After 1-2 weeks, upgrade to `p=quarantine`
- Eventually use `p=reject` for maximum protection

## 📊 Expected Results

### Email Deliverability Improvements:
- ✅ Professional email authentication
- ✅ Reduced spam filtering  
- ✅ Improved inbox delivery rates
- ✅ Brand protection from spoofing
- ✅ SendGrid analytics and reporting

### Business Impact:
- Higher trial confirmation email open rates
- Better customer onboarding experience
- Professional sender reputation
- Compliance with email best practices

## 🛠️ Troubleshooting

### Common Issues:
1. **TTL Settings**: Use 300-3600 seconds
2. **Subdomain Format**: Ensure exact match including dots
3. **Propagation Time**: Allow 24-48 hours
4. **Case Sensitivity**: Use lowercase for hosts

### Verification Commands:
```bash
# Check CNAME records
nslookup url8860.analyticacoreai.ie
nslookup s1._domainkey.analyticacoreai.ie

# Check TXT record  
nslookup -type=TXT _dmarc.analyticacoreai.ie
```

## 📧 Email Configuration

Once DNS is setup, update your environment variables:

```env
FROM_EMAIL=contact@analyticacoreai.ie
SENDGRID_FROM_NAME=AnalyticaCore AI
SENDGRID_DOMAIN=analyticacoreai.ie
```

## Next Steps

1. ✅ Add DNS records to your domain registrar
2. ✅ Verify domain in SendGrid dashboard  
3. ✅ Test email sending functionality
4. ✅ Monitor delivery rates and adjust if needed
5. ✅ Update environment variables in Vercel

Your professional email setup will be complete! 🎯
