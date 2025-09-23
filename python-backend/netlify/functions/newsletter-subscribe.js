const nodemailer = require('nodemailer');

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers, body: JSON.stringify({ error: 'Method not allowed' }) };
  }

  try {
    const transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST || 'smtp.office365.com',
      port: Number(process.env.SMTP_PORT) || 587,
      secure: false,
      auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
      tls: { ciphers: 'TLSv1.2' }
    });

    const contentType = event.headers['content-type'] || event.headers['Content-Type'] || '';
    let body = {};
    if (contentType.includes('application/json')) {
      body = JSON.parse(event.body || '{}');
    } else if (contentType.includes('application/x-www-form-urlencoded')) {
      body = Object.fromEntries(new URLSearchParams(event.body || ''));
    } else {
      try { body = JSON.parse(event.body || '{}'); } catch (_) { body = {}; }
    }

    const email = String(body.email || '').trim();
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return { statusCode: 400, headers, body: JSON.stringify({ error: 'Invalid email' }) };
    }

    const adminTo = 'information@analyticacoreai.ie';
    // Notify admin
    await transporter.sendMail({
      to: adminTo,
      from: process.env.SMTP_USER || adminTo,
      subject: `New newsletter subscriber: ${email}`,
      html: `<p>New newsletter signup:</p><p><strong>${email}</strong></p><p>Time: ${new Date().toISOString()}</p>`
    });

    // Optional confirmation to user
    try {
      await transporter.sendMail({
        to: email,
        from: process.env.SMTP_USER || adminTo,
        subject: 'Thanks for subscribing — AnalyticaCore AI',
        html: `<p>Thanks for subscribing to AnalyticaCore AI promotions and updates.</p><p>You can unsubscribe anytime.</p>`
      });
    } catch (e) {
      // Do not fail on user confirmation email
    }

    return { statusCode: 200, headers, body: JSON.stringify({ success: true }) };
  } catch (e) {
    return { statusCode: 500, headers, body: JSON.stringify({ error: e.message }) };
  }
};

