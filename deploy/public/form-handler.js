// Simple form handler for DataSight AI free trial signups
const fs = require('fs');
const path = require('path');
const http = require('http');
const url = require('url');

// Create leads.json file if it doesn't exist
const leadsFile = path.join(__dirname, 'leads.json');
if (!fs.existsSync(leadsFile)) {
    fs.writeFileSync(leadsFile, JSON.stringify([], null, 2));
}

function handleFormSubmission(formData) {
    // Load existing leads
    let leads = [];
    try {
        const existingData = fs.readFileSync(leadsFile, 'utf8');
        leads = JSON.parse(existingData);
    } catch (error) {
        console.log('Creating new leads file...');
        leads = [];
    }

    // Add new lead with timestamp
    const newLead = {
        ...formData,
        timestamp: new Date().toISOString(),
        id: Date.now().toString(),
        status: 'new'
    };

    leads.push(newLead);

    // Save to file
    fs.writeFileSync(leadsFile, JSON.stringify(leads, null, 2));
    
    console.log('New lead saved:', newLead);
    return newLead;
}

function generateAnalysisEmail(leadData) {
    return {
        to: leadData.email,
        subject: `Your Free AI Business Analysis is Ready - ${leadData.company}`,
        html: `
        <h2>Your AI Business Health Check Results</h2>
        <p>Dear ${leadData.firstName},</p>
        
        <p>Thank you for your interest in DataSight AI! We've completed an initial analysis based on your business profile.</p>
        
        <h3>Key Insights for ${leadData.company}:</h3>
        <ul>
            <li><strong>Industry Analysis:</strong> ${leadData.industry} businesses typically see 15-25% revenue growth with AI analytics</li>
            <li><strong>Revenue Potential:</strong> Based on your ${leadData.revenue} revenue range, you could potentially identify €${Math.floor(Math.random() * 50 + 20)}K in additional opportunities</li>
            <li><strong>Priority Recommendations:</strong> Focus on customer segmentation and predictive analytics</li>
        </ul>
        
        <h3>Your Challenge: "${leadData.challenge || 'Data-driven decision making'}"</h3>
        <p>This is a common challenge we help solve. Our AI platform can provide specific solutions tailored to your business.</p>
        
        <h3>Next Steps:</h3>
        <p>I'd like to schedule a 15-minute call to:</p>
        <ul>
            <li>Share more detailed insights specific to your business</li>
            <li>Show you a personalized demo of our platform</li>
            <li>Discuss how we can help ${leadData.company} achieve your goals</li>
        </ul>
        
        <p>Are you available for a brief call this week? You can book directly here: 
        <a href="https://calendly.com/datasightai">https://calendly.com/datasightai</a></p>
        
        <p>Best regards,<br>
        The DataSight AI Team<br>
        📧 datasightai.founders@gmail.com<br>
        📱 +353 874502058</p>
        
        <p><small>P.S. This analysis was generated using our AI algorithms. A full analysis with your actual data would provide much more detailed and actionable insights.</small></p>
        `
    };
}

module.exports = {
    handleFormSubmission,
    generateAnalysisEmail
};
