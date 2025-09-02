// Netlify Function: Send contact email via Outlook SMTP (smtp.office365.com)
// Env vars required:
// - OUTLOOK_USER (e.g., analyticacoreai@outlook.com)
// - OUTLOOK_PASS (account password or app password if MFA)
// Optional overrides (defaults shown):
// - OUTLOOK_SMTP_HOST=smtp.office365.com
// - OUTLOOK_SMTP_PORT=587
// - OUTLOOK_FROM (defaults to OUTLOOK_USER)

const nodemailer = require('nodemailer');

function createTransport() {
  const host = process.env.OUTLOOK_SMTP_HOST || 'smtp.office365.com';
  const port = parseInt(process.env.OUTLOOK_SMTP_PORT || '587', 10);
  const user = process.env.OUTLOOK_USER;
  const pass = process.env.OUTLOOK_PASS;
  if (!user || !pass) {
    throw new Error('OUTLOOK_USER/OUTLOOK_PASS not configured');
  }
  return nodemailer.createTransport({
    host,
    port,
    secure: false, // STARTTLS
    auth: { user, pass },
    tls: { ciphers: 'TLSv1.2' }
  });
}

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: JSON.stringify({ error: 'Method not allowed' }) };
  }
  try {
    const body = JSON.parse(event.body || '{}');
    const name = body.name || 'Website Visitor';
    const email = body.email || '';
    const message = body.message || '';
    const to = body.to || process.env.CONTACT_TO_EMAIL || process.env.OUTLOOK_USER;
    const fromAddress = process.env.OUTLOOK_FROM || process.env.OUTLOOK_USER;

    if (!email || !message) {
      return { statusCode: 400, body: JSON.stringify({ error: 'email and message are required' }) };
    }

    const transporter = createTransport();

    const mailOptions = {
      from: fromAddress,
      to,
      subject: `Website enquiry from ${name}`,
      replyTo: email,
      text: message,
      html: `<div><p><strong>Name:</strong> ${name}</p><p><strong>Email:</strong> ${email}</p><p><strong>Message:</strong></p><p>${String(message).replace(/\n/g,'<br>')}</p></div>`
    };

    await transporter.sendMail(mailOptions);

    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  } catch (err) {
    console.error('Outlook SMTP error', err);
    return { statusCode: 500, body: JSON.stringify({ error: 'Failed to send message' }) };
  }
};

