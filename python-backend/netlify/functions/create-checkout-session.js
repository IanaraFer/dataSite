const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers, body: JSON.stringify({ error: 'Method not allowed' }) };
  }

  try {
    const { plan } = JSON.parse(event.body || '{}');
    const planKey = (plan || 'starter').toLowerCase();

    const priceMap = {
      starter: process.env.STRIPE_PRICE_ID_STARTER,
      professional: process.env.STRIPE_PRICE_ID_PROFESSIONAL,
      business: process.env.STRIPE_PRICE_ID_PROFESSIONAL || process.env.STRIPE_PRICE_ID_ENTERPRISE,
      enterprise: process.env.STRIPE_PRICE_ID_ENTERPRISE
    };

    const priceId = priceMap[planKey];
    if (!priceId) {
      return { statusCode: 400, headers, body: JSON.stringify({ error: 'Missing Stripe price ID for plan' }) };
    }

    const origin = (event.headers['origin'] || event.headers['Origin'] || '').replace(/\/$/, '');
    const siteBase = origin || 'https://analyticacoreai.netlify.app';

    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: `${siteBase}/working-payment.html?success=true`,
      cancel_url: `${siteBase}/working-payment.html`,
      allow_promotion_codes: true
    });

    return { statusCode: 200, headers, body: JSON.stringify({ id: session.id }) };
  } catch (e) {
    console.error('create-checkout-session error:', e);
    return { statusCode: 500, headers, body: JSON.stringify({ error: e.message || 'Server error' }) };
  }
};

