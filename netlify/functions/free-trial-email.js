const nodemailer = require('nodemailer');

exports.handler = async function(event, context) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const data = JSON.parse(event.body);
  const { name, email, company, message } = data;

  // Configure Microsoft 365 SMTP
  const transporter = nodemailer.createTransport({
    host: 'smtp.office365.com',
    port: 587,
    secure: false,
    auth: {
      user: process.env.EMAIL_USER || 'information@analyticacoreai.ie',
      pass: process.env.EMAIL_PASSWORD // Use environment variable in production
    }
  });

  const mailOptions = {
    from: 'information@analyticacoreai.ie',
    to: 'information@analyticacoreai.ie',
    subject: `Free Trial Request from ${name}`,
    text: `Name: ${name}\nEmail: ${email}\nCompany: ${company}\nMessage: ${message}`
  };

  try {
    await transporter.sendMail(mailOptions);
    return { statusCode: 200, body: 'Email sent successfully' };
  } catch (error) {
    return { statusCode: 500, body: 'Email failed: ' + error.message };
  }
};
