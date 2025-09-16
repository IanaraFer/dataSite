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
    const sendgridKey = process.env.SENDGRID_API_KEY;

    let transporter;
    if (smtpPass) {
      transporter = nodemailer.createTransport({ host: smtpHost, port: smtpPort, secure: false, auth: { user: smtpUser, pass: smtpPass } });
    } else if (sendgridKey) {
      transporter = nodemailer.createTransport({ service: 'SendGrid', auth: { user: 'apikey', pass: sendgridKey } });
    } else {
      return { statusCode: 500, body: JSON.stringify({ error: 'Email credentials not configured' }) };
    }

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

    // Send confirmation to requester
    if (email) {
      const confirmSubject = 'We received your One-Time Data Analysis request';
      const typeList = Array.isArray(analysisTypes) ? analysisTypes.join(', ') : analysisTypes;
      const confirmText = `Hi ${fullName},\n\nThanks for your request. Our team at Analytica Core AI has received your details and will contact you shortly.\n\nSummary:\n• Name: ${fullName}\n• Email: ${email}\n• Company: ${company}\n• Analysis Types: ${typeList}\n\nYour message:\n${message || '(none)'}\n\nIf you have additional files or context, just reply to this email.\n\nBest regards,\nAnalytica Core AI`;
      await transporter.sendMail({
        from: smtpUser,
        to: email,
        subject: confirmSubject,
        text: confirmText
      });
    }

    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message || String(err) }) };
  }
};

