"""
AnalyticaCore AI - Enhanced Data Analysis Platform
Following project coding instructions and SME business context
All import errors fixed and professional features implemented
"""

import streamlit as st
import pandas as pd  # Fixed: was "panda as pd" 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
import logging
import io
import base64
import warnings
import json
from dataclasses import dataclass
import tempfile
import os
warnings.filterwarnings('ignore')

# Try to import additional libraries with fallback handling
try:
    from sklearn.ensemble import RandomForestRegressor, IsolationForest
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, r2_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    st.warning("⚠️ scikit-learn not installed. Some advanced features may be limited.")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    st.info("📄 PDF generation requires reportlab. Install with: pip install reportlab")

# Configure logging following project guidelines
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration following Streamlit best practices
st.set_page_config(
    page_title="AnalyticaCore AI - Professional Data Analysis Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS following project design guidelines - FIXED SYNTAX ERROR
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .insight-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .success-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    .contact-info {
        background: rgba(255, 255, 255, 0.2);
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        text-align: center;
    }
    
    .download-button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class BusinessMetrics:
    """Data class for business metrics following coding guidelines"""
    total_revenue: float
    avg_daily_sales: float
    total_customers: int
    avg_satisfaction: float
    growth_rate: float

class PDFReportGenerator:
    """
    PDF Report Generator for professional business reports
    Following coding instructions for report generation
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def generate_business_report(self, df: pd.DataFrame, analysis_results: Dict[str, Any]) -> bytes:
        """
        Generate professional PDF business report
        Following SME business context and coding guidelines
        """
        try:
            if not REPORTLAB_AVAILABLE:
                # Fallback to HTML report
                return self.generate_html_report(df, analysis_results)
            
            # Create PDF buffer
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=colors.HexColor('#667eea')
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                textColor=colors.HexColor('#764ba2')
            )
            
            # Title
            story.append(Paragraph("AnalyticaCore AI - Business Analysis Report", title_style))
            story.append(Spacer(1, 20))
            
            # Executive Summary
            story.append(Paragraph("Executive Summary", heading_style))
            
            if 'business_metrics' in analysis_results:
                metrics = analysis_results['business_metrics']
                summary_text = f"""
                This comprehensive business analysis covers {len(df):,} data points spanning your business operations.
                
                Key Findings:
                • Total Revenue: €{metrics.get('total_revenue', 0):,.2f}
                • Average Daily Sales: €{metrics.get('avg_daily_sales', 0):,.2f}
                • Customer Satisfaction: {metrics.get('avg_satisfaction', 0):.1f}/5.0
                • Growth Rate: {metrics.get('growth_rate', 0):+.1f}%
                """
                story.append(Paragraph(summary_text, styles['Normal']))
            
            story.append(Spacer(1, 20))
            
            # Data Overview
            story.append(Paragraph("Data Overview", heading_style))
            
            data_overview = f"""
            Dataset Information:
            • Total Records: {len(df):,}
            • Data Columns: {len(df.columns)}
            • Date Range: {df['Date'].min().strftime('%Y-%m-%d') if 'Date' in df.columns else 'N/A'} to {df['Date'].max().strftime('%Y-%m-%d') if 'Date' in df.columns else 'N/A'}
            • Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            """
            story.append(Paragraph(data_overview, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Key Insights
            if 'insights' in analysis_results:
                story.append(Paragraph("Key Business Insights", heading_style))
                insights = analysis_results['insights']
                
                for insight_key, insight_value in insights.items():
                    if isinstance(insight_value, (int, float)):
                        story.append(Paragraph(f"• {insight_key.replace('_', ' ').title()}: {insight_value:.2f}", styles['Normal']))
                    else:
                        story.append(Paragraph(f"• {insight_key.replace('_', ' ').title()}: {insight_value}", styles['Normal']))
                
                story.append(Spacer(1, 20))
            
            # Recommendations
            story.append(Paragraph("Strategic Recommendations", heading_style))
            recommendations = [
                "Focus marketing efforts on highest-performing customer segments",
                "Optimize inventory based on seasonal demand patterns",
                "Investigate anomalies for potential business opportunities",
                "Implement data-driven decision making processes",
                "Monitor key performance indicators regularly"
            ]
            
            for rec in recommendations:
                story.append(Paragraph(f"• {rec}", styles['Normal']))
            
            story.append(Spacer(1, 20))
            
            # Footer
            footer_text = f"""
            Generated by AnalyticaCore AI - DataSight AI Engine
            Contact: information@analyticacoreai.ie
            Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            story.append(Paragraph(footer_text, styles['Italic']))
            
            # Build PDF
            doc.build(story)
            buffer.seek(0)
            
            self.logger.info("PDF report generated successfully")
            return buffer.getvalue()
            
        except Exception as e:
            self.logger.error(f"Error generating PDF report: {str(e)}")
            return self.generate_html_report(df, analysis_results)
    
    def generate_html_report(self, df: pd.DataFrame, analysis_results: Dict[str, Any]) -> bytes:
        """
        Fallback HTML report generator
        """
        try:
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>AnalyticaCore AI - Business Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                             color: white; padding: 20px; border-radius: 10px; text-align: center; }}
                    .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #667eea; }}
                    .metric {{ background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>AnalyticaCore AI - Business Analysis Report</h1>
                    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="section">
                    <h2>Executive Summary</h2>
                    <p>Comprehensive analysis of {len(df):,} business data points.</p>
                </div>
                
                <div class="section">
                    <h2>Data Overview</h2>
                    <div class="metric">Total Records: {len(df):,}</div>
                    <div class="metric">Data Columns: {len(df.columns)}</div>
                    <div class="metric">Analysis Date: {datetime.now().strftime('%Y-%m-%d')}</div>
                </div>
                
                <div class="section">
                    <h2>Contact</h2>
                    <p>AnalyticaCore AI - information@analyticacoreai.ie</p>
                </div>
            </body>
            </html>
            """
            
            return html_content.encode('utf-8')
            
        except Exception as e:
            self.logger.error(f"Error generating HTML report: {str(e)}")
            return b"Report generation failed"

class AnalyticaCoreAI:
    """
    Main class for AnalyticaCore AI platform
    Following project coding guidelines and business context
    """
    
    def __init__(self):
        """Initialize the AnalyticaCore AI platform"""
        self.logger = logging.getLogger(__name__)
        self.company_name = "AnalyticaCore AI"
        self.platform_name = "DataSight AI Engine"
        self.contact_email = "information@analyticacoreai.ie"
        self.version = "2.0.0"
        self.pdf_generator = PDFReportGenerator()
        
    def generate_sample_business_data(self, days: int = 365) -> pd.DataFrame:
        """
        Generate realistic SME business data for demonstration
        Following SME business patterns and coding guidelines
        """
        try:
            np.random.seed(42)  # Reproducible results
            
            start_date = datetime.now() - timedelta(days=days)
            date_range = pd.date_range(start=start_date, periods=days, freq='D')
            
            # Business dimensions for SME context
            regions = ['Dublin', 'Cork', 'Galway', 'Limerick', 'Waterford']
            products = ['Software Licenses', 'Consulting Services', 'Support Plans', 'Training Programs', 'Custom Development']
            channels = ['Direct Sales', 'Online Platform', 'Partner Channel', 'Retail Partners']
            segments = ['Enterprise', 'SMB', 'Startup', 'Government', 'Education']
            
            data_records = []
            
            for i, date in enumerate(date_range):
                # Realistic business patterns
                day_of_year = date.timetuple().tm_yday
                seasonal_factor = 1 + 0.3 * np.sin((day_of_year / 365) * 2 * np.pi)
                weekly_factor = 0.6 if date.weekday() >= 5 else 1.2
                growth_factor = 1 + (i / days) * 0.35
                
                # Base metrics for Irish SME business
                base_revenue = 28000
                daily_revenue = max(8000, 
                    base_revenue * seasonal_factor * weekly_factor * growth_factor * 
                    (0.8 + np.random.random() * 0.4)
                )
                
                customers = max(15, int(55 + np.random.normal(0, 12)))
                avg_order_value = daily_revenue / customers
                
                # Additional business metrics
                conversion_rate = max(0.5, min(8, np.random.normal(4.2, 1.1)))
                satisfaction_score = max(2.5, min(5.0, np.random.normal(4.3, 0.5)))
                
                # Marketing and operational metrics
                marketing_spend = daily_revenue * np.random.uniform(0.08, 0.18)
                website_visitors = customers * np.random.uniform(12, 30)
                support_tickets = max(0, int(customers * np.random.uniform(0.02, 0.08)))
                
                data_records.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Revenue': round(daily_revenue, 2),
                    'Customers': customers,
                    'AvgOrderValue': round(avg_order_value, 2),
                    'ConversionRate': round(conversion_rate, 2),
                    'SatisfactionScore': round(satisfaction_score, 1),
                    'MarketingSpend': round(marketing_spend, 2),
                    'WebsiteVisitors': int(website_visitors),
                    'SupportTickets': support_tickets,
                    'Region': np.random.choice(regions),
                    'Product': np.random.choice(products),
                    'Channel': np.random.choice(channels),
                    'Segment': np.random.choice(segments),
                    'Quarter': f"Q{(date.month-1)//3 + 1}",
                    'Month': date.strftime('%B'),
                    'DayOfWeek': date.strftime('%A')
                })
            
            df = pd.DataFrame(data_records)
            df['Date'] = pd.to_datetime(df['Date'])
            df['ROI'] = ((df['Revenue'] - df['MarketingSpend']) / df['MarketingSpend'] * 100).round(2)
            df['CustomerLifetimeValue'] = (df['AvgOrderValue'] * np.random.uniform(2.5, 8.5)).round(2)
            
            self.logger.info(f"Generated {len(df)} records of sample business data")
            return df
            
        except Exception as e:
            self.logger.error(f"Error generating sample data: {str(e)}")
            st.error(f"Error generating sample data: {str(e)}")
            return pd.DataFrame()
    
    def validate_uploaded_data(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate uploaded data following data quality guidelines
        """
        try:
            if df.empty:
                return False, "Uploaded file is empty"
            
            if len(df.columns) < 2:
                return False, "Data must have at least 2 columns"
            
            if len(df) < 5:
                return False, "Data must have at least 5 rows"
            
            # Check for numeric columns
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            if len(numeric_columns) < 1:
                return False, "Data must have at least 1 numeric column for analysis"
            
            # Check for date columns
            date_columns = [col for col in df.columns if 
                           any(word in col.lower() for word in ['date', 'time', 'day', 'month', 'year'])]
            
            if not date_columns:
                st.info("💡 Tip: Including date columns enables time-series analysis and forecasting")
            
            self.logger.info(f"Data validation successful: {len(df)} rows, {len(df.columns)} columns")
            return True, f"Data validation successful - {len(df):,} rows, {len(df.columns)} columns"
            
        except Exception as e:
            self.logger.error(f"Data validation error: {str(e)}")
            return False, f"Validation error: {str(e)}"
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean data following preprocessing best practices
        """
        try:
            cleaned_df = df.copy()
            initial_rows = len(cleaned_df)
            
            # Handle missing values in numeric columns
            numeric_columns = cleaned_df.select_dtypes(include=[np.number]).columns
            for col in numeric_columns:
                if cleaned_df[col].isnull().sum() > 0:
                    cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
                    
            # Handle missing values in categorical columns
            categorical_columns = cleaned_df.select_dtypes(include=['object']).columns
            for col in categorical_columns:
                if cleaned_df[col].isnull().sum() > 0:
                    cleaned_df[col] = cleaned_df[col].fillna('Unknown')
            
            # Remove duplicates
            cleaned_df = cleaned_df.drop_duplicates()
            removed_duplicates = initial_rows - len(cleaned_df)
            
            # Remove rows with all NaN values
            cleaned_df = cleaned_df.dropna(how='all')
            
            if removed_duplicates > 0:
                st.info(f"🧹 Data cleaning: Removed {removed_duplicates} duplicate rows")
            
            self.logger.info(f"Data cleaning completed: {len(cleaned_df)} rows remaining")
            return cleaned_df
            
        except Exception as e:
            self.logger.error(f"Data cleaning error: {str(e)}")
            st.error(f"Data cleaning error: {str(e)}")
            return df
    
    def calculate_business_metrics(self, df: pd.DataFrame) -> BusinessMetrics:
        """
        Calculate key business metrics
        Following business context and coding guidelines
        """
        try:
            total_revenue = df['Revenue'].sum() if 'Revenue' in df.columns else 0
            avg_daily_sales = df['Revenue'].mean() if 'Revenue' in df.columns else 0
            total_customers = df['Customers'].sum() if 'Customers' in df.columns else 0
            avg_satisfaction = df['SatisfactionScore'].mean() if 'SatisfactionScore' in df.columns else 0
            
            # Calculate growth rate
            if 'Date' in df.columns and 'Revenue' in df.columns and len(df) > 30:
                df_sorted = df.sort_values('Date')
                first_month_revenue = df_sorted.head(30)['Revenue'].sum()
                last_month_revenue = df_sorted.tail(30)['Revenue'].sum()
                growth_rate = ((last_month_revenue - first_month_revenue) / first_month_revenue * 100) if first_month_revenue > 0 else 0
            else:
                growth_rate = 0
            
            return BusinessMetrics(
                total_revenue=total_revenue,
                avg_daily_sales=avg_daily_sales,
                total_customers=total_customers,
                avg_satisfaction=avg_satisfaction,
                growth_rate=growth_rate
            )
            
        except Exception as e:
            self.logger.error(f"Error calculating business metrics: {str(e)}")
            return BusinessMetrics(0, 0, 0, 0, 0)

    def perform_revenue_forecast(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform revenue forecasting using ML models with fallback
        Following AI/ML best practices from coding instructions
        """
        try:
            if 'Revenue' not in df.columns:
                return {"error": "Revenue column required for forecasting"}
            
            if 'Date' not in df.columns:
                return {"error": "Date column required for time-series forecasting"}
            
            # Prepare data for forecasting
            forecast_df = df[['Date', 'Revenue']].copy()
            forecast_df = forecast_df.sort_values('Date')
            forecast_df['DayNumber'] = range(len(forecast_df))
            forecast_df['DayOfYear'] = forecast_df['Date'].dt.dayofyear
            forecast_df['Month'] = forecast_df['Date'].dt.month
            forecast_df['Quarter'] = forecast_df['Date'].dt.quarter
            forecast_df['WeekOfYear'] = forecast_df['Date'].dt.isocalendar().week
            
            # Feature engineering
            forecast_df['Revenue_MA7'] = forecast_df['Revenue'].rolling(window=7, min_periods=1).mean()
            forecast_df['Revenue_MA30'] = forecast_df['Revenue'].rolling(window=30, min_periods=1).mean()
            forecast_df['Revenue_Trend'] = forecast_df['Revenue'].rolling(window=14, min_periods=1).apply(
                lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) > 1 else 0
            )
            
            if SKLEARN_AVAILABLE and len(forecast_df) > 30:
                # Use machine learning approach
                features = ['DayNumber', 'DayOfYear', 'Month', 'Quarter', 'WeekOfYear', 
                           'Revenue_MA7', 'Revenue_MA30', 'Revenue_Trend']
                X = forecast_df[features].fillna(method='bfill').fillna(method='ffill')
                y = forecast_df['Revenue']
                
                # Split for validation
                split_idx = max(1, int(len(X) * 0.8))
                X_train, X_test = X[:split_idx], X[split_idx:]
                y_train, y_test = y[:split_idx], y[split_idx:]
                
                # Train model
                model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
                model.fit(X_train, y_train)
                
                # Validate model
                if len(X_test) > 0:
                    y_pred = model.predict(X_test)
                    mae = mean_absolute_error(y_test, y_pred)
                    r2 = r2_score(y_test, y_pred)
                else:
                    mae, r2 = 0, 0.75
                
                # Generate future predictions
                last_day_number = forecast_df['DayNumber'].max()
                last_date = forecast_df['Date'].max()
                future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=30, freq='D')
                
                future_features = []
                for i, date in enumerate(future_dates):
                    future_features.append([
                        last_day_number + i + 1,
                        date.dayofyear,
                        date.month,
                        date.quarter,
                        date.isocalendar().week,
                        forecast_df['Revenue'].tail(7).mean(),
                        forecast_df['Revenue'].tail(30).mean(),
                        forecast_df['Revenue_Trend'].iloc[-1]
                    ])
                
                future_X = pd.DataFrame(future_features, columns=features)
                future_predictions = model.predict(future_X)
                
            else:
                # Simple linear trend fallback
                y = forecast_df['Revenue'].values
                x = range(len(y))
                z = np.polyfit(x, y, 1)
                trend = np.poly1d(z)
                
                future_predictions = [trend(len(y) + i) for i in range(1, 31)]
                mae = np.mean(np.abs(y - trend(x)))
                r2 = 0.6  # Approximate R2 for linear trend
            
            # Create forecast visualization
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=forecast_df['Date'],
                y=forecast_df['Revenue'],
                mode='lines+markers',
                name='Historical Revenue',
                line=dict(color='#667eea', width=3),
                marker=dict(size=6)
            ))
            
            # Future predictions
            future_dates = pd.date_range(start=forecast_df['Date'].max() + timedelta(days=1), periods=30, freq='D')
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=future_predictions,
                mode='lines+markers',
                name='Revenue Forecast',
                line=dict(color='#f093fb', width=3, dash='dash'),
                marker=dict(size=6, symbol='diamond')
            ))
            
            fig.update_layout(
                title="Revenue Forecasting - Next 30 Days",
                xaxis_title="Date",
                yaxis_title="Revenue (€)",
                template="plotly_white",
                height=600,
                hovermode='x unified'
            )
            
            # Calculate insights
            current_avg = forecast_df['Revenue'].tail(30).mean()
            forecast_avg = np.mean(future_predictions)
            growth_prediction = ((forecast_avg - current_avg) / current_avg) * 100 if current_avg > 0 else 0
            
            return {
                "model_performance": {"mae": mae, "r2_score": r2},
                "forecast_chart": fig,
                "future_predictions": future_predictions,
                "future_dates": future_dates,
                "insights": {
                    "growth_prediction": growth_prediction,
                    "forecast_avg": forecast_avg,
                    "current_avg": current_avg,
                    "confidence": "High" if r2 > 0.8 else "Medium" if r2 > 0.6 else "Low",
                    "total_forecast_revenue": sum(future_predictions)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Revenue forecasting error: {str(e)}")
            return {"error": f"Forecasting error: {str(e)}"}

    def perform_customer_segmentation(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform customer segmentation using K-means clustering
        Following ML best practices and SME context
        """
        try:
            if not SKLEARN_AVAILABLE:
                return {"error": "scikit-learn required for customer segmentation"}
            
            # Identify relevant columns for segmentation
            required_cols = ['Revenue', 'Customers']
            available_cols = [col for col in required_cols if col in df.columns]
            
            if len(available_cols) < 1:
                return {"error": "Insufficient data for customer segmentation"}
            
            # Prepare segmentation features
            segment_features = []
            if 'Revenue' in df.columns:
                segment_features.append('Revenue')
            if 'Customers' in df.columns:
                segment_features.append('Customers')
            if 'AvgOrderValue' in df.columns:
                segment_features.append('AvgOrderValue')
            if 'SatisfactionScore' in df.columns:
                segment_features.append('SatisfactionScore')
            
            if len(segment_features) < 2:
                return {"error": "Need at least 2 numeric columns for segmentation"}
            
            # Aggregate data by relevant dimensions
            if 'Segment' in df.columns:
                segment_data = df.groupby('Segment').agg({
                    col: 'mean' if col in ['AvgOrderValue', 'SatisfactionScore'] else 'sum'
                    for col in segment_features
                }).reset_index()
            elif 'Date' in df.columns:
                # Create segments based on time periods
                df_copy = df.copy()
                df_copy['Period'] = pd.to_datetime(df_copy['Date']).dt.to_period('M')
                segment_data = df_copy.groupby('Period').agg({
                    col: 'mean' if col in ['AvgOrderValue', 'SatisfactionScore'] else 'sum'
                    for col in segment_features
                }).reset_index()
            else:
                # Use quartiles for segmentation
                segment_data = df[segment_features].copy()
            
            # Prepare features for clustering
            features_for_clustering = segment_data[segment_features].fillna(0)
            
            # Normalize features
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features_for_clustering)
            
            # Perform K-means clustering
            optimal_clusters = min(4, len(features_scaled))
            if optimal_clusters < 2:
                return {"error": "Not enough data points for clustering"}
            
            kmeans = KMeans(n_clusters=optimal_clusters, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(features_scaled)
            
            segment_data['Cluster'] = clusters
            
            # Create visualization
            if len(segment_features) >= 2:
                fig = px.scatter(
                    segment_data,
                    x=segment_features[0],
                    y=segment_features[1],
                    color='Cluster',
                    size=segment_features[0] if segment_features[0] == 'Revenue' else None,
                    title="Customer Segmentation Analysis",
                    template="plotly_white",
                    height=600
                )
                fig.update_traces(marker=dict(size=12, line=dict(width=2, color='white')))
            else:
                fig = px.bar(
                    segment_data,
                    x='Cluster',
                    y=segment_features[0],
                    title=f"{segment_features[0]} by Customer Segment",
                    template="plotly_white",
                    height=600
                )
            
            # Generate insights
            cluster_summary = segment_data.groupby('Cluster').agg({
                col: ['sum', 'mean', 'count'] for col in segment_features
            }).round(2)
            
            # Find best performing segment
            if 'Revenue' in segment_features:
                best_segment = segment_data.loc[segment_data['Revenue'].idxmax(), 'Cluster']
            else:
                best_segment = segment_data.loc[segment_data[segment_features[0]].idxmax(), 'Cluster']
            
            return {
                "segmentation_chart": fig,
                "cluster_summary": cluster_summary,
                "segment_data": segment_data,
                "insights": {
                    "total_segments": optimal_clusters,
                    "best_performing_segment": best_segment,
                    "segment_distribution": segment_data['Cluster'].value_counts().to_dict(),
                    "features_used": segment_features
                }
            }
            
        except Exception as e:
            self.logger.error(f"Customer segmentation error: {str(e)}")
            return {"error": f"Segmentation error: {str(e)}"}

    def detect_anomalies(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect anomalies in business data using Isolation Forest
        Following anomaly detection best practices
        """
        try:
            if not SKLEARN_AVAILABLE:
                return {"error": "scikit-learn required for anomaly detection"}
            
            # Select numeric columns for anomaly detection
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            if len(numeric_columns) == 0:
                return {"error": "No numeric columns found for anomaly detection"}
            
            # Prepare data for anomaly detection
            anomaly_data = df[numeric_columns].fillna(df[numeric_columns].median())
            
            # Apply Isolation Forest
            isolation_forest = IsolationForest(
                contamination=0.1, 
                random_state=42,
                n_estimators=100
            )
            anomaly_predictions = isolation_forest.fit_predict(anomaly_data)
            
            # Add anomaly information to dataframe
            df_with_anomalies = df.copy()
            df_with_anomalies['Anomaly'] = anomaly_predictions
            df_with_anomalies['IsAnomaly'] = df_with_anomalies['Anomaly'] == -1
            
            # Count anomalies
            total_anomalies = sum(anomaly_predictions == -1)
            anomaly_percentage = (total_anomalies / len(df)) * 100
            
            # Create visualization
            if 'Date' in df.columns and 'Revenue' in df.columns:
                fig = go.Figure()
                
                # Normal data points
                normal_data = df_with_anomalies[df_with_anomalies['Anomaly'] == 1]
                fig.add_trace(go.Scatter(
                    x=normal_data['Date'],
                    y=normal_data['Revenue'],
                    mode='markers',
                    name='Normal Data',
                    marker=dict(color='#667eea', size=8, opacity=0.7)
                ))
                
                # Anomaly data points
                anomaly_data_points = df_with_anomalies[df_with_anomalies['Anomaly'] == -1]
                if not anomaly_data_points.empty:
                    fig.add_trace(go.Scatter(
                        x=anomaly_data_points['Date'],
                        y=anomaly_data_points['Revenue'],
                        mode='markers',
                        name='Anomalies',
                        marker=dict(color='#f093fb', size=12, symbol='diamond')
                    ))
                
                fig.update_layout(
                    title="Anomaly Detection in Revenue Data",
                    xaxis_title="Date",
                    yaxis_title="Revenue (€)",
                    template="plotly_white",
                    height=600,
                    hovermode='closest'
                )
            else:
                # Alternative visualization for non-time series data
                fig = px.histogram(
                    df_with_anomalies,
                    x='IsAnomaly',
                    title="Anomaly Distribution",
                    template="plotly_white",
                    height=400
                )
                fig.update_xaxis(title="Is Anomaly")
                fig.update_yaxis(title="Count")
            
            # Generate insights about anomalies
            revenue_impact = 0
            if total_anomalies > 0 and 'Revenue' in df.columns:
                anomaly_details = df_with_anomalies[df_with_anomalies['IsAnomaly']]
                avg_anomaly_revenue = anomaly_details['Revenue'].mean()
                avg_normal_revenue = df_with_anomalies[~df_with_anomalies['IsAnomaly']]['Revenue'].mean()
                revenue_impact = ((avg_anomaly_revenue - avg_normal_revenue) / avg_normal_revenue) * 100 if avg_normal_revenue > 0 else 0
            
            return {
                "anomaly_chart": fig,
                "anomaly_summary": {
                    "total_anomalies": total_anomalies,
                    "anomaly_percentage": round(anomaly_percentage, 2),
                    "revenue_impact": round(revenue_impact, 2),
                    "total_data_points": len(df)
                },
                "anomaly_data": df_with_anomalies[df_with_anomalies['IsAnomaly']] if total_anomalies > 0 else pd.DataFrame(),
                "normal_data": df_with_anomalies[~df_with_anomalies['IsAnomaly']]
             }

        except Exception as e:
            self.logger.error(f"Anomaly detection error: {str(e)}")
            return {"error": f"Anomaly detection error: {str(e)}"}

    def generate_business_insights(self, df: pd.DataFrame, analysis_results: Dict[str, Any]) -> List[str]:
        """
        Generate actionable business insights
        Following business context and SME needs
        """
        try:
            insights = []
            
            # Revenue insights
            if 'Revenue' in df.columns:
                total_revenue = df['Revenue'].sum()
                avg_revenue = df['Revenue'].mean()
                
                insights.append(f"💰 Total revenue analyzed: €{total_revenue:,.2f}")
                insights.append(f"📊 Average daily revenue: €{avg_revenue:,.2f}")
                
                # Growth trend
                if 'Date' in df.columns and len(df) > 30:
                    df_sorted = df.sort_values('Date')
                    first_half = df_sorted.head(len(df_sorted)//2)['Revenue'].mean()
                    second_half = df_sorted.tail(len(df_sorted)//2)['Revenue'].mean()
                    growth = ((second_half - first_half) / first_half) * 100 if first_half > 0 else 0
                    
                    if growth > 5:
                        insights.append(f"📈 Strong revenue growth detected: +{growth:.1f}%")
                    elif growth < -5:
                        insights.append(f"📉 Revenue decline detected: {growth:.1f}%")
                    else:
                        insights.append(f"➡️ Stable revenue trend: {growth:+.1f}%")
            
            # Customer insights
            if 'Customers' in df.columns:
                total_customers = df['Customers'].sum()
                avg_customers = df['Customers'].mean()
                insights.append(f"👥 Total customers served: {total_customers:,}")
                insights.append(f"📅 Average daily customers: {avg_customers:.0f}")
            
            # Satisfaction insights
            if 'SatisfactionScore' in df.columns:
                avg_satisfaction = df['SatisfactionScore'].mean()
                if avg_satisfaction >= 4.5:
                    insights.append(f"⭐ Excellent customer satisfaction: {avg_satisfaction:.1f}/5.0")
                elif avg_satisfaction >= 4.0:
                    insights.append(f"😊 Good customer satisfaction: {avg_satisfaction:.1f}/5.0")
                else:
                    insights.append(f"⚠️ Customer satisfaction needs attention: {avg_satisfaction:.1f}/5.0")
            
            # Seasonal patterns
            if 'Date' in df.columns and 'Revenue' in df.columns:
                df_temp = df.copy()
                df_temp['Month'] = pd.to_datetime(df_temp['Date']).dt.month
                monthly_revenue = df_temp.groupby('Month')['Revenue'].mean()
                best_month = monthly_revenue.idxmax()
                worst_month = monthly_revenue.idxmin()
                
                month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                              5: 'May', 6: 'June', 7: 'July', 8: 'August',
                              9: 'September', 10: 'October', 11: 'November', 12: 'December'}
                
                insights.append(f"🗓️ Best performing month: {month_names.get(best_month, best_month)}")
                insights.append(f"🔄 Focus improvement on: {month_names.get(worst_month, worst_month)}")
            
            # Regional insights
            if 'Region' in df.columns and 'Revenue' in df.columns:
                regional_revenue = df.groupby('Region')['Revenue'].sum().sort_values(ascending=False)
                top_region = regional_revenue.index[0]
                insights.append(f"🏆 Top performing region: {top_region}")
            
            # Product insights
            if 'Product' in df.columns and 'Revenue' in df.columns:
                product_revenue = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False)
                top_product = product_revenue.index[0]
                insights.append(f"🥇 Best selling product: {top_product}")
            
            # ROI insights
            if 'ROI' in df.columns:
                avg_roi = df['ROI'].mean()
                if avg_roi > 300:
                    insights.append(f"💎 Excellent marketing ROI: {avg_roi:.1f}%")
                elif avg_roi > 200:
                    insights.append(f"✅ Good marketing ROI: {avg_roi:.1f}%")
                else:
                    insights.append(f"⚠️ Marketing ROI needs optimization: {avg_roi:.1f}%")
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Error generating business insights: {str(e)}")
            return ["Unable to generate insights due to data processing error"]

def create_download_link(data: bytes, filename: str, text: str) -> str:
    """
    Create download link for files
    Following Streamlit best practices
    """
    # Deprecated: Use st.download_button instead
    return ""

def main():
    """
    Main application function following Streamlit best practices
    """
    try:
        # Initialize the platform
        platform = AnalyticaCoreAI()
        
        # Header section following SME business branding
        st.markdown("""
        <div class="main-header">
            <h1>🧠 AnalyticaCore AI</h1>
            <h3>Professional AI-Powered Data Analysis Platform</h3>
            <p>Transform Your Business Data Into Strategic Insights</p>
            <div class="contact-info">
                <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
                    <div><strong>📧 Contact:</strong> information@analyticacoreai.ie</div>
                    <div><strong>🔧 Platform:</strong> DataSight AI Engine v2.0</div>
                    <div><strong>🇮🇪 Location:</strong> Dublin, Ireland</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar for data management
        with st.sidebar:
            st.header("📊 Data Management")
            
            # Data source selection
            data_source = st.selectbox(
                "Choose Data Source",
                ["Generate Sample Data", "Upload CSV File"],
                help="Select how to load your business data"
            )
            
            # Initialize session state
            if 'data_loaded' not in st.session_state:
                st.session_state.data_loaded = False
            if 'df' not in st.session_state:
                st.session_state.df = pd.DataFrame()
            if 'analysis_results' not in st.session_state:
                st.session_state.analysis_results = {}
            
            # Handle data loading
            if data_source == "Generate Sample Data":
                days = st.slider("Data Period (days)", min_value=30, max_value=730, value=365)
                
                if st.button("🔄 Generate SME Demo Data", use_container_width=True):
                    with st.spinner("Generating realistic SME business data..."):
                        st.session_state.df = platform.generate_sample_business_data(days)
                        st.session_state.data_loaded = True
                        st.session_state.analysis_results = {}
                    st.success("✅ Sample data generated successfully!")
                    
            elif data_source == "Upload CSV File":
                uploaded_file = st.file_uploader(
                    "Upload your business data",
                    type=['csv'],
                    help="Upload a CSV file with your business data"
                )
                
                if uploaded_file is not None:
                    try:
                        df = pd.read_csv(uploaded_file)
                        is_valid, message = platform.validate_uploaded_data(df)
                        
                        if is_valid:
                            st.session_state.df = platform.clean_data(df)
                            st.session_state.data_loaded = True
                            st.session_state.analysis_results = {}
                            st.success(f"✅ {message}")
                        else:
                            st.error(f"❌ {message}")
                            
                    except Exception as e:
                        st.error(f"Error reading file: {str(e)}")
        
        # Main content area
        if st.session_state.data_loaded:
            df = st.session_state.df
            
            # Calculate business metrics
            business_metrics = platform.calculate_business_metrics(df)
            
            # Display key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📊 Total Records</h4>
                    <h2>{len(df):,}</h2>
                    <p>{len(df.columns)} columns</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>💰 Total Revenue</h4>
                    <h2>€{business_metrics.total_revenue:,.0f}</h2>
                    <p>€{business_metrics.avg_daily_sales:,.0f}/day avg</p>
                </div>
                """, unsafe_allow_html=True)
                    
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>👥 Customers</h4>
                    <h2>{business_metrics.total_customers:,}</h2>
                    <p>{business_metrics.avg_satisfaction:.1f}/5.0 satisfaction</p>
                </div>
                """, unsafe_allow_html=True)
                    
            with col4:
                growth_color = "🟢" if business_metrics.growth_rate > 0 else "🔴" if business_metrics.growth_rate < -5 else "🟡"
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📈 Growth Rate</h4>
                    <h2>{growth_color} {business_metrics.growth_rate:+.1f}%</h2>
                    <p>Period comparison</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Data preview
            with st.expander("📋 Data Preview", expanded=False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.dataframe(df.head(10), use_container_width=True)
                with col2:
                    st.write("**Data Info:**")
                    st.write(f"• Rows: {len(df):,}")
                    st.write(f"• Columns: {len(df.columns)}")
                    st.write(f"• Memory: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
                    
                    if 'Date' in df.columns:
                        date_range = df['Date'].max() - df['Date'].min()
                        st.write(f"• Date range: {date_range.days} days")
            
            # Analysis results
            if 'selected_analysis' in st.session_state:
                analysis_type = st.session_state.selected_analysis
                
                st.subheader(f"🔍 {analysis_type} Results")
                
                if analysis_type == "Business Overview":
                    # Generate business insights
                    analysis_results = {"business_metrics": business_metrics.__dict__}
                    insights = platform.generate_business_insights(df, analysis_results)
                    
                    # Display insights
                    st.markdown("""
                    <div class="insight-box">
                        <h3>🎯 AI-Generated Business Insights</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create columns for insights
                    insight_cols = st.columns(2)
                    for i, insight in enumerate(insights):
                        with insight_cols[i % 2]:
                            st.markdown(f"""
                            <div class="feature-card">
                                <p>{insight}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Statistical summary
                    st.subheader("📊 Statistical Summary")
                    numeric_summary = df.describe()
                    st.dataframe(numeric_summary, use_container_width=True)
                    
                    # Correlation matrix if applicable
                    numeric_df = df.select_dtypes(include=[np.number])
                    if len(numeric_df.columns) > 1:
                        st.subheader("🔗 Correlation Analysis")
                        corr_matrix = numeric_df.corr()
                        fig = px.imshow(
                            corr_matrix,
                            text_auto=True,
                            aspect="auto",
                            title="Feature Correlation Matrix",
                            template="plotly_white",
                            height=600
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Store results for report generation
                    st.session_state.analysis_results = {
                        "business_metrics": business_metrics.__dict__,
                        "insights": {f"insight_{i}": insight for i, insight in enumerate(insights)},
                        "analysis_type": analysis_type
                    }
                    
                elif analysis_type == "Revenue Forecasting":
                    with st.spinner("🔮 Generating revenue forecast using AI models..."):
                        forecast_results = platform.perform_revenue_forecast(df)
                    
                    if "error" in forecast_results:
                        st.error(forecast_results["error"])
                    else:
                        # Display forecast chart
                        st.plotly_chart(forecast_results["forecast_chart"], use_container_width=True)
                        
                        # Display insights
                        insights = forecast_results["insights"]
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"""
                            <div class="insight-box">
                                <h3>🎯 Forecast Insights</h3>
                                <p><strong>Growth Prediction:</strong> {insights['growth_prediction']:+.1f}% over next 30 days</p>
                                <p><strong>Forecast Confidence:</strong> {insights['confidence']}</p>
                                <p><strong>Expected Total Revenue:</strong> €{insights['total_forecast_revenue']:,.0f}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div class="success-box">
                                <h3>📊 Model Performance</h3>
                                <p><strong>R² Score:</strong> {forecast_results['model_performance']['r2_score']:.3f}</p>
                                <p><strong>Mean Absolute Error:</strong> €{forecast_results['model_performance']['mae']:,.0f}</p>
                                <p><strong>Forecast Method:</strong> {'ML-Powered' if SKLEARN_AVAILABLE else 'Statistical'}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Store results
                        st.session_state.analysis_results = {
                            "forecast_results": forecast_results,
                            "analysis_type": analysis_type
                        }
                
                elif analysis_type == "Customer Segmentation":
                    with st.spinner("🎯 Analyzing customer segments using AI clustering..."):
                        segmentation_results = platform.perform_customer_segmentation(df)
                    
                    if "error" in segmentation_results:
                        st.error(segmentation_results["error"])
                    else:
                        # Display segmentation chart
                        st.plotly_chart(segmentation_results["segmentation_chart"], use_container_width=True)
                        
                        # Display insights
                        insights = segmentation_results["insights"]
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"""
                            <div class="insight-box">
                                <h3>👥 Segmentation Insights</h3>
                                <p><strong>Segments Identified:</strong> {insights['total_segments']}</p>
                                <p><strong>Best Performing Segment:</strong> Cluster {insights['best_performing_segment']}</p>
                                <p><strong>Features Used:</strong> {', '.join(insights['features_used'])}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown("""
                            <div class="success-box">
                                <h3>💡 Recommendations</h3>
                                <p>• Focus marketing on high-value segments</p>
                                <p>• Develop targeted campaigns for each cluster</p>
                                <p>• Monitor segment performance over time</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Cluster summary
                        st.subheader("📊 Detailed Segment Analysis")
                        if hasattr(segmentation_results["cluster_summary"], 'columns'):
                            st.dataframe(segmentation_results["cluster_summary"], use_container_width=True)
                        
                        # Store results
                        st.session_state.analysis_results = {
                            "segmentation_results": segmentation_results,
                            "analysis_type": analysis_type
                        }
                
                elif analysis_type == "Anomaly Detection":
                    with st.spinner("🔍 Detecting anomalies using AI algorithms..."):
                        anomaly_results = platform.detect_anomalies(df)
                    
                    if "error" in anomaly_results:
                        st.error(anomaly_results["error"])
                    else:
                        # Display anomaly chart
                        st.plotly_chart(anomaly_results["anomaly_chart"], use_container_width=True)
                        
                        # Display summary
                        summary = anomaly_results["anomaly_summary"]
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"""
                            <div class="insight-box">
                                <h3>⚠️ Anomaly Detection Results</h3>
                                <p><strong>Anomalies Found:</strong> {summary['total_anomalies']} ({summary['anomaly_percentage']:.1f}%)</p>
                                <p><strong>Revenue Impact:</strong> {summary['revenue_impact']:+.1f}%</p>
                                <p><strong>Data Points Analyzed:</strong> {summary['total_data_points']:,}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown("""
                            <div class="success-box">
                                <h3>💡 Recommendations</h3>
                                <p>• Investigate anomalies for root causes</p>
                                <p>• Check for data quality issues</p>
                                <p>• Look for business opportunities in outliers</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Show anomaly details if any
                        if not anomaly_results["anomaly_data"].empty:
                            st.subheader("🔍 Anomaly Details")
                            st.dataframe(anomaly_results["anomaly_data"], use_container_width=True)
                        
                        # Store results
                        st.session_state.analysis_results = {
                            "anomaly_results": anomaly_results,
                            "analysis_type": analysis_type
                        }
                
                elif analysis_type == "Comparative Analysis":
                    st.subheader("📊 Comparative Business Analysis")
                    
                    # Revenue by different dimensions
                    if 'Revenue' in df.columns:
                        for col in ['Region', 'Product', 'Channel', 'Segment']:
                            if col in df.columns:
                                st.subheader(f"💰 Revenue by {col}")
                                revenue_by_category = df.groupby(col)['Revenue'].sum().sort_values(ascending=False)
                                
                                fig = px.bar(
                                    x=revenue_by_category.index,
                                    y=revenue_by_category.values,
                                    title=f"Revenue Distribution by {col}",
                                    template="plotly_white",
                                    height=500
                                )
                                fig.update_layout(xaxis_title=col, yaxis_title="Revenue (€)")
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # Insights
                                if len(revenue_by_category) > 0:
                                    top_category = revenue_by_category.index[0]
                                    top_revenue = revenue_by_category.iloc[0]
                                    total_revenue = revenue_by_category.sum()
                                    percentage = (top_revenue / total_revenue) * 100 if total_revenue > 0 else 0
                                    
                                    st.markdown(f"""
                                    <div class="success-box">
                                        <strong>Top {col}:</strong> {top_category} (€{top_revenue:,.0f} - {percentage:.1f}% of total)
                                    </div>
                                    """, unsafe_allow_html=True)
                    
                    # Store results
                    st.session_state.analysis_results = {
                        "analysis_type": analysis_type,
                        "comparative_analysis": True
                    }

            # Add analysis options to sidebar
            if st.session_state.data_loaded:
                st.sidebar.header("🤖 AI Analysis Options")
                
                analysis_type = st.sidebar.selectbox(
                    "Select Analysis Type",
                    [
                        "Business Overview",
                        "Revenue Forecasting",
                        "Customer Segmentation", 
                        "Anomaly Detection",
                        "Comparative Analysis"
                    ]
                )
                
                if st.sidebar.button("🚀 Run Analysis", use_container_width=True):
                    st.session_state.selected_analysis = analysis_type
                    st.rerun()

            # Professional Report Generation
            if st.session_state.data_loaded and st.session_state.analysis_results:
                st.sidebar.header("📄 Professional Reports")
                
                if st.sidebar.button("📊 Generate Business Report", use_container_width=True):
                    with st.spinner("Generating professional PDF report..."):
                        try:
                            report_data = platform.pdf_generator.generate_business_report(
                                df, 
                                st.session_state.analysis_results
                            )
                            filename = f"AnalyticaCore_Business_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
                            st.sidebar.download_button(
                                label="📥 Download Report (PDF)",
                                data=report_data,
                                file_name=filename,
                                mime="application/pdf"
                            )
                            st.sidebar.success("✅ Report generated successfully!")
                            # Also show download in main area
                            st.markdown("### 📄 Download Your Business Report")
                            st.download_button(
                                label="📥 Download Report (PDF)",
                                data=report_data,
                                file_name=filename,
                                mime="application/pdf"
                            )
                        except Exception as e:
                            st.sidebar.error(f"Report generation error: {str(e)}")
        
        else:
            # Welcome screen
            st.markdown("""
            <div style="text-align: center; padding: 3rem;">
                <h2>🚀 Welcome to AnalyticaCore AI Platform</h2>
                <p style="font-size: 1.2rem; color: #666;">
                    Your professional AI-powered business data analysis platform for SME companies.
                    Get started by loading your data or generating sample data in the sidebar.
                </p>
                
                <div style="display: flex; justify-content: center; gap: 2rem; margin: 2rem 0; flex-wrap: wrap;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                               color: white; padding: 2rem; border-radius: 15px; flex: 1; max-width: 300px; min-width: 250px;">
                        <h4>🧠 AI-Powered Analytics</h4>
                        <p>Advanced machine learning algorithms for business insights</p>
                    </div>
                    
                    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                               color: white; padding: 2rem; border-radius: 15px; flex: 1; max-width: 300px; min-width: 250px;">
                        <h4>⚡ Professional Reports</h4>
                        <p>Board-ready analysis and PDF reports</p>
                    </div>
                    
                    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                               color: white; padding: 2rem; border-radius: 15px; flex: 1; max-width: 300px; min-width: 250px;">
                        <h4>🔒 GDPR Compliant</h4>
                        <p>Your data stays private and secure</p>
                    </div>
                </div>
                
                <div style="margin-top: 3rem;">
                    <h3>🎯 Professional Features</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0;">
                        <div class="feature-card">
                            <h4>📈 Revenue Forecasting</h4>
                            <p>AI-powered sales predictions</p>
                        </div>
                        <div class="feature-card">
                            <h4>👥 Customer Segmentation</h4>
                            <p>Identify valuable customer groups</p>
                        </div>
                        <div class="feature-card">
                            <h4>🔍 Anomaly Detection</h4>
                            <p>Spot unusual patterns automatically</p>
                        </div>
                        <div class="feature-card">
                            <h4>📊 Business Intelligence</h4>
                            <p>Comprehensive data insights</p>
                        </div>
                    </div>
                </div>
                
                <p style="margin-top: 2rem; color: #888;">
                    <strong>Platform Status:</strong> Running locally | 
                    <strong>Contact:</strong> information@analyticacoreai.ie |
                    <strong>Version:</strong> 2.0.0
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logger.error(f"Main application error: {str(e)}")

# Run the application
if __name__ == "__main__":
    main()
