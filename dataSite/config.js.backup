/**
 * DataSight AI Platform Configuration
 * Following project coding instructions and business context
 */

const PLATFORM_CONFIG = {
    // Company Information - Following SME business requirements
    companyName: 'AnalyticaCore AI',
    platformName: 'DataSight AI',
    
    // Contact Information - Updated with correct email
    email: 'analyticacoreai@outlook.com',
    website: 'https://analyticacoreai.com',
    
    // Business Information - SME-focused value proposition
    tagline: 'Transform Your Business Data Into Actionable Insights',
    description: 'AI-powered company data analysis platform built for SMEs',
    
    // Feature Development Priorities (as per coding instructions)
    features: {
        dataUpload: true,
        automatedCleaning: true,
        businessForecasting: true,
        customerSegmentation: true,
        anomalyDetection: true,
        naturalLanguageInsights: true,
        dashboardCustomization: true,
        reportGeneration: true
    },
    
    // Azure Integration Settings
    azure: {
        region: 'West Europe',
        resourceGroup: 'rg-datasight-ai',
        containerApp: 'ca-datasight-platform',
        keyVault: 'kv-datasight-secrets'
    },
    
    // Security Configuration - Following security considerations
    security: {
        maxFileSize: '50MB',
        allowedFileTypes: ['.csv', '.xlsx', '.json'],
        rateLimiting: true,
        dataEncryption: true,
        auditLogging: true
    },
    
    // ML Model Configuration - Following AI/ML best practices
    models: {
        forecastAccuracy: 0.85,
        segmentationModel: 'kmeans',
        anomalyThreshold: 2.5,
        crossValidationFolds: 5
    }
};

// Email update functionality - Following secure coding practices
function updatePlatformEmail() {
    try {
        // Update all email references to correct business email
        const correctEmail = PLATFORM_CONFIG.email;
        
        // Update mailto links
        document.querySelectorAll('a[href^="mailto:"]').forEach(link => {
            link.href = `mailto:${correctEmail}`;
            if (link.textContent.includes('@')) {
                link.textContent = correctEmail;
            }
        });
        
        // Update contact forms
        document.querySelectorAll('input[type="email"]').forEach(input => {
            if (input.placeholder && input.placeholder.includes('@')) {
                input.placeholder = `Contact us at ${correctEmail}`;
            }
        });
        
        console.log(`✅ Platform email updated to ${correctEmail}`);
        return true;
        
    } catch (error) {
        console.error('❌ Error updating email configuration:', error);
        return false;
    }
}

// Export configuration - Following modular design principles
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PLATFORM_CONFIG;
}

// Auto-update on page load
document.addEventListener('DOMContentLoaded', () => {
    updatePlatformEmail();
    console.log('🚀 DataSight AI Platform configuration loaded');
});