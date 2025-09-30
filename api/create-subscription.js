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

    const { payment_method_id, customer_data } = req.body || {};
    if (!payment_method_id || !customer_data || !customer_data.email || !customer_data.plan) {
      return res.status(400).json({ error: 'payment_method_id, customer_data.email and customer_data.plan required' });
    }

    // Map simple plan names to price IDs from env
    const planToPriceId = {
      starter: process.env.STRIPE_PRICE_ID_STARTER,
      professional: process.env.STRIPE_PRICE_ID_PROFESSIONAL,
      enterprise: process.env.STRIPE_PRICE_ID_ENTERPRISE
    };
    const priceId = planToPriceId[customer_data.plan];
    if (!priceId) {
      return res.status(400).json({ error: 'Invalid plan' });
    }

    // Find or create customer
    const existing = await stripe.customers.list({ email: customer_data.email, limit: 1 });
    const customer = existing.data[0] || await stripe.customers.create({
      email: customer_data.email,
      name: customer_data.name,
      metadata: { company: customer_data.company || '' }
    });

    // Attach PM and set default
    await stripe.paymentMethods.attach(payment_method_id, { customer: customer.id });
    await stripe.customers.update(customer.id, {
      invoice_settings: { default_payment_method: payment_method_id }
    });

    const subscription = await stripe.subscriptions.create({
      customer: customer.id,
      items: [{ price: priceId }],
      expand: ['latest_invoice.payment_intent']
    });

    res.status(200).json({
      success: true,
      customer_id: customer.id,
      subscription_id: subscription.id,
      requires_action: subscription.latest_invoice.payment_intent.status === 'requires_action',
      payment_intent_client_secret: subscription.latest_invoice.payment_intent.client_secret
    });
  } catch (err) {
    console.error('subscription error', err);
    res.status(500).json({ error: err.message || 'Internal error' });
  }
};

