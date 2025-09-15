const nodemailer = require('nodemailer');
const parseMultipart = require('parse-multipart-data');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const contentType = event.headers['content-type'] || event.headers['Content-Type'] || '';
    const isMultipart = contentType.includes('multipart/form-data');
    if (!isMultipart) {
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
      if (part.filename) {
        files.push(part);
      } else {
        if (fields[part.name]) {
          // support multi-select
          fields[part.name] = Array.isArray(fields[part.name]) ? fields[part.name] : [fields[part.name]];
          fields[part.name].push(part.data.toString());
        } else {
          fields[part.name] = part.data.toString();
        }
      }
    }

    const fullName = fields.fullName || 'Unknown';
    const email = fields.email || '';
    const company = fields.company || '';
    const message = fields.message || '';
    const analysisTypes = fields.analysisTypes || [];

    const smtpUser = process.env.SMTP_USER || process.env.EMAIL_USER || 'information@analyticacoreai.ie';
    const smtpPass = process.env.SMTP_PASS || process.env.EMAIL_PASS;
    const smtpHost = process.env.SMTP_HOST || 'smtp.office365.com';
    const smtpPort = parseInt(process.env.SMTP_PORT || '587', 10);

    if (!smtpPass) {
      return { statusCode: 500, body: JSON.stringify({ error: 'Email credentials not configured' }) };
    }

    const transporter = nodemailer.createTransport({
      host: smtpHost,
      port: smtpPort,
      secure: false,
      auth: { user: smtpUser, pass: smtpPass }
    });

    const to = 'information@analyticacoreai.ie';
    const subject = `One-Time Data Analysis Request - ${fullName}${company ? ' (' + company + ')' : ''}`;
    const text = `New One-Time Data Analysis request\n\nName: ${fullName}\nEmail: ${email}\nCompany: ${company}\nAnalysis Types: ${Array.isArray(analysisTypes) ? analysisTypes.join(', ') : analysisTypes}\n\nMessage:\n${message}`;

    const attachments = files.map(f => ({
      filename: f.filename,
      content: Buffer.from(f.data),
      contentType: f.type || 'application/octet-stream'
    }));

    await transporter.sendMail({
      from: smtpUser,
      to,
      subject,
      text,
      attachments
    });

    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message || String(err) }) };
  }
};

