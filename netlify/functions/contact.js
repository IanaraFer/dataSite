// Netlify Function: Contact form via SendGrid
// Expects POST JSON: { name, email, message }
// Requires env: SENDGRID_API_KEY, CONTACT_TO_EMAIL (destination), FROM_EMAIL (verified sender)

const sgMail = require('@sendgrid/mail');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: JSON.stringify({ error: 'Method not allowed' }) };
  }

  if (!process.env.SENDGRID_API_KEY || !process.env.CONTACT_TO_EMAIL || !process.env.FROM_EMAIL) {
    return { statusCode: 500, body: JSON.stringify({ error: 'Email not configured' }) };
  }

  try {
    const body = JSON.parse(event.body || '{}');
    const name = body.name || 'Visitor';
    const email = body.email || '';
    const message = body.message || '';
    if (!email || !message) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Email and message are required' }) };
    }

    sgMail.setApiKey(process.env.SENDGRID_API_KEY);

    const msg = {
      to: process.env.CONTACT_TO_EMAIL,
      from: { email: process.env.FROM_EMAIL, name: 'AnalyticaCore AI Website' },
      replyTo: email,
      subject: `Website contact from ${name}`,
      html: `
        <div>
          <h3>New website enquiry</h3>
          <p><strong>Name:</strong> ${name}</p>
          <p><strong>Email:</strong> ${email}</p>
          <p><strong>Message:</strong></p>
          <p>${(message || '').replace(/\n/g, '<br>')}</p>
        </div>
      `,
    };

    await sgMail.send(msg);
    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  } catch (err) {
    console.error('Contact email error', err);
    return { statusCode: 500, body: JSON.stringify({ error: 'Failed to send message' }) };
  }
};

