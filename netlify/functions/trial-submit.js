const nodemailer = require('nodemailer');
const parseMultipart = require('parse-multipart-data');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }
  try {
    const contentType = event.headers['content-type'] || event.headers['Content-Type'] || '';
    if (!contentType.includes('multipart/form-data')) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Content-Type must be multipart/form-data' }) };
    }
    const boundaryMatch = contentType.match(/boundary=(.*)$/);
    if (!boundaryMatch) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Missing multipart boundary' }) };
    }
    const boundary = boundaryMatch[1];
    const bodyBuffer = Buffer.from(event.body, event.isBase64Encoded ? 'base64' : 'utf-8');
    const parts = parseMultipart.parse(bodyBuffer, boundary);

    const fields = {};
    const files = [];
    for (const part of parts) {
      if (part.filename) files.push(part); else fields[part.name] = part.data.toString();
    }

    const firstName = fields.firstName || '';
    const lastName = fields.lastName || '';
    const email = fields.email || '';
    const phone = fields.phone || '';
    const company = fields.company || '';
    const industry = fields.industry || '';
    const revenue = fields.revenue || '';
    const challenge = fields.challenge || '';

    if (!firstName || !lastName || !email || !phone || !company || !industry || !revenue) {
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
    const subject = `New Free Trial Request - ${firstName} ${lastName} (${company})`;
    const text = `New Free Trial Lead\n\nName: ${firstName} ${lastName}\nEmail: ${email}\nPhone: ${phone}\nCompany: ${company}\nIndustry: ${industry}\nRevenue: ${revenue}\n\nChallenge:\n${challenge || '(not specified)'}\n`;
    const attachments = files.slice(0, 1).map(f => ({ filename: f.filename, content: Buffer.from(f.data), contentType: f.type || 'application/octet-stream' }));

    await transporter.sendMail({ from: smtpUser, to, subject, text, attachments });

    // Confirmation to requester
    await transporter.sendMail({
      from: smtpUser,
      to: email,
      subject: 'We received your free trial request',
      text: `Hi ${firstName},\n\nThanks for requesting a free AI business health check. Our team will review your details${attachments.length ? ' and your uploaded file' : ''} and send your analysis shortly.\n\nSummary:\nCompany: ${company}\nIndustry: ${industry}\nRevenue: ${revenue}\nChallenge: ${challenge || '(not specified)'}\n\nBest regards,\nAnalytica Core AI`
    });

    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message || String(err) }) };
  }
};

