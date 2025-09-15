const nodemailer = require('nodemailer');

exports.handler = async function(event) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const {
      toEmail,
      company,
      industry,
      overallScore,
      growthScore,
      efficiencyScore,
      riskScore,
      keyInsights,
      recommendations,
      opportunities
    } = JSON.parse(event.body || '{}');

    if (!toEmail || !company) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Missing toEmail or company' }) };
    }

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

    const subject = `Your Business Analysis Report - ${company}`;
    const text = `Business Analysis Report\n\nCompany: ${company}\nIndustry: ${industry}\n\nScores:\n- Overall: ${overallScore}\n- Growth: ${growthScore}\n- Efficiency: ${efficiencyScore}\n- Risk: ${riskScore}\n\nKey Insights:\n${keyInsights}\n\nRecommendations:\n${recommendations}\n\nGrowth Opportunities:\n${opportunities}`;

    const html = `
      <div style="font-family: Arial, sans-serif; line-height: 1.5;">
        <h2>Business Analysis Report</h2>
        <p><strong>Company:</strong> ${company}</p>
        <p><strong>Industry:</strong> ${industry}</p>
        <h3>Scores</h3>
        <ul>
          <li><strong>Overall:</strong> ${overallScore}</li>
          <li><strong>Growth:</strong> ${growthScore}</li>
          <li><strong>Efficiency:</strong> ${efficiencyScore}</li>
          <li><strong>Risk:</strong> ${riskScore}</li>
        </ul>
        <h3>Key Insights</h3>
        <pre style="white-space: pre-wrap;">${keyInsights}</pre>
        <h3>Recommendations</h3>
        <pre style="white-space: pre-wrap;">${recommendations}</pre>
        <h3>Growth Opportunities</h3>
        <pre style="white-space: pre-wrap;">${opportunities}</pre>
        <hr />
        <p>Sent by Analytica Core AI</p>
      </div>
    `;

    // Send to the user
    await transporter.sendMail({
      from: smtpUser,
      to: toEmail,
      subject,
      text,
      html
    });

    // CC business inbox for follow-up
    const bizTo = process.env.BUSINESS_INBOX || 'information@analyticacoreai.ie';
    await transporter.sendMail({
      from: smtpUser,
      to: bizTo,
      subject: `Copy: ${subject}`,
      text: `Report sent to ${toEmail}\n\n${text}`,
    });

    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message || String(err) }) };
  }
};

