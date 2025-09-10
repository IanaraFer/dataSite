# Immediate Email Setup - AnalyticaCore AI

## 🚀 Get Email Working in 5 Minutes

Since your `.ie` domain is still in verification, let's get emails working immediately with a temporary setup.

### Option 1: Single Sender Verification (Recommended)

1. **Go to SendGrid** → https://app.sendgrid.com/settings/sender_auth/senders/new
2. **Add Single Sender**:
   ```
   From Name: AnalyticaCore AI Support
   From Email: your-email@gmail.com (or your business email)
   Reply To: your-email@gmail.com
   ```
3. **Verify the email** (check your inbox)
4. **Get API Key** → https://app.sendgrid.com/settings/api_keys
5. **Add to Vercel Environment Variables**:
   ```
   SENDGRID_API_KEY=SG.your_api_key_here
   FROM_EMAIL=your-email@gmail.com
   FROM_NAME=AnalyticaCore AI Support
   ```

### Option 2: Use Your Current Business Email

If you have a business email (like Gmail Workspace):
```env
FROM_EMAIL=contact@yourbusiness.com
FROM_NAME=AnalyticaCore AI
```

### Option 3: Create a Free Business Email

Quick setup with ProtonMail or Gmail:
1. Create: `analyticacore@gmail.com`
2. Use this as your FROM_EMAIL temporarily
3. Professional enough for early customers

## 🔄 Easy Migration Later

When `analyticacoreai.ie` is ready:
1. Update SendGrid domain authentication
2. Change environment variable: `FROM_EMAIL=information@analyticacoreai.ie`
3. Customers won't notice the change!

## ✅ Test Email Sending

Once configured, test with this curl command:

```bash
curl -X POST https://data-site-zucu.vercel.app/api/trial/submit \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Test",
    "lastName": "User", 
    "email": "your-test-email@gmail.com",
    "phone": "123-456-7890",
    "company": "Test Company",
    "industry": "Technology",
    "revenue": "€100k-€500k"
  }'
```

## 📧 What Customers Will See

**Email Header:**
```
From: AnalyticaCore AI Support <your-email@gmail.com>
Subject: 🚀 Welcome to AnalyticaCore AI - Trial Activated!
```

This looks professional and builds trust while you wait for the perfect domain setup.

---

**Ready to go live with professional emails today!** 🎯
