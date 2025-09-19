const stripeSdk = require('stripe');

exports.handler = async function(event) {
  try {
    const params = event.queryStringParameters || {};
    const planParam = (params.plan || params.tier || params.planType || 'starter').toString().toLowerCase();
    const allowCreate = (params.create || 'false').toString().toLowerCase() === 'true';

    const secret = process.env.STRIPE_SECRET_KEY || '';
    if (!secret) {
      return resp(500, { error: 'Missing STRIPE_SECRET_KEY' });
    }
    const stripe = stripeSdk(secret);
    const usingLiveKey = secret.startsWith('sk_live_');

    const plan = planParam.includes('enterprise') ? 'enterprise' : (planParam.includes('pro') ? 'professional' : 'starter');
    const envPrice = {
      starter: process.env.PRICE_ID_STARTER || process.env.STRIPE_PRICE_ID_STARTER || process.env.STARTER_PRICE_ID,
      professional: process.env.PRICE_ID_PROFESSIONAL || process.env.STRIPE_PRICE_ID_PROFESSIONAL || process.env.PROFESSIONAL_PRICE_ID,
      enterprise: process.env.PRICE_ID_ENTERPRISE || process.env.STRIPE_PRICE_ID_ENTERPRISE || process.env.ENTERPRISE_PRICE_ID,
    }[plan];
    const fallbackMap = {
      starter: 'price_1RyYmsCsG7kLS0L9IukaQMDl',
      professional: 'price_1RyYo0CsG7kLS0L9ewWXfqnf',
      enterprise: 'price_1RyYpmCsG7kLS0L9PEzBRHFE'
    };
    const priceId = envPrice || fallbackMap[plan] || null;

    const result = {
      mode: usingLiveKey ? 'live' : 'test',
      plan,
      env: {
        PRICE_ID_STARTER: !!(process.env.PRICE_ID_STARTER || process.env.STRIPE_PRICE_ID_STARTER || process.env.STARTER_PRICE_ID),
        PRICE_ID_PROFESSIONAL: !!(process.env.PRICE_ID_PROFESSIONAL || process.env.STRIPE_PRICE_ID_PROFESSIONAL || process.env.PROFESSIONAL_PRICE_ID),
        PRICE_ID_ENTERPRISE: !!(process.env.PRICE_ID_ENTERPRISE || process.env.STRIPE_PRICE_ID_ENTERPRISE || process.env.ENTERPRISE_PRICE_ID)
      },
      price_id_used: priceId,
      price_lookup: null,
      auto_created: false
    };

    if (!priceId) {
      return resp(200, { ...result, error: `No price ID resolved for plan '${plan}'` });
    }

    try {
      const price = await stripe.prices.retrieve(priceId);
      result.price_lookup = { id: price.id, active: price.active, currency: price.currency, recurring: price.recurring };
      return resp(200, result);
    } catch (err) {
      const msg = typeof err?.message === 'string' ? err.message : String(err);
      result.price_lookup = { error: msg };
      const planMeta = {
        starter: { amount: 19900, name: 'Starter Plan' },
        professional: { amount: 39900, name: 'Professional Plan' },
        enterprise: { amount: 79900, name: 'Enterprise Plan' }
      }[plan];
      if (allowCreate && usingLiveKey && msg.includes('No such price') && planMeta) {
        const created = await stripe.prices.create({
          currency: 'eur',
          unit_amount: planMeta.amount,
          recurring: { interval: 'month' },
          lookup_key: `${plan}_monthly_eur`,
          product_data: { name: `AnalyticaCore AI ${planMeta.name}` }
        });
        result.auto_created = true;
        result.price_id_used = created.id;
        result.price_lookup = { id: created.id, active: created.active, currency: created.currency, recurring: created.recurring };
        return resp(200, result);
      }
      return resp(200, result);
    }
  } catch (e) {
    return resp(500, { error: e?.message || String(e) });
  }
};

function resp(statusCode, body) {
  return {
    statusCode,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
    body: JSON.stringify(body)
  };
}

