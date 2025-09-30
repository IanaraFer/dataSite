const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY || '');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }
  try {
    if (!process.env.STRIPE_SECRET_KEY) {
      throw new Error('Missing STRIPE_SECRET_KEY');
    }

    const {
      price_data,
      success_url,
      cancel_url,
      mode = 'subscription'
    } = req.body || {};

    if (!price_data) {
      return res.status(400).json({ error: 'price_data required' });
    }

    const session = await stripe.checkout.sessions.create({
      mode,
      line_items: [{ price_data, quantity: 1 }],
      success_url: success_url || `${req.headers.origin || 'https://example.com'}/success.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: cancel_url || `${req.headers.origin || 'https://example.com'}/pricing.html`,
      payment_method_types: ['card']
    });

    res.status(200).json({ id: session.id });
  } catch (err) {
    console.error('checkout error', err);
    res.status(500).json({ error: err.message || 'Internal error' });
  }
};

