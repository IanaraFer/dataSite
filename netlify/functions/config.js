exports.handler = async () => {
  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
    body: JSON.stringify({ publishableKey: process.env.STRIPE_PUBLISHABLE_KEY || '' })
  };
};

