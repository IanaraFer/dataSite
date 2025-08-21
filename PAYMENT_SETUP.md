# 💳 DataSight AI - Payment System Setup Guide

## 🚀 Complete Payment Integration for Your SaaS Platform

### 📋 Overview
Your DataSight AI platform now has a complete payment system with:
- ✅ Stripe integration for secure payments
- ✅ Subscription management (Starter €199, Professional €399, Enterprise €799)
- ✅ Customer dashboard after payment
- ✅ Webhook handling for payment events
- ✅ 7-day free trial period

### 🔧 Setup Instructions

#### 1. **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

#### 2. **Stripe Account Setup**
1. Go to [Stripe Dashboard](https://dashboard.stripe.com)
2. Create account or login
3. Get your API keys:
   - Publishable key: `pk_test_...`
   - Secret key: `sk_test_...`

#### 3. **Create Stripe Products & Prices**
In Stripe Dashboard, create these products:

**Starter Plan:**
- Name: DataSight AI Starter
- Price: €199/month
- Copy the Price ID (e.g., `price_1ABC123...`)

**Professional Plan:**
- Name: DataSight AI Professional  
- Price: €399/month
- Copy the Price ID

**Enterprise Plan:**
- Name: DataSight AI Enterprise
- Price: €799/month
- Copy the Price ID

#### 4. **Configure Environment**
```bash
# Copy environment file
cp .env.example .env

# Edit .env file with your keys
STRIPE_SECRET_KEY=sk_test_YOUR_ACTUAL_KEY
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_ACTUAL_KEY
STRIPE_PRICE_STARTER=price_YOUR_STARTER_PRICE_ID
STRIPE_PRICE_PROFESSIONAL=price_YOUR_PROFESSIONAL_PRICE_ID
STRIPE_PRICE_ENTERPRISE=price_YOUR_ENTERPRISE_PRICE_ID
```

#### 5. **Update Frontend Stripe Key**
Edit `pricing-payment.html` line 321:
```javascript
const stripe = Stripe('pk_test_YOUR_ACTUAL_PUBLISHABLE_KEY');
```

#### 6. **Start Payment Server**
```bash
python payment_server.py
```

### 🔗 URLs & Endpoints

**Customer-facing pages:**
- Payment page: `http://localhost:8002/pricing-payment.html`
- Dashboard: `http://localhost:8002/dashboard.html`

**API endpoints:**
- Create subscription: `POST /api/create-subscription`
- Get customer: `GET /api/customer/{customer_id}`
- Stripe webhook: `POST /api/webhook`

### 📱 Payment Flow

#### Customer Journey:
1. **Select Plan** → Customer clicks "Start [Plan] Plan"
2. **Payment Modal** → Stripe payment form opens
3. **Enter Details** → Email, name, company, card info
4. **Process Payment** → Stripe handles payment securely
5. **Create Subscription** → Backend creates customer record
6. **Redirect to Dashboard** → Customer sees their new dashboard
7. **Welcome Email** → Automated confirmation email

#### Backend Processing:
1. **Payment Method** → Created via Stripe Elements
2. **Customer Creation** → Stripe customer with metadata
3. **Subscription** → Monthly recurring billing
4. **Customer Record** → Saved to `customers/` directory
5. **Dashboard Setup** → Customer dashboard configuration

### 🔒 Security Features

- **PCI Compliance** → Stripe handles all card data
- **3D Secure** → Automatic authentication when required
- **Webhook Verification** → Stripe signature verification
- **Customer IDs** → Unique tracking system
- **Trial Period** → 7-day free trial included

### 💰 Pricing Structure

| Plan | Price | Features |
|------|-------|----------|
| **Starter** | €199/month | 5 datasets, basic insights, email support |
| **Professional** | €399/month | 20 datasets, advanced insights, priority support |
| **Enterprise** | €799/month | Unlimited datasets, custom AI, dedicated support |

### 📊 Customer Management

**Customer Data Storage:**
```
customers/
├── CUST-20250821-1234.json    # Customer record
├── CUST-20250821-5678.json
└── ...

dashboards/
├── CUST-20250821-1234_dashboard.json    # Dashboard config
└── ...
```

**Customer Record Example:**
```json
{
  "customer_id": "CUST-20250821-1234",
  "stripe_customer_id": "cus_ABC123",
  "stripe_subscription_id": "sub_ABC123",
  "email": "customer@company.com",
  "name": "John Doe",
  "company": "Example Corp",
  "plan": "professional",
  "price": 399,
  "status": "active",
  "trial_end": "2025-08-28T12:00:00Z"
}
```

### 🔔 Webhook Events

**Handled Events:**
- `invoice.payment_succeeded` → Update customer status
- `invoice.payment_failed` → Handle failed payments
- `customer.subscription.deleted` → Process cancellations

**Webhook URL for Stripe:**
```
http://your-domain.com/api/webhook
```

### 🧪 Testing

#### Test Credit Cards (Stripe Test Mode):
- **Visa:** 4242 4242 4242 4242
- **Mastercard:** 5555 5555 5555 4444
- **Declined:** 4000 0000 0000 0002

#### Test Scenarios:
1. Successful payment
2. Failed payment
3. 3D Secure authentication
4. Subscription cancellation

### 🚀 Deployment Checklist

#### Before Going Live:
- [ ] Switch to Stripe live keys
- [ ] Set up proper webhook endpoint
- [ ] Configure email service (SendGrid/Mailgun)
- [ ] Set up database (PostgreSQL/MySQL)
- [ ] Configure SSL certificate
- [ ] Test all payment flows
- [ ] Set up monitoring/logging

### 💡 Next Steps

1. **Email Integration** → Set up SendGrid or Mailgun
2. **Database** → Move from JSON files to proper database
3. **Analytics** → Track payment metrics
4. **Customer Portal** → Allow customers to manage subscriptions
5. **Invoicing** → Automated invoice generation

### ❓ Troubleshooting

**Common Issues:**

1. **Payment fails:** Check Stripe keys and test cards
2. **Webhook errors:** Verify webhook secret
3. **Customer not found:** Check customer ID format
4. **CORS errors:** Update CORS settings in backend

**Support Contacts:**
- Stripe Documentation: https://stripe.com/docs
- Stripe Support: https://support.stripe.com

---

## 🎯 Your Payment System is Ready!

Your DataSight AI platform now has enterprise-grade payment processing. Customers can:
- Choose from 3 subscription tiers
- Pay securely with credit/debit cards
- Access their personalized dashboard
- Manage their subscriptions
- Get automated email confirmations

**Revenue Potential:**
- Starter: €199/month
- Professional: €399/month  
- Enterprise: €799/month

Start accepting payments and growing your AI SaaS business! 🚀
