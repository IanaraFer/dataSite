# ?? STRIPE PAYMENT SETUP - COMPLETE GUIDE

## ?? WHERE THE MONEY GOES:
- Money goes directly to YOUR bank account
- Stripe takes 2.9% + €0.25 per transaction
- You get paid every 2-7 days automatically
- You receive email notifications for every payment

## ?? STEP-BY-STEP SETUP:

### 1. CREATE STRIPE ACCOUNT:
- Go to: https://stripe.com
- Sign up with your business email
- Complete business verification
- Add your BANK ACCOUNT (where money will go)

### 2. VERIFY YOUR BUSINESS:
- Business name: AnalyticaCore AI
- Business type: Software/SaaS
- Country: Ireland
- Add your Irish bank account details

### 3. CREATE SUBSCRIPTION PRODUCTS:
- Go to Stripe Dashboard ? Products
- Create 3 products:
  * Starter Plan - €199/month
  * Professional Plan - €399/month  
  * Enterprise Plan - €799/month

### 4. GET STRIPE KEYS:
- Go to Developers ? API Keys
- Copy: Publishable key (pk_live_...)
- Copy: Secret key (sk_live_...)
- KEEP THESE SAFE!

### 5. CREATE CUSTOMER PORTAL:
- Go to Settings ? Customer Portal
- Enable customer portal
- This allows customers to manage subscriptions

## ?? TECHNICAL SETUP NEEDED:

### Environment Variables for Netlify:
`
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
`

### Webhook Setup:
- Go to Developers ? Webhooks
- Add endpoint: https://analyticacoreai.netlify.app/.netlify/functions/webhook
- Select events: customer.subscription.created, invoice.payment_succeeded

## ?? EMAIL NOTIFICATIONS:
- You'll get emails for every payment
- Customer gets receipt emails
- Failed payment notifications
- Subscription status changes

## ?? MONEY FLOW:
1. Customer subscribes ? Stripe processes payment
2. Money goes to your Irish bank account (minus fees)
3. You get instant email notification
4. Customer gets receipt
5. Recurring billing happens automatically

## ?? IMPORTANT:
- Start with TEST MODE first
- Use test card: 4242 4242 4242 4242
- Switch to LIVE MODE only after testing
- Keep API keys secure (never share publicly)
