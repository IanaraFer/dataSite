const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const nodemailer = require('nodemailer');

exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { paymentMethodId, customerData, planType } = JSON.parse(event.body);

    // Plan configuration with price IDs
    const plans = {
      starter: {
        priceId: process.env.STRIPE_PRICE_ID_STARTER,
        amount: 19900, // €199 in cents
        name: 'Starter Plan'
      },
      professional: {
        priceId: process.env.STRIPE_PRICE_ID_PROFESSIONAL,
        amount: 39900, // €399 in cents
        name: 'Professional Plan'
      },
      enterprise: {
        priceId: process.env.STRIPE_PRICE_ID_ENTERPRISE,
        amount: 79900, // €799 in cents
        name: 'Enterprise Plan'
      }
    };

    const selectedPlan = plans[planType];
    if (!selectedPlan) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Invalid plan selected' })
      };
    }

    // Create or retrieve customer
    let customer;
    const existingCustomers = await stripe.customers.list({
      email: customerData.email,
      limit: 1
    });

    if (existingCustomers.data.length > 0) {
      customer = existingCustomers.data[0];
    } else {
      customer = await stripe.customers.create({
        email: customerData.email,
        name: customerData.fullName,
        phone: customerData.phone,
        address: {
          line1: customerData.address,
          city: customerData.city,
          postal_code: customerData.postalCode,
          country: customerData.country
        },
        metadata: {
          customerType: customerData.customerType,
          companyName: customerData.companyName || '',
          source: 'analyticacore_website'
        }
      });
    }

    // Attach payment method to customer
    await stripe.paymentMethods.attach(paymentMethodId, {
      customer: customer.id,
    });

    // Set as default payment method
    await stripe.customers.update(customer.id, {
      invoice_settings: {
        default_payment_method: paymentMethodId,
      },
    });

    // Create subscription
    const subscription = await stripe.subscriptions.create({
      customer: customer.id,
      items: [{ price: selectedPlan.priceId }],
      default_payment_method: paymentMethodId,
      expand: ['latest_invoice.payment_intent'],
      metadata: {
        planType: planType,
        customerType: customerData.customerType,
        companyName: customerData.companyName || ''
      }
    });

    // Send confirmation emails via SMTP
    await sendConfirmationEmails(customer, subscription, selectedPlan, customerData);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        subscriptionId: subscription.id,
        customerId: customer.id,
        clientSecret: subscription.latest_invoice.payment_intent.client_secret
      })
    };

  } catch (error) {
    console.error('Subscription creation error:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: error.message || 'Failed to create subscription'
      })
    };
  }
};

async function sendConfirmationEmails(customer, subscription, plan, customerData) {
  try {
    const transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST || 'smtp.office365.com',
      port: Number(process.env.SMTP_PORT) || 587,
      secure: false,
      auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
      tls: { ciphers: 'TLSv1.2' }
    });
    // Email to customer
    const customerEmail = {
      to: customer.email,
      from: process.env.SMTP_USER || 'information@analyticacoreai.ie',
      replyTo: process.env.SMTP_USER || 'information@analyticacoreai.ie',
      subject: 'Welcome to AnalyticaCore AI - Subscription Confirmed!',
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
          <h1 style="color: #3b82f6;">Welcome to AnalyticaCore AI!</h1>
          
          <p>Hi ${customer.name},</p>
          
          <p>Thank you for subscribing to our <strong>${plan.name}</strong>! Your subscription is now active.</p>
          
          <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3>Subscription Details:</h3>
            <p><strong>Plan:</strong> ${plan.name}</p>
            <p><strong>Amount:</strong> €${plan.amount / 100}/month</p>
            <p><strong>Subscription ID:</strong> ${subscription.id}</p>
            <p><strong>Next billing:</strong> ${new Date(subscription.current_period_end * 1000).toLocaleDateString()}</p>
          </div>
          
          <h3>What's Next?</h3>
          <ul>
            <li>Access your dashboard at: <a href="https://analyticacoreai.netlify.app/platform.html">Dashboard</a></li>
            <li>Upload your data files for AI analysis</li>
            <li>Generate powerful business insights</li>
            <li>Contact support if you need help: information@analyticacoreai.ie</li>
          </ul>
          
          <p>You can manage your subscription anytime in your account dashboard.</p>
          
          <p>Best regards,<br>The AnalyticaCore AI Team</p>
        </div>
      `
    };

    // Email to admin
    const adminEmail = {
      to: 'information@analyticacoreai.ie',
      from: process.env.SMTP_USER || 'information@analyticacoreai.ie',
      subject: `New Subscription: ${plan.name} - ${customer.email}`,
      html: `
        <h2>New Subscription Created</h2>
        <p><strong>Customer:</strong> ${customer.name} (${customer.email})</p>
        <p><strong>Plan:</strong> ${plan.name}</p>
        <p><strong>Amount:</strong> €${plan.amount / 100}/month</p>
        <p><strong>Customer Type:</strong> ${customerData.customerType}</p>
        <p><strong>Company:</strong> ${customerData.companyName || 'N/A'}</p>
        <p><strong>Subscription ID:</strong> ${subscription.id}</p>
        <p><strong>Customer ID:</strong> ${customer.id}</p>
      `
    };

    await Promise.all([
      transporter.sendMail(customerEmail),
      transporter.sendMail(adminEmail)
    ]);

  } catch (error) {
    console.error('Email sending failed:', error);
    // Don't fail the subscription if email fails
  }
}
