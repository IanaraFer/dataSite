const nodemailer = require('nodemailer');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }
  try {
    const { fullName, email, description } = JSON.parse(event.body || '{}');
    if (!fullName || !email || !description) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Missing required fields' }) };
    }

    const smtpUser = process.env.SMTP_USER || process.env.EMAIL_USER || 'information@analyticacoreai.ie';
    const smtpPass = process.env.SMTP_PASS || process.env.EMAIL_PASS;
    const smtpHost = process.env.SMTP_HOST || 'smtp.office365.com';
    const smtpPort = parseInt(process.env.SMTP_PORT || '587', 10);
    if (!smtpPass) {
      return { statusCode: 500, body: JSON.stringify({ error: 'Email credentials not configured' }) };
    }

    const transporter = nodemailer.createTransport({ host: smtpHost, port: smtpPort, secure: false, auth: { user: smtpUser, pass: smtpPass } });

    const to = 'information@analyticacoreai.ie';
    const subject = `Data Deletion Request - ${fullName}`;
    const text = `Name: ${fullName}\nEmail: ${email}\n\nDescription:\n${description}\n\nPlease action this request and confirm to the user.`;

    await transporter.sendMail({ from: smtpUser, to, subject, text });
    await transporter.sendMail({ from: smtpUser, to: email, subject: 'We received your data deletion request', text: `Hi ${fullName},\n\nWe received your data deletion request and will process it promptly.\n\nSummary:\n${description}\n\nYou will receive a confirmation when complete.\n\nBest regards,\nAnalytica Core AI` });

    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message || String(err) }) };
  }
};

