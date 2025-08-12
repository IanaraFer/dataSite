# 🤖 AI-Powered Company Data Analyzer

> **Transform your business data into actionable insights with the power of AI**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Azure](https://img.shields.io/badge/Azure-0078D4?logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/)

## 🌟 Overview

**DataSight AI** is an intelligent business analytics platform that automatically analyzes company datasets and delivers actionable insights using advanced AI and machine learning. Built for small to medium enterprises who want enterprise-level analytics without the complexity.

### ✨ Key Features

- **🚀 Automated Analysis**: Upload data and get insights in minutes, not weeks
- **📈 Sales Forecasting**: AI-powered forecasting with 85%+ accuracy using Prophet
- **👥 Customer Segmentation**: Automatic customer grouping and behavior analysis
- **🔍 Anomaly Detection**: Real-time detection of unusual patterns and outliers
- **💡 AI Recommendations**: Natural language business recommendations
- **📊 Interactive Dashboards**: Beautiful, customizable visualizations
- **🎯 Business Intelligence**: Executive-level reports and KPI tracking

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                Frontend (Streamlit)             │
│  • Data Upload    • Dashboards    • Reports    │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│              Backend API (FastAPI)             │
│  • Data Processing    • ML Pipeline    • Auth  │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│           AI/ML Engine (Python)                │
│  • Prophet    • scikit-learn    • XGBoost     │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│          Azure Cloud Infrastructure            │
│  • Container Apps    • Storage    • Analytics  │
└─────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Azure CLI (for deployment)
- Docker (optional, for containerization)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-company-analyzer.git
cd ai-company-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open your browser** to `http://localhost:8501`

### Azure Deployment

1. **Install Azure Developer CLI**
```bash
# Windows (PowerShell)
winget install microsoft.azd

# macOS
brew tap azure/azd && brew install azd

# Linux
curl -fsSL https://aka.ms/install-azd.sh | bash
```

2. **Deploy to Azure**
```bash
azd up
```

## 📊 Usage Examples

### Sales Forecasting
```python
# Upload your sales data (CSV with date and sales columns)
# The AI will automatically:
# 1. Clean and validate your data
# 2. Apply Prophet forecasting model
# 3. Generate 90-day predictions
# 4. Provide growth insights and recommendations
```

### Customer Segmentation
```python
# Upload customer data (revenue, frequency, recency)
# The system will:
# 1. Apply K-means clustering
# 2. Identify customer segments
# 3. Generate marketing recommendations
# 4. Create segment visualizations
```

### Anomaly Detection
```python
# Any numeric column can be analyzed for anomalies
# The AI detects:
# 1. Statistical outliers using IQR method
# 2. Trend deviations
# 3. Seasonal anomalies
# 4. Business impact assessment
```

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.11+**: Main programming language
- **Streamlit**: Web application framework
- **FastAPI**: REST API backend
- **pandas**: Data manipulation and analysis
- **scikit-learn**: Machine learning algorithms

### AI/ML Libraries
- **Prophet**: Time series forecasting
- **XGBoost**: Gradient boosting for predictions
- **matplotlib/plotly**: Data visualization
- **NLTK**: Natural language processing

### Cloud & Infrastructure
- **Azure Container Apps**: Hosting platform
- **Azure Container Registry**: Container management
- **Azure Log Analytics**: Monitoring and logging
- **Azure Storage**: Data persistence

## 📁 Project Structure

```
dataSite/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container configuration
├── azure.yaml                  # Azure deployment config
├── backend/
│   └── main.py                # FastAPI backend server
├── business/
│   ├── investor-pitch.md       # Investor presentation
│   ├── marketing-plan.md       # Marketing strategy
│   └── business-model.md       # Business model canvas
├── infra/
│   ├── main.bicep             # Azure infrastructure
│   ├── main.parameters.json   # Deployment parameters
│   └── core/                  # Bicep modules
└── .github/
    └── copilot-instructions.md # Development guidelines
```

## 🔧 Configuration

### Environment Variables

```bash
# Azure Configuration
AZURE_CLIENT_ID=your-client-id
AZURE_TENANT_ID=your-tenant-id
AZURE_SUBSCRIPTION_ID=your-subscription-id

# Application Settings
STREAMLIT_SERVER_PORT=8501
PYTHONPATH=/app
```

### Azure Resources

The application creates these Azure resources:
- **Container App Environment**: Hosting environment
- **Container Registry**: Image storage
- **Log Analytics Workspace**: Monitoring
- **Managed Identity**: Secure authentication

## 📈 Business Model

### Revenue Streams
- **Starter Plan**: €29/month (SMBs)
- **Professional Plan**: €99/month (Growing businesses)
- **Enterprise Plan**: €299/month (Large organizations)
- **Professional Services**: Custom development and training

### Target Market
- Small to Medium Businesses (10-500 employees)
- Consulting firms needing analytics tools
- E-commerce companies for customer analysis
- Any business seeking data-driven insights

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Roadmap

### Phase 1 (Q1 2025) ✅
- [x] Core AI analytics engine
- [x] Streamlit web interface
- [x] Azure deployment infrastructure
- [x] Business documentation

### Phase 2 (Q2 2025)
- [ ] Advanced ML models
- [ ] Multi-tenant architecture
- [ ] API marketplace
- [ ] Mobile responsiveness

### Phase 3 (Q3 2025)
- [ ] Real-time analytics
- [ ] Industry-specific templates
- [ ] Advanced integrations
- [ ] International expansion

## 🛡️ Security & Privacy

- **GDPR Compliant**: Full data protection compliance
- **Secure Authentication**: Azure managed identity
- **Data Encryption**: At rest and in transit
- **Audit Logging**: Complete user activity tracking
- **Privacy by Design**: Minimal data collection

## 📞 Support & Contact

- **Documentation**: [docs.datasight.ai](https://docs.datasight.ai)
- **Email**: support@datasight.ai
- **LinkedIn**: [DataSight AI](https://linkedin.com/company/datasight-ai)
- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-company-analyzer/issues)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Prophet](https://facebook.github.io/prophet/) for time series forecasting
- [Azure](https://azure.microsoft.com/) for cloud infrastructure
- [scikit-learn](https://scikit-learn.org/) for machine learning tools

---

**Made with ❤️ by DataSight AI Team**

*Transforming data into decisions, one business at a time.*
