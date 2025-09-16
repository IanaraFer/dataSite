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

  // Mode detection
  const usingLiveKey = process.env.STRIPE_SECRET_KEY.startsWith('sk_live_');

  // Price IDs from environment with aliases and safe fallbacks (test only)
  const priceIdMap = {
    starter: process.env.PRICE_ID_STARTER || process.env.STRIPE_PRICE_ID_STARTER || process.env.STARTER_PRICE_ID,
    professional: process.env.PRICE_ID_PROFESSIONAL || process.env.STRIPE_PRICE_ID_PROFESSIONAL || process.env.PROFESSIONAL_PRICE_ID,
    enterprise: process.env.PRICE_ID_ENTERPRISE || process.env.STRIPE_PRICE_ID_ENTERPRISE || process.env.ENTERPRISE_PRICE_ID,
  };

  const priceId = priceIdMap[normalizedPlan];
  if (!priceId) {
    if (usingLiveKey) {
      return {
        statusCode: 500,
        body: JSON.stringify({ error: `Missing live price ID for plan '${normalizedPlan}'. Set PRICE_ID_* environment variables.` })
      };
    }
    const allowFallbacks = (process.env.ALLOW_HARDCODED_PRICE_FALLBACKS || 'false').toLowerCase() === 'true';
    const fallbackMap = allowFallbacks ? {
      starter: 'price_1RyYmsCsG7kLS0L9IukaQMDl',
      professional: 'price_1RyYo0CsG7kLS0L9ewWXfqnf',
      enterprise: 'price_1RyYpmCsG7kLS0L9PEzBRHFE'
    } : {};
    const resolved = fallbackMap[normalizedPlan];
    if (!resolved) {
      return {
        statusCode: 500,
        body: JSON.stringify({ error: `Missing test price ID for plan '${normalizedPlan}'. Provide PRICE_ID_* or enable ALLOW_HARDCODED_PRICE_FALLBACKS=true.` })
      };
    }
    priceIdMap[normalizedPlan] = resolved;
  }

  try {
    const hostHeader = event.headers['x-forwarded-host'] || event.headers['host'] || 'analyticacoreai.netlify.app';
    const scheme = (event.headers['x-forwarded-proto'] || 'https');
    const baseUrl = `${scheme}://${hostHeader}`;

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [{ price: priceIdMap[normalizedPlan], quantity: 1 }],
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
