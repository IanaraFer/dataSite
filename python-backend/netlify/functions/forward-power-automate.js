// Forwards form submissions to a Power Automate HTTP Request trigger
// Set POWER_AUTOMATE_URL in Netlify env vars

exports.handler = async (event) => {
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
    const flowUrl = process.env.POWER_AUTOMATE_URL;
    if (!flowUrl) return { statusCode: 500, headers, body: JSON.stringify({ error: 'POWER_AUTOMATE_URL not set' }) };

    const contentType = event.headers['content-type'] || event.headers['Content-Type'] || '';
    let payload = {};
    if (contentType.includes('application/json')) {
      payload = JSON.parse(event.body || '{}');
    } else if (contentType.includes('application/x-www-form-urlencoded')) {
      payload = Object.fromEntries(new URLSearchParams(event.body || ''));
    } else {
      // Try JSON as a fallback
      try { payload = JSON.parse(event.body || '{}'); } catch (_) { payload = { raw: event.body || '' }; }
    }

    const resp = await fetch(flowUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const text = await resp.text();
    const ok = resp.ok;
    return { statusCode: ok ? 200 : 502, headers, body: JSON.stringify({ success: ok, flowStatus: resp.status, flowBody: text }) };
  } catch (e) {
    return { statusCode: 500, headers, body: JSON.stringify({ error: e.message }) };
  }
};

