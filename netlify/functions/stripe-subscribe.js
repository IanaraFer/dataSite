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

  const data = JSON.parse(event.body);
  const { plan, email } = data;

  // Map plan name to Stripe price ID
  const priceIds = {
    'Starter Plan': 'price_1S2Ne8EPS0ev8tkiBKZzV4pS',
    'Professional Plan': 'price_1S2NfWEPS0ev8tkiwao10uJ0',
    'Enterprise Plan': 'price_1S2NgSEPS0ev8tkiRuu9Xbtb'
  };
  const priceId = priceIds[plan] || priceIds['Starter Plan'];

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [{ price: priceId, quantity: 1 }],
      mode: 'subscription',
      customer_email: email,
      success_url: 'https://analyticacoreai.netlify.app/success.html',
      cancel_url: 'https://analyticacoreai.netlify.app/pricing.html'
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
