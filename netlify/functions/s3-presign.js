// Netlify Function: Generate S3 pre-signed URL for client uploads
// Expects POST JSON: { filename, contentType }
// Requires env: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET_NAME

const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner');

const s3 = new S3Client({
  region: process.env.AWS_REGION || 'eu-west-1',
  credentials: process.env.AWS_ACCESS_KEY_ID && process.env.AWS_SECRET_ACCESS_KEY ? {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  } : undefined,
});

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: JSON.stringify({ error: 'Method not allowed' }) };
  }
  try {
    const body = JSON.parse(event.body || '{}');
    const filename = body.filename || `upload-${Date.now()}`;
    const contentType = body.contentType || 'application/octet-stream';
    const bucket = process.env.S3_BUCKET_NAME;
    if (!bucket) {
      return { statusCode: 500, body: JSON.stringify({ error: 'S3 not configured' }) };
    }
    const key = `uploads/${Date.now()}-${filename.replace(/[^a-zA-Z0-9._-]/g, '_')}`;
    const command = new PutObjectCommand({ Bucket: bucket, Key: key, ContentType: contentType });
    const url = await getSignedUrl(s3, command, { expiresIn: 60 * 5 }); // 5 minutes
    return { statusCode: 200, body: JSON.stringify({ url, key, bucket }) };
  } catch (err) {
    console.error('S3 presign error', err);
    return { statusCode: 500, body: JSON.stringify({ error: 'Failed to sign URL' }) };
  }
};

