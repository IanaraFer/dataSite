const nodemailer = require('nodemailer');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }
  try {
    const { email } = JSON.parse(event.body || '{}');
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Valid email required' }) };
    }

    const smtpUser = process.env.SMTP_USER || process.env.EMAIL_USER || process.env.SENDGRID_FROM || 'information@analyticacoreai.ie';
    const smtpPass = process.env.SMTP_PASS || process.env.EMAIL_PASS;
    const smtpHost = process.env.SMTP_HOST || 'smtp.office365.com';
    const smtpPort = parseInt(process.env.SMTP_PORT || '587', 10);
    const sendgridKey = process.env.SENDGRID_API_KEY;

    let transporter;
    let fromAddress = smtpUser;
    if (smtpPass) {
      transporter = nodemailer.createTransport({ host: smtpHost, port: smtpPort, secure: false, auth: { user: smtpUser, pass: smtpPass } });
    } else if (sendgridKey) {
      transporter = nodemailer.createTransport({ service: 'SendGrid', auth: { user: 'apikey', pass: sendgridKey } });
      fromAddress = process.env.SENDGRID_FROM;
      if (!fromAddress) {
        return { statusCode: 500, body: JSON.stringify({ error: 'SENDGRID_FROM not set. Set it to a verified sender in SendGrid.' }) };
      }
    } else {
      return { statusCode: 500, body: JSON.stringify({ error: 'Email credentials not configured' }) };
    }

    // Notify business inbox
    const businessInbox = process.env.BUSINESS_INBOX || 'information@analyticacoreai.ie';
    await transporter.sendMail({
      from: fromAddress,
      to: 'information@analyticacoreai.ie',
      subject: 'New newsletter subscriber',
      text: `Email: ${email}`,
      replyTo: email
    });

    // Send confirmation to subscriber
    await transporter.sendMail({
      from: fromAddress,
      to: email,
      subject: 'Thanks for subscribing to Analytica Core AI updates',
      text: 'Thanks for subscribing! We will send you occasional product updates and promotions. You can unsubscribe anytime by replying STOP.'
    });

    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err?.message || String(err) }) };
  }
};

