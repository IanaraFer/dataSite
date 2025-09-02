// Netlify Function: Bank transfer request
// Sends an email to the customer confirming bank-transfer selection
// and notifies your team to follow up with invoice/bank details.
// Uses SendGrid if available; otherwise falls back to Outlook SMTP endpoint.

const sgMail = require('@sendgrid/mail');

async function sendWithSendGrid({ to, from, subject, html }) {
  if (!process.env.SENDGRID_API_KEY || !from) return false;
  try {
    sgMail.setApiKey(process.env.SENDGRID_API_KEY);
    await sgMail.send({ to, from, subject, html });
    return true;
  } catch (e) {
    console.error('SendGrid send error', e);
    return false;
  }
}

async function sendViaOutlookFallback({ to, subject, html }) {
  // Call our Outlook SMTP function as a fallback, if configured
  try {
    const res = await fetch(process.env.SITE_URL ? `${process.env.SITE_URL}/api/contact-outlook` : '/api/contact-outlook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'AnalyticaCore AI', email: 'no-reply@analyticacore.ai', message: `${subject}\n\n${html.replace(/<[^>]+>/g, '')}` })
    });
    return res.ok;
  } catch (e) {
    console.error('Outlook fallback error', e);
    return false;
  }
}

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: JSON.stringify({ error: 'Method not allowed' }) };
  }

  try {
    const body = JSON.parse(event.body || '{}');
    const name = (body.name || '').trim();
    const email = (body.email || '').trim();
    const company = (body.company || '').trim();
    const plan = (body.plan || 'professional').toLowerCase();

    if (!email) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Email is required' }) };
    }

    const adminEmail = process.env.CONTACT_TO_EMAIL || process.env.FROM_EMAIL || process.env.OUTLOOK_USER || 'analyticacoreai@outlook.com';
    const fromEmail = process.env.FROM_EMAIL || 'analyticacoreai@outlook.com';

    const customerSubject = `Bank Transfer Selected – AnalyticaCore AI ${plan.charAt(0).toUpperCase()+plan.slice(1)} Plan`;
    const adminSubject = `New Bank Transfer Request – ${plan} plan`;

    const customerHtml = `
      <div style="font-family: Arial, sans-serif;">
        <h2>Thanks, ${name || 'there'}!</h2>
        <p>You've selected <strong>Bank Transfer</strong> for the <strong>${plan}</strong> subscription.</p>
        <p>Our team will email you an invoice and bank details shortly. Once payment is received, your subscription will be activated.</p>
        <p>If you prefer to pay by card instead, you can return to the checkout and choose Card payment.</p>
        <p>— AnalyticaCore AI</p>
      </div>
    `;

    const adminHtml = `
      <div style="font-family: Arial, sans-serif;">
        <h3>Bank Transfer Request</h3>
        <p><strong>Name:</strong> ${name || 'N/A'}</p>
        <p><strong>Email:</strong> ${email}</p>
        <p><strong>Company:</strong> ${company || 'N/A'}</p>
        <p><strong>Plan:</strong> ${plan}</p>
        <hr/>
        <p>Please send invoice and bank details to the customer and mark the subscription as pending payment.</p>
      </div>
    `;

    // Try SendGrid first for both emails
    const sentToCustomer = await sendWithSendGrid({ to: email, from: fromEmail, subject: customerSubject, html: customerHtml });
    const sentToAdmin = await sendWithSendGrid({ to: adminEmail, from: fromEmail, subject: adminSubject, html: adminHtml });

    // If SendGrid is not configured, fallback to Outlook function for admin notification only
    if (!sentToCustomer || !sentToAdmin) {
      await sendViaOutlookFallback({ to: adminEmail, subject: adminSubject, html: adminHtml });
    }

    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  } catch (err) {
    console.error('bank-transfer error', err);
    return { statusCode: 500, body: JSON.stringify({ error: 'Failed to register bank transfer request' }) };
  }
};

