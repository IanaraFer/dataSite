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

  // Price IDs from environment with aliases and safe fallbacks
  const priceIdMap = {
    starter: process.env.PRICE_ID_STARTER || process.env.STRIPE_PRICE_ID_STARTER || process.env.STARTER_PRICE_ID,
    professional: process.env.PRICE_ID_PROFESSIONAL || process.env.STRIPE_PRICE_ID_PROFESSIONAL || process.env.PROFESSIONAL_PRICE_ID,
    enterprise: process.env.PRICE_ID_ENTERPRISE || process.env.STRIPE_PRICE_ID_ENTERPRISE || process.env.ENTERPRISE_PRICE_ID,
  };

  const priceId = priceIdMap[normalizedPlan];
  if (!priceId) {
    // Optional last-resort fallbacks (only used if explicitly allowed)
    const allowFallbacks = (process.env.ALLOW_HARDCODED_PRICE_FALLBACKS || 'false').toLowerCase() === 'true';
    const fallbackMap = allowFallbacks ? {
      starter: 'price_1S2Ne8EPS0ev8tkiBKZzV4pS',
      professional: 'price_1S2NfWEPS0ev8tkiwao10uJ0',
      enterprise: 'price_1S2NgSEPS0ev8tkiRuu9Xbtb'
    } : {};
    const resolved = fallbackMap[normalizedPlan];
    if (!resolved) {
      return {
        statusCode: 500,
        body: JSON.stringify({
          error: `Missing price ID for plan '${normalizedPlan}'. Set PRICE_ID_STARTER, PRICE_ID_PROFESSIONAL, PRICE_ID_ENTERPRISE (or STRIPE_PRICE_ID_* aliases).`,
          details: {
            plan: normalizedPlan,
            expected_env_vars: ['PRICE_ID_STARTER','PRICE_ID_PROFESSIONAL','PRICE_ID_ENTERPRISE'],
            aliases: ['STRIPE_PRICE_ID_STARTER','STRIPE_PRICE_ID_PROFESSIONAL','STRIPE_PRICE_ID_ENTERPRISE','STARTER_PRICE_ID','PROFESSIONAL_PRICE_ID','ENTERPRISE_PRICE_ID']
          }
        })
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
