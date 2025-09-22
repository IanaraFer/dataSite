const nodemailer = require('nodemailer');

exports.handler = async () => {
  try {
    const transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST || 'smtp.office365.com',
      port: Number(process.env.SMTP_PORT) || 587,
      secure: false,
      auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
      tls: { ciphers: 'TLSv1.2' }
    });

    // Verify connection
    await transporter.verify();

    // Send a minimal test email to the SMTP_USER
    const to = process.env.SMTP_USER;
    await transporter.sendMail({
      to,
      from: to,
      subject: 'SMTP Test - AnalyticaCore AI',
      text: 'This is a test email from Netlify function using Microsoft 365 SMTP.'
    });

    return { statusCode: 200, body: JSON.stringify({ success: true, message: `Test email sent to ${to}` }) };
  } catch (e) {
    return { statusCode: 500, body: JSON.stringify({ success: false, error: e.message }) };
  }
};

