const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

exports.handler = async function(event, context) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  if (!process.env.STRIPE_SECRET_KEY || process.env.STRIPE_SECRET_KEY.includes('YOUR_SECRET_KEY')) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Stripe key not configured. Set STRIPE_SECRET_KEY in environment.' })
    };
  }

  const data = JSON.parse(event.body || '{}');
  // Accept multiple shapes from different frontends
  let planInput = data.plan || data.planType || data.tier || '';
  const customerEmail = data.customer_email || data.email || data.userEmail || '';

  // Normalize plan
  const normalizedPlan = String(planInput).toLowerCase().includes('enterprise')
    ? 'enterprise'
    : String(planInput).toLowerCase().includes('pro')
      ? 'professional'
      : 'starter';

  // Price IDs from environment (no hard-coded IDs)
  const priceIdMap = {
    starter: process.env.PRICE_ID_STARTER,
    professional: process.env.PRICE_ID_PROFESSIONAL,
    enterprise: process.env.PRICE_ID_ENTERPRISE,
  };

  const priceId = priceIdMap[normalizedPlan];
  if (!priceId) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: `Missing price ID for plan '${normalizedPlan}'. Set PRICE_ID_STARTER, PRICE_ID_PROFESSIONAL, PRICE_ID_ENTERPRISE in environment.` })
    };
  }

  try {
    const hostHeader = event.headers['x-forwarded-host'] || event.headers['host'] || 'analyticacoreai.netlify.app';
    const scheme = (event.headers['x-forwarded-proto'] || 'https');
    const baseUrl = `${scheme}://${hostHeader}`;

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [{ price: priceId, quantity: 1 }],
      mode: 'subscription',
      customer_email: customerEmail || undefined,
      success_url: `${baseUrl}/success.html`,
      cancel_url: `${baseUrl}/pricing.html`
    });
    return {
      statusCode: 200,
      body: JSON.stringify({ success: true, checkout_url: session.url })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
