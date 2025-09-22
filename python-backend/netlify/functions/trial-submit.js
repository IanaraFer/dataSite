const AWS = require('aws-sdk');
const multipart = require('parse-multipart-data');
const nodemailer = require('nodemailer');

// Optional S3 setup (only used if AWS creds are present)
const s3 = new AWS.S3({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: process.env.AWS_REGION || 'eu-west-1'
});

// SMTP transporter (Microsoft 365)
const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST || 'smtp.office365.com',
  port: Number(process.env.SMTP_PORT) || 587,
  secure: false,
  auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
  tls: { ciphers: 'TLSv1.2' }
});

exports.handler = async (event, context) => {
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
    const contentType = event.headers['content-type'] || event.headers['Content-Type'] || '';

    let form = {};
    let filePart = null;

    if (contentType.includes('multipart/form-data')) {
      const boundary = contentType.split('boundary=')[1];
      const parts = multipart.parse(Buffer.from(event.body, 'base64'), boundary);
      for (const p of parts) {
        if (p.filename) {
          if (p.name === 'businessData' || p.name === 'file') {
            filePart = p;
          }
        } else {
          form[p.name] = p.data.toString();
        }
      }
    } else if (contentType.includes('application/json')) {
      form = JSON.parse(event.body || '{}');
    } else if (contentType.includes('application/x-www-form-urlencoded')) {
      form = Object.fromEntries(new URLSearchParams(event.body || ''));
    } else {
      // Attempt JSON as a fallback
      try { form = JSON.parse(event.body || '{}'); } catch (_) { form = {}; }
    }

    const firstName = (form.firstName || '').toString().trim();
    const lastName = (form.lastName || '').toString().trim();
    const email = (form.email || '').toString().trim();
    const phone = (form.phone || '').toString().trim();
    const company = (form.company || '').toString().trim();
    const industry = (form.industry || '').toString().trim();
    const revenue = (form.revenue || '').toString().trim();
    const challenge = (form.challenge || '').toString().trim();

    if (!firstName || !lastName || !email || !phone || !company || !industry || !revenue) {
      return { statusCode: 400, headers, body: JSON.stringify({ error: 'Missing required fields' }) };
    }

    // Optionally store file in S3
    let uploadedInfo = null;
    if (filePart && filePart.data && filePart.data.length > 0) {
      const timestamp = Date.now();
      const safeUserId = email.replace(/[^a-zA-Z0-9_.@-]/g, 'x');
      const fileName = filePart.filename || 'upload';
      const fileKey = `uploads/trials/${safeUserId}/${timestamp}-${fileName}`;

      if (process.env.AWS_ACCESS_KEY_ID && process.env.AWS_SECRET_ACCESS_KEY && (process.env.S3_BUCKET_NAME || '').length > 0) {
        const uploadParams = {
          Bucket: process.env.S3_BUCKET_NAME,
          Key: fileKey,
          Body: filePart.data,
          ContentType: filePart.type || 'application/octet-stream',
          Metadata: {
            originalName: fileName,
            uploadedAt: new Date().toISOString(),
            company
          }
        };
        const result = await s3.upload(uploadParams).promise();
        uploadedInfo = { fileKey, fileName, fileSize: filePart.data.length, url: result.Location };
      } else {
        // No S3 configured; include minimal file info
        uploadedInfo = { fileKey, fileName, fileSize: filePart.data.length };
      }
    }

    // Build email contents
    const adminHtml = `
      <h2>New Trial Form Submission</h2>
      <p><strong>Name:</strong> ${firstName} ${lastName}</p>
      <p><strong>Email:</strong> ${email}</p>
      <p><strong>Phone:</strong> ${phone}</p>
      <p><strong>Company:</strong> ${company}</p>
      <p><strong>Industry:</strong> ${industry}</p>
      <p><strong>Revenue:</strong> ${revenue}</p>
      <p><strong>Challenge:</strong> ${challenge || 'Not specified'}</p>
      ${uploadedInfo ? `<hr><p><strong>Dataset:</strong> ${uploadedInfo.fileName} (${Math.round(uploadedInfo.fileSize/1024)} KB)</p>${uploadedInfo.url ? `<p><a href="${uploadedInfo.url}">View in S3</a></p>` : ''}` : ''}
      <hr>
      <p>Submitted at: ${new Date().toLocaleString()}</p>
    `;

    const adminEmail = {
      to: 'information@analyticacoreai.ie',
      from: process.env.SMTP_USER || 'information@analyticacoreai.ie',
      subject: `New Trial Lead - ${firstName} ${lastName} (${company})`,
      html: adminHtml
    };

    const userEmailMsg = {
      to: email,
      from: process.env.SMTP_USER || 'information@analyticacoreai.ie',
      replyTo: process.env.SMTP_USER || 'information@analyticacoreai.ie',
      subject: 'We received your request — AnalyticaCore AI',
      html: `
        <h2>Thanks, ${firstName}!</h2>
        <p>We received your request and will get back to you within 24 hours.</p>
        ${uploadedInfo ? `<p>We also received your file: <strong>${uploadedInfo.fileName}</strong>.</p>` : ''}
        <p>Best regards,<br>AnalyticaCore AI Team</p>
      `
    };

    // Send both emails (do not fail the whole request if user email fails)
    try { await transporter.sendMail(adminEmail); } catch (e) { console.error('Admin email failed', e); }
    try { await transporter.sendMail(userEmailMsg); } catch (e) { console.error('User email failed', e); }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ success: true, message: 'Submission received. We will contact you shortly.' })
    };

  } catch (err) {
    console.error('trial-submit error:', err);
    return { statusCode: 500, headers, body: JSON.stringify({ error: 'Internal server error' }) };
  }
};

