# AnalyticaCore AI Configuration Guide

## Required Environment Variables

### Stripe Payment Integration
1. **Create a Stripe account** at https://stripe.com
2. **Get your API keys** from the Stripe Dashboard
3. **Set environment variables** in Vercel:
   - `STRIPE_PUBLISHABLE_KEY=pk_test_...` (starts with pk_test for testing)
   - `STRIPE_SECRET_KEY=sk_test_...` (starts with sk_test for testing)
   - `STRIPE_WEBHOOK_SECRET=whsec_...` (for webhook verification)

### SendGrid Email Integration  
1. **Create a SendGrid account** at https://sendgrid.com
2. **Generate an API key** in SendGrid Settings > API Keys
3. **Set environment variables**:
   - `SENDGRID_API_KEY=SG.your_api_key_here`
   - `FROM_EMAIL=information@analyticacoreai.ie`

### Google Analytics
1. **Create a Google Analytics 4 property** at https://analytics.google.com
2. **Get your Measurement ID** (starts with G-)
3. **Replace G-XXXXXXXXXX** in all HTML files with your actual ID

## Vercel Environment Variables Setup

1. Go to your Vercel dashboard
2. Select your project (data-site-zucu)
3. Go to Settings > Environment Variables
4. Add each variable with appropriate values

## Domain Setup (.ie verification)

Your `analyticacoreai.ie` domain is pending verification. Once approved:

1. **Add domain to Vercel**:
   - Go to Project Settings > Domains
   - Add `analyticacoreai.ie` and `www.analyticacoreai.ie`

2. **Update DNS records** with your domain provider:
   - Add CNAME records pointing to Vercel

## Testing Payment Integration

1. **Use Stripe test mode** initially
2. **Test card numbers**: 4242424242424242 (Visa), 4000002500003155 (Visa Debit)
3. **Monitor webhooks** in Stripe Dashboard > Developers > Webhooks

## Email Template Customization

The current email templates include:
- Trial confirmation emails
- Welcome emails for paid subscribers
- Irish business focus and branding

## Analytics Tracking

The following events are tracked:
- Page views (all pages)
- Trial form submissions
- Payment attempts
- Successful subscriptions
- Pricing plan views

## Next Steps

1. ✅ **Set up Stripe account and keys**
2. ✅ **Configure SendGrid for emails**  
3. ✅ **Set up Google Analytics property**
4. ✅ **Add environment variables to Vercel**
5. ✅ **Test payment flow end-to-end**
6. ✅ **Connect analyticacoreai.ie domain**
7. ✅ **Monitor analytics and conversions**
