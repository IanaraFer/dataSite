exports.handler = async () => {
  const present = (v) => typeof v === 'string' && v.trim() !== '';
  const smtpUser = process.env.SMTP_USER || process.env.EMAIL_USER;
  const smtpPass = process.env.SMTP_PASS || process.env.EMAIL_PASS;
  const smtpHost = process.env.SMTP_HOST;
  const smtpPort = process.env.SMTP_PORT;
  const stripeKey = process.env.STRIPE_SECRET_KEY;
  const priceStarter = process.env.PRICE_ID_STARTER || process.env.STRIPE_PRICE_ID_STARTER || process.env.STARTER_PRICE_ID;
  const pricePro = process.env.PRICE_ID_PROFESSIONAL || process.env.STRIPE_PRICE_ID_PROFESSIONAL || process.env.PROFESSIONAL_PRICE_ID;
  const priceEnt = process.env.PRICE_ID_ENTERPRISE || process.env.STRIPE_PRICE_ID_ENTERPRISE || process.env.ENTERPRISE_PRICE_ID;

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
    body: JSON.stringify({
      SMTP_USER: present(smtpUser),
      SMTP_PASS: present(smtpPass),
      SMTP_HOST: smtpHost || null,
      SMTP_PORT: smtpPort || null,
      STRIPE_SECRET_KEY: present(stripeKey),
      PRICE_ID_STARTER: present(priceStarter),
      PRICE_ID_PROFESSIONAL: present(pricePro),
      PRICE_ID_ENTERPRISE: present(priceEnt)
    })
  };
};

