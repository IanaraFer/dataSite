const sgMail = require('@sendgrid/mail');

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
    if (!process.env.SENDGRID_API_KEY) {
      throw new Error('Missing SENDGRID_API_KEY');
    }
    sgMail.setApiKey(process.env.SENDGRID_API_KEY);

    const { name, email, company, message } = req.body || {};
    if (!name || !email || !message) {
      return res.status(400).json({ error: 'name, email, message required' });
    }

    const adminMsg = {
      to: process.env.CONTACT_TO_EMAIL || 'analyticacoreai@outlook.com',
      from: process.env.CONTACT_FROM_EMAIL || 'information@analyticacoreai.ie',
      subject: 'New Contact Form Submission',
      html: `<div><h2>Contact Form</h2><p><b>Name:</b> ${name}</p><p><b>Email:</b> ${email}</p><p><b>Company:</b> ${company || ''}</p><p><b>Message:</b></p><pre>${(message || '').toString()}</pre></div>`
    };

    const userMsg = {
      to: email,
      from: process.env.CONTACT_FROM_EMAIL || 'information@analyticacoreai.ie',
      subject: 'Thank you for contacting AnalyticaCore AI',
      html: `<div><p>Hi ${name},</p><p>We received your message and will respond within 24 hours.</p></div>`
    };

    await Promise.all([sgMail.send(adminMsg), sgMail.send(userMsg)]);
    res.status(200).json({ success: true });
  } catch (err) {
    console.error('contact error', err);
    res.status(500).json({ error: err.message || 'Internal error' });
  }
};

