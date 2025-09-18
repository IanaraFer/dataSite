const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

exports.handler = async function(event, context) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ error: 'Method Not Allowed' }) };
  }

  if (!process.env.STRIPE_SECRET_KEY || process.env.STRIPE_SECRET_KEY.includes('YOUR_SECRET_KEY')) {
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
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

  // Mode detection (informational)
  const usingLiveKey = process.env.STRIPE_SECRET_KEY.startsWith('sk_live_');

  // Price IDs from environment with aliases
  const priceIdMap = {
    starter: process.env.PRICE_ID_STARTER || process.env.STRIPE_PRICE_ID_STARTER || process.env.STARTER_PRICE_ID,
    professional: process.env.PRICE_ID_PROFESSIONAL || process.env.STRIPE_PRICE_ID_PROFESSIONAL || process.env.PROFESSIONAL_PRICE_ID,
    enterprise: process.env.PRICE_ID_ENTERPRISE || process.env.STRIPE_PRICE_ID_ENTERPRISE || process.env.ENTERPRISE_PRICE_ID,
  };

  const priceId = priceIdMap[normalizedPlan];
  // Always allow fallback to known IDs you provided so checkout works even if env vars are unset
  const fallbackMap = {
    starter: 'price_1RyYmsCsG7kLS0L9IukaQMDl',
    professional: 'price_1RyYo0CsG7kLS0L9ewWXfqnf',
    enterprise: 'price_1RyYpmCsG7kLS0L9PEzBRHFE'
  };
  const finalPriceId = priceId || fallbackMap[normalizedPlan];
  if (!finalPriceId) {
    return {
      statusCode: 500,
      body: JSON.stringify({
        error: `Missing price ID for plan '${normalizedPlan}'. Set PRICE_ID_* env vars or verify fallback IDs.`,
        plan: normalizedPlan
      })
    };
  }

  try {
    const hostHeader = event.headers['x-forwarded-host'] || event.headers['host'] || 'analyticacoreai.netlify.app';
    const scheme = (event.headers['x-forwarded-proto'] || 'https');
    const baseUrl = `${scheme}://${hostHeader}`;
    const planMeta = {
      starter: { amount: 19900, name: 'Starter Plan' },
      professional: { amount: 39900, name: 'Professional Plan' },
      enterprise: { amount: 79900, name: 'Enterprise Plan' }
    }[normalizedPlan];

    async function createSessionWithPrice(priceId) {
      const session = await stripe.checkout.sessions.create({
        payment_method_types: ['card'],
        line_items: [{ price: priceId, quantity: 1 }],
        mode: 'subscription',
        customer_email: customerEmail || undefined,
        success_url: `${baseUrl}/success.html`,
        cancel_url: `${baseUrl}/pricing.html`
      });
      return session;
    }

    let session;
    try {
      session = await createSessionWithPrice(finalPriceId);
    } catch (err) {
      const allowAutoCreate = (process.env.AUTO_CREATE_PRICES || 'true').toLowerCase() === 'true';
      const isNoSuchPrice = typeof err?.message === 'string' && err.message.includes('No such price');
      if (usingLiveKey && allowAutoCreate && isNoSuchPrice && planMeta) {
        // Auto-create a live EUR monthly price if missing
        const price = await stripe.prices.create({
          currency: 'eur',
          unit_amount: planMeta.amount,
          recurring: { interval: 'month' },
          lookup_key: `${normalizedPlan}_monthly_eur`,
          product_data: { name: `AnalyticaCore AI ${planMeta.name}` }
        });
        session = await createSessionWithPrice(price.id);
      } else {
        throw err;
      }
    }

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
      body: JSON.stringify({ success: true, checkout_url: session.url })
    };
  } catch (error) {
    const mode = usingLiveKey ? 'live' : 'test';
    const helpful = (typeof error?.message === 'string' && error.message.includes('No such price'))
      ? `Price ID not found in ${mode} mode. Ensure the PRICE_ID for plan '${normalizedPlan}' exists in your ${mode} Stripe account.`
      : error?.message;
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
      body: JSON.stringify({
        error: helpful || 'Stripe error',
        details: {
          mode,
          plan: normalizedPlan,
          price_id_used: finalPriceId
        }
      })
    };
  }
};
