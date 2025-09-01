// Netlify Function: Stripe Checkout for subscriptions
// Expects POST JSON: { plan: "starter|professional|enterprise", email: string, name?: string }
// Environment variables required:
// - STRIPE_SECRET_KEY
// - SITE_URL (e.g., https://analyticacoreai.netlify.app or custom domain)
// Optional price IDs (preferred for subscriptions):
// - STRIPE_PRICE_STARTER
// - STRIPE_PRICE_PROFESSIONAL
// - STRIPE_PRICE_ENTERPRISE

const Stripe = require('stripe');

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || '', {
  apiVersion: '2024-06-20',
});

// Support both naming schemes: STRIPE_PRICE_* and STRIPE_PRICE_ID_*
const PLAN_TO_PRICE_ENV = {
  starter: ['STRIPE_PRICE_STARTER', 'STRIPE_PRICE_ID_STARTER'],
  professional: ['STRIPE_PRICE_PROFESSIONAL', 'STRIPE_PRICE_ID_PROFESSIONAL'],
  enterprise: ['STRIPE_PRICE_ENTERPRISE', 'STRIPE_PRICE_ID_ENTERPRISE'],
};

const PLAN_TO_AMOUNT_EUR = {
  starter: 19900,
  professional: 39900,
  enterprise: 79900,
};

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: JSON.stringify({ error: 'Method not allowed' }) };
  }

  if (!process.env.STRIPE_SECRET_KEY) {
    return { statusCode: 500, body: JSON.stringify({ error: 'Stripe not configured' }) };
  }

  try {
    const body = JSON.parse(event.body || '{}');
    const plan = (body.plan || '').toLowerCase();
    const email = body.email || '';
    const name = body.name || '';

    if (!['starter', 'professional', 'enterprise'].includes(plan)) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Invalid plan' }) };
    }
    if (!email) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Email is required' }) };
    }

    const siteUrl = process.env.SITE_URL || 'https://analyticacoreai.netlify.app';

    // Prefer static Price IDs if provided; fallback to dynamic price_data
    const priceEnvKeys = PLAN_TO_PRICE_ENV[plan] || [];
    const priceId = priceEnvKeys.map((k) => process.env[k]).find(Boolean);

    const lineItem = priceId
      ? { price: priceId, quantity: 1 }
      : {
          price_data: {
            currency: 'eur',
            product_data: {
              name: `AnalyticaCore AI - ${plan.charAt(0).toUpperCase() + plan.slice(1)} Plan`,
            },
            unit_amount: PLAN_TO_AMOUNT_EUR[plan],
            recurring: { interval: 'month' },
          },
          quantity: 1,
        };

    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      payment_method_types: ['card'],
      line_items: [lineItem],
      success_url: `${siteUrl}/success.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${siteUrl}/pricing.html`,
      customer_email: email,
      metadata: { plan, name },
      allow_promotion_codes: true,
    });

    return {
      statusCode: 200,
      body: JSON.stringify({ url: session.url, sessionId: session.id }),
    };
  } catch (err) {
    console.error('Stripe checkout error', err);
    return { statusCode: 500, body: JSON.stringify({ error: err.message || 'Checkout error' }) };
  }
};

