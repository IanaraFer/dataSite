// Netlify Function: Stripe webhook
// Set endpoint at /api/stripe-webhook
// Requires env STRIPE_WEBHOOK_SECRET

const Stripe = require('stripe');

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || '', {
  apiVersion: '2024-06-20',
});

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method not allowed' };
  }

  const sig = event.headers['stripe-signature'];
  if (!process.env.STRIPE_WEBHOOK_SECRET) {
    console.warn('Missing STRIPE_WEBHOOK_SECRET');
    return { statusCode: 500, body: 'Webhook not configured' };
  }

  let evt;
  try {
    evt = stripe.webhooks.constructEvent(event.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    console.error('Webhook signature verification failed.', err.message);
    return { statusCode: 400, body: `Webhook Error: ${err.message}` };
  }

  try {
    switch (evt.type) {
      case 'checkout.session.completed': {
        const session = evt.data.object;
        console.log('Checkout completed', session.id, session.customer_email, session.metadata);
        break;
      }
      case 'invoice.payment_succeeded':
      case 'customer.subscription.created':
      case 'customer.subscription.updated':
      case 'customer.subscription.deleted': {
        console.log('Subscription event', evt.type);
        break;
      }
      default:
        console.log(`Unhandled event type ${evt.type}`);
    }
    return { statusCode: 200, body: JSON.stringify({ received: true }) };
  } catch (err) {
    console.error('Webhook handler error', err);
    return { statusCode: 500, body: 'Webhook handler error' };
  }
};

