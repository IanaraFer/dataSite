exports.handler = async () => {
  const present = (v) => typeof v === 'string' && v.trim() !== '';
  const smtpUser = process.env.SMTP_USER || process.env.EMAIL_USER;
  const smtpPass = process.env.SMTP_PASS || process.env.EMAIL_PASS;
  const smtpHost = process.env.SMTP_HOST;
  const smtpPort = process.env.SMTP_PORT;

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
    body: JSON.stringify({
      SMTP_USER: present(smtpUser),
      SMTP_PASS: present(smtpPass),
      SMTP_HOST: smtpHost || null,
      SMTP_PORT: smtpPort || null
    })
  };
};

