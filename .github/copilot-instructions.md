<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# AI Company Data Analyzer - Copilot Instructions

## Project Overview
This is an AI-powered company data analysis platform built as a SaaS business. The application automatically analyzes company datasets and provides actionable business insights using machine learning and artificial intelligence.

## Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Backend**: FastAPI (REST API)
- **AI/ML**: pandas, scikit-learn, Prophet, XGBoost
- **Deployment**: Azure Container Apps
- **Infrastructure**: Azure Bicep templates

## Code Style Guidelines
- Use Python 3.11+ features and type hints
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Add comprehensive docstrings to all functions and classes
- Implement proper error handling with meaningful error messages
- Use logging instead of print statements for debugging

## AI/ML Best Practices
- Always validate and clean data before processing
- Use try-catch blocks around ML model operations
- Implement proper data scaling and normalization
- Add model performance metrics and validation
- Use cross-validation for model evaluation
- Cache expensive computations when possible

## Streamlit Patterns
- Use session state for data persistence
- Implement proper error handling with st.error()
- Use st.cache_data for expensive operations
- Create reusable components as functions
- Use columns and containers for better layout
- Add progress bars for long-running operations

## Azure Integration
- Use managed identity for secure authentication
- Implement proper CORS policies for container apps
- Use Azure Key Vault for sensitive configuration
- Follow Azure naming conventions for resources
- Implement proper logging and monitoring

## Business Context
- Focus on SME (Small-Medium Enterprise) use cases
- Prioritize ease of use over complex features
- Generate actionable business recommendations
- Ensure data privacy and GDPR compliance
- Design for scalability and multi-tenancy

## Feature Development Priorities
1. Data upload and validation
2. Automated data cleaning
3. Business forecasting (sales, revenue)
4. Customer segmentation
5. Anomaly detection
6. Natural language insights
7. Dashboard customization
8. Report generation and export

## Security Considerations
- Validate all user inputs
- Sanitize file uploads
- Implement rate limiting
- Use secure file handling
- Encrypt sensitive data
- Audit user actions

When working on this project, always consider the end user experience and business value of each feature.
