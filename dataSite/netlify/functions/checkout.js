const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

exports.handler = async (event, context) => {
  // Enable CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers };
  }

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers, body: 'Method Not Allowed' };
  }

  try {
    const { plan } = JSON.parse(event.body);
    
    // Price mapping
    const prices = {
      'starter': process.env.STRIPE_PRICE_STARTER || 'price_1234567890starter',
      'professional': process.env.STRIPE_PRICE_PROFESSIONAL || 'price_1234567890prof', 
      'enterprise': process.env.STRIPE_PRICE_ENTERPRISE || 'price_1234567890ent'
    };

    const session = await stripe.checkout.Session.create({
      payment_method_types: ['card'],
      line_items: [{
        price: prices[plan],
        quantity: 1,
      }],
      mode: 'subscription',
      success_url: `${process.env.SITE_URL || 'https://analyticacoreai.netlify.app'}/success.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.SITE_URL || 'https://analyticacoreai.netlify.app'}/pricing.html`,
    });

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ url: session.url })
    };
  } catch (error) {
    console.error('Stripe error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message })
    };
  }
};
