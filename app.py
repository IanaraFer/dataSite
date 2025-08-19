"""
AnalyticaCore AI - Advanced Data Analysis Platform
Following project coding instructions and SME business context
AI-powered company data analysis platform for SMEs
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
import logging
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Configure logging following project guidelines
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration following SME business context
st.set_page_config(
    page_title="AnalyticaCore AI - Data Analysis Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS following project design guidelines
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

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
        self.contact_email = "founder@analyticacoreai.com"
        
    def generate_sample_business_data(self, days: int = 365) -> pd.DataFrame:
        """
        Generate realistic SME business data for demonstration
        Following SME business patterns and use cases
        """
        try:
            np.random.seed(42)  # For reproducible results
            
            # SME business parameters following project context
            start_date = datetime.now() - timedelta(days=days)
            date_range = pd.date_range(start=start_date, periods=days, freq='D')
            
            # Business dimensions for SME context
            regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
            products = ['Software Licenses', 'Consulting Services', 'Support Plans', 'Training Programs']
            channels = ['Direct Sales', 'Online Platform', 'Partner Channel', 'Retail Partners']
            segments = ['Enterprise', 'SMB', 'Startup', 'Government']
            
            data_records = []
            
            for i, date in enumerate(date_range):
                # Business patterns following SME analytics
                day_of_year = date.timetuple().tm_yday
                seasonal_factor = 1 + 0.3 * np.sin((day_of_year / 365) * 2 * np.pi)
                weekly_factor = 0.7 if date.weekday() >= 5 else 1.2
                growth_factor = 1 + (i / days) * 0.25
                
                # Base metrics for SME business
                base_revenue = 25000
                daily_revenue = max(8000, 
                    base_revenue * seasonal_factor * weekly_factor * growth_factor * 
                    (0.8 + np.random.random() * 0.4)
                )
                
                customers = max(25, int(60 + np.random.normal(0, 15)))
                avg_order_value = daily_revenue / customers
                
                # Additional business metrics
                conversion_rate = max(1, min(8, np.random.normal(4.5, 1.2)))
                satisfaction_score = max(3.0, min(5.0, np.random.normal(4.2, 0.6)))
                
                # Marketing metrics
                marketing_spend = daily_revenue * np.random.uniform(0.08, 0.15)
                website_visitors = customers * np.random.uniform(8, 25)
                
                data_records.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Revenue': round(daily_revenue, 2),
                    'Customers': customers,
                    'AvgOrderValue': round(avg_order_value, 2),
                    'ConversionRate': round(conversion_rate, 2),
                    'SatisfactionScore': round(satisfaction_score, 1),
                    'MarketingSpend': round(marketing_spend, 2),
                    'WebsiteVisitors': int(website_visitors),
                    'Region': np.random.choice(regions),
                    'Product': np.random.choice(products),
                    'Channel': np.random.choice(channels),
                    'Segment': np.random.choice(segments),
                    'Quarter': f"Q{(date.month-1)//3 + 1}"
                })
            
            df = pd.DataFrame(data_records)
            df['Date'] = pd.to_datetime(df['Date'])
            df['ROI'] = ((df['Revenue'] - df['MarketingSpend']) / df['MarketingSpend'] * 100).round(2)
            
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
            
            if len(df.columns) < 3:
                return False, "Data must have at least 3 columns"
            
            if len(df) < 10:
                return False, "Data must have at least 10 rows"
            
            # Check for date column
            date_columns = [col for col in df.columns if 
                           any(word in col.lower() for word in ['date', 'time', 'day', 'month', 'year'])]
            
            if not date_columns:
                st.warning("No date column detected. Some time-series analyses may be limited.")
            
            # Check for numeric columns
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            if len(numeric_columns) < 2:
                return False, "Data must have at least 2 numeric columns for analysis"
            
            self.logger.info(f"Data validation successful: {len(df)} rows, {len(df.columns)} columns")
            return True, "Data validation successful"
            
        except Exception as e:
            self.logger.error(f"Data validation error: {str(e)}")
            return False, f"Validation error: {str(e)}"
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean data following data preprocessing best practices
        """
        try:
            cleaned_df = df.copy()
            
            # Handle missing values
            numeric_columns = cleaned_df.select_dtypes(include=[np.number]).columns
            for col in numeric_columns:
                cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
            
            # Handle categorical missing values
            categorical_columns = cleaned_df.select_dtypes(include=['object']).columns
            for col in categorical_columns:
                cleaned_df[col] = cleaned_df[col].fillna('Unknown')
            
            # Remove duplicates
            initial_rows = len(cleaned_df)
            cleaned_df = cleaned_df.drop_duplicates()
            removed_duplicates = initial_rows - len(cleaned_df)
            
            if removed_duplicates > 0:
                st.info(f"Removed {removed_duplicates} duplicate rows")
            
            self.logger.info(f"Data cleaning completed: {len(cleaned_df)} rows remaining")
            return cleaned_df
            
        except Exception as e:
            self.logger.error(f"Data cleaning error: {str(e)}")
            st.error(f"Data cleaning error: {str(e)}")
            return df
    
    def perform_revenue_forecast(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform revenue forecasting using ML models
        Following AI/ML best practices
        """
        try:
            if 'Revenue' not in df.columns or 'Date' not in df.columns:
                return {"error": "Revenue and Date columns required for forecasting"}
            
            # Prepare data for forecasting
            forecast_df = df[['Date', 'Revenue']].copy()
            forecast_df = forecast_df.sort_values('Date')
            forecast_df['DayOfYear'] = forecast_df['Date'].dt.dayofyear
            forecast_df['Month'] = forecast_df['Date'].dt.month
            forecast_df['Quarter'] = forecast_df['Date'].dt.quarter
            forecast_df['WeekOfYear'] = forecast_df['Date'].dt.isocalendar().week
            
            # Feature engineering
            forecast_df['Revenue_MA7'] = forecast_df['Revenue'].rolling(window=7, min_periods=1).mean()
            forecast_df['Revenue_MA30'] = forecast_df['Revenue'].rolling(window=30, min_periods=1).mean()
            
            # Prepare features and target
            features = ['DayOfYear', 'Month', 'Quarter', 'WeekOfYear', 'Revenue_MA7', 'Revenue_MA30']
            X = forecast_df[features].fillna(method='bfill')
            y = forecast_df['Revenue']
            
            # Split data for validation
            split_idx = int(len(X) * 0.8)
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
            
            # Train Random Forest model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Model validation
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Generate future predictions
            last_date = forecast_df['Date'].max()
            future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=30, freq='D')
            
            future_features = []
            for date in future_dates:
                future_features.append([
                    date.dayofyear,
                    date.month,
                    date.quarter,
                    date.isocalendar().week,
                    forecast_df['Revenue'].tail(7).mean(),
                    forecast_df['Revenue'].tail(30).mean()
                ])
            
            future_X = pd.DataFrame(future_features, columns=features)
            future_predictions = model.predict(future_X)
            
            # Create forecast visualization
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=forecast_df['Date'],
                y=forecast_df['Revenue'],
                mode='lines',
                name='Historical Revenue',
                line=dict(color='#667eea', width=2)
            ))
            
            # Future predictions
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=future_predictions,
                mode='lines',
                name='Revenue Forecast',
                line=dict(color='#f093fb', width=2, dash='dash')
            ))
            
            fig.update_layout(
                title="Revenue Forecasting - Next 30 Days",
                xaxis_title="Date",
                yaxis_title="Revenue (€)",
                template="plotly_white",
                height=500
            )
            
            # Calculate insights
            current_avg = forecast_df['Revenue'].tail(30).mean()
            forecast_avg = np.mean(future_predictions)
            growth_prediction = ((forecast_avg - current_avg) / current_avg) * 100
            
            return {
                "model_performance": {"mae": mae, "r2_score": r2},
                "forecast_chart": fig,
                "insights": {
                    "growth_prediction": growth_prediction,
                    "forecast_avg": forecast_avg,
                    "current_avg": current_avg,
                    "confidence": "High" if r2 > 0.8 else "Medium" if r2 > 0.6 else "Low"
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
            # Identify relevant columns for segmentation
            required_cols = ['Revenue', 'Customers']
            available_cols = [col for col in required_cols if col in df.columns]
            
            if len(available_cols) < 2:
                return {"error": "Insufficient data for customer segmentation"}
            
            # Prepare segmentation features
            segment_features = ['Revenue', 'Customers']
            if 'AvgOrderValue' in df.columns:
                segment_features.append('AvgOrderValue')
            if 'SatisfactionScore' in df.columns:
                segment_features.append('SatisfactionScore')
            
            # Aggregate data by relevant dimensions
            if 'Segment' in df.columns:
                segment_data = df.groupby('Segment').agg({
                    'Revenue': 'sum',
                    'Customers': 'sum',
                    'AvgOrderValue': 'mean' if 'AvgOrderValue' in df.columns else 'count',
                    'SatisfactionScore': 'mean' if 'SatisfactionScore' in df.columns else 'count'
                }).reset_index()
            else:
                # Create segments based on date periods
                df_copy = df.copy()
                df_copy['Period'] = pd.to_datetime(df_copy['Date']).dt.to_period('M')
                segment_data = df_copy.groupby('Period').agg({
                    'Revenue': 'sum',
                    'Customers': 'sum',
                    'AvgOrderValue': 'mean' if 'AvgOrderValue' in df.columns else 'count',
                    'SatisfactionScore': 'mean' if 'SatisfactionScore' in df.columns else 'count'
                }).reset_index()
            
            # Prepare features for clustering
            features_for_clustering = segment_data[segment_features].fillna(0)
            
            # Normalize features
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features_for_clustering)
            
            # Perform K-means clustering
            optimal_clusters = min(4, len(features_scaled))
            kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
            clusters = kmeans.fit_predict(features_scaled)
            
            segment_data['Cluster'] = clusters
            
            # Create visualization
            if len(segment_features) >= 2:
                fig = px.scatter(
                    segment_data,
                    x=segment_features[0],
                    y=segment_features[1],
                    color='Cluster',
                    size='Revenue' if 'Revenue' in segment_features else None,
                    title="Customer Segmentation Analysis",
                    template="plotly_white",
                    height=500
                )
            else:
                fig = px.bar(
                    segment_data,
                    x='Cluster',
                    y='Revenue',
                    title="Revenue by Customer Segment",
                    template="plotly_white"
                )
            
            # Generate insights
            cluster_summary = segment_data.groupby('Cluster').agg({
                'Revenue': ['sum', 'mean'],
                'Customers': ['sum', 'mean']
            }).round(2)
            
            return {
                "segmentation_chart": fig,
                "cluster_summary": cluster_summary,
                "insights": {
                    "total_segments": optimal_clusters,
                    "high_value_segment": segment_data.loc[segment_data['Revenue'].idxmax(), 'Cluster'],
                    "segment_distribution": segment_data['Cluster'].value_counts().to_dict()
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
            # Select numeric columns for anomaly detection
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            if len(numeric_columns) == 0:
                return {"error": "No numeric columns found for anomaly detection"}
            
            # Prepare data for anomaly detection
            anomaly_data = df[numeric_columns].fillna(df[numeric_columns].median())
            
            # Apply Isolation Forest
            isolation_forest = IsolationForest(contamination=0.1, random_state=42)
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
                    marker=dict(color='#667eea', size=6)
                ))
                
                # Anomaly data points
                anomaly_data_points = df_with_anomalies[df_with_anomalies['Anomaly'] == -1]
                if not anomaly_data_points.empty:
                    fig.add_trace(go.Scatter(
                        x=anomaly_data_points['Date'],
                        y=anomaly_data_points['Revenue'],
                        mode='markers',
                        name='Anomalies',
                        marker=dict(color='#f093fb', size=10, symbol='diamond')
                    ))
                
                fig.update_layout(
                    title="Anomaly Detection in Revenue Data",
                    xaxis_title="Date",
                    yaxis_title="Revenue",
                    template="plotly_white",
                    height=500
                )
            else:
                # Alternative visualization for non-time series data
                fig = px.histogram(
                    df_with_anomalies,
                    x='IsAnomaly',
                    title="Anomaly Distribution",
                    template="plotly_white"
                )
            
            # Generate insights about anomalies
            if total_anomalies > 0:
                anomaly_details = df_with_anomalies[df_with_anomalies['IsAnomaly']]
                if 'Revenue' in anomaly_details.columns:
                    avg_anomaly_revenue = anomaly_details['Revenue'].mean()
                    avg_normal_revenue = df_with_anomalies[~df_with_anomalies['IsAnomaly']]['Revenue'].mean()
                    revenue_impact = ((avg_anomaly_revenue - avg_normal_revenue) / avg_normal_revenue) * 100
                else:
                    revenue_impact = 0
            else:
                revenue_impact = 0
            
            return {
                "anomaly_chart": fig,
                "anomaly_summary": {
                    "total_anomalies": total_anomalies,
                    "anomaly_percentage": round(anomaly_percentage, 2),
                    "revenue_impact": round(revenue_impact, 2)
                },
                "anomaly_data": df_with_anomalies[df_with_anomalies['IsAnomaly']] if total_anomalies > 0 else pd.DataFrame()
            }
            
        except Exception as e:
            self.logger.error(f"Anomaly detection error: {str(e)}")
            return {"error": f"Anomaly detection error: {str(e)}"}

def main():
    """
    Main application function following Streamlit best practices
    """
    # Initialize the platform
    platform = AnalyticaCoreAI()
    
    # Header section following SME business branding
    st.markdown("""
    <div class="main-header">
        <h1>🧠 AnalyticaCore AI</h1>
        <h3>AI-Powered Company Data Analysis Platform</h3>
        <p>Transform Your Business Data Into Strategic Insights</p>
        <p><strong>Contact:</strong> founder@analyticacoreai.com | <strong>Platform:</strong> DataSight AI Engine</p>
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
        
        # Handle data loading
        if data_source == "Generate Sample Data":
            if st.button("🔄 Generate SME Demo Data", use_container_width=True):
                with st.spinner("Generating realistic SME business data..."):
                    st.session_state.df = platform.generate_sample_business_data()
                    st.session_state.data_loaded = True
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
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
                        
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
        
        # Analysis options
        if st.session_state.data_loaded:
            st.header("🤖 AI Analysis Options")
            
            analysis_type = st.selectbox(
                "Select Analysis Type",
                [
                    "Business Overview",
                    "Revenue Forecasting",
                    "Customer Segmentation", 
                    "Anomaly Detection",
                    "Comparative Analysis"
                ]
            )
            
            if st.button("🚀 Run Analysis", use_container_width=True):
                st.session_state.selected_analysis = analysis_type
    
    # Main content area
    if st.session_state.data_loaded:
        df = st.session_state.df
        
        # Display basic data information
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>📊 Total Records</h3>
                <h2>{:,}</h2>
            </div>
            """.format(len(df)), unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>📈 Data Columns</h3>
                <h2>{}</h2>
            </div>
            """.format(len(df.columns)), unsafe_allow_html=True)
            
        with col3:
            if 'Revenue' in df.columns:
                total_revenue = df['Revenue'].sum()
                st.markdown("""
                <div class="metric-card">
                    <h3>💰 Total Revenue</h3>
                    <h2>€{:,.0f}</h2>
                </div>
                """.format(total_revenue), unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="metric-card">
                    <h3>📊 Data Quality</h3>
                    <h2>✅ Clean</h2>
                </div>
                """, unsafe_allow_html=True)
                
        with col4:
            if 'Date' in df.columns:
                date_range = df['Date'].max() - df['Date'].min()
                st.markdown("""
                <div class="metric-card">
                    <h3>📅 Date Range</h3>
                    <h2>{} Days</h2>
                </div>
                """.format(date_range.days), unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="metric-card">
                    <h3>🎯 Analysis Ready</h3>
                    <h2>✅ Yes</h2>
                </div>
                """, unsafe_allow_html=True)
        
        # Data preview
        st.subheader("📋 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Analysis results
        if 'selected_analysis' in st.session_state:
            analysis_type = st.session_state.selected_analysis
            
            st.subheader(f"🔍 {analysis_type} Results")
            
            if analysis_type == "Business Overview":
                # Basic statistical overview
                st.subheader("📊 Statistical Summary")
                st.dataframe(df.describe(), use_container_width=True)
                
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
                        template="plotly_white"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
            elif analysis_type == "Revenue Forecasting":
                with st.spinner("🔮 Generating revenue forecast..."):
                    forecast_results = platform.perform_revenue_forecast(df)
                
                if "error" in forecast_results:
                    st.error(forecast_results["error"])
                else:
                    # Display forecast chart
                    st.plotly_chart(forecast_results["forecast_chart"], use_container_width=True)
                    
                    # Display insights
                    insights = forecast_results["insights"]
                    st.markdown(f"""
                    <div class="insight-box">
                        <h3>🎯 AI Forecast Insights</h3>
                        <p><strong>Growth Prediction:</strong> {insights['growth_prediction']:.1f}% over next 30 days</p>
                        <p><strong>Forecast Confidence:</strong> {insights['confidence']}</p>
                        <p><strong>Expected Avg Revenue:</strong> €{insights['forecast_avg']:,.0f}/day</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Model performance
                    perf = forecast_results["model_performance"]
                    st.info(f"Model Performance: R² Score = {perf['r2_score']:.3f}, MAE = €{perf['mae']:,.0f}")
            
            elif analysis_type == "Customer Segmentation":
                with st.spinner("🎯 Analyzing customer segments..."):
                    segmentation_results = platform.perform_customer_segmentation(df)
                
                if "error" in segmentation_results:
                    st.error(segmentation_results["error"])
                else:
                    # Display segmentation chart
                    st.plotly_chart(segmentation_results["segmentation_chart"], use_container_width=True)
                    
                    # Display insights
                    insights = segmentation_results["insights"]
                    st.markdown(f"""
                    <div class="insight-box">
                        <h3>👥 Customer Segmentation Insights</h3>
                        <p><strong>Total Segments Identified:</strong> {insights['total_segments']}</p>
                        <p><strong>Highest Value Segment:</strong> Cluster {insights['high_value_segment']}</p>
                        <p><strong>Recommendation:</strong> Focus marketing efforts on high-value segments for maximum ROI</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Cluster summary
                    st.subheader("📊 Segment Summary")
                    st.dataframe(segmentation_results["cluster_summary"], use_container_width=True)
            
            elif analysis_type == "Anomaly Detection":
                with st.spinner("🔍 Detecting anomalies in your data..."):
                    anomaly_results = platform.detect_anomalies(df)
                
                if "error" in anomaly_results:
                    st.error(anomaly_results["error"])
                else:
                    # Display anomaly chart
                    st.plotly_chart(anomaly_results["anomaly_chart"], use_container_width=True)
                    
                    # Display summary
                    summary = anomaly_results["anomaly_summary"]
                    st.markdown(f"""
                    <div class="insight-box">
                        <h3>⚠️ Anomaly Detection Results</h3>
                        <p><strong>Anomalies Detected:</strong> {summary['total_anomalies']} ({summary['anomaly_percentage']:.1f}% of data)</p>
                        <p><strong>Revenue Impact:</strong> {summary['revenue_impact']:+.1f}% vs normal data</p>
                        <p><strong>Recommendation:</strong> Investigate anomalies for potential issues or opportunities</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show anomaly details if any
                    if not anomaly_results["anomaly_data"].empty:
                        st.subheader("🔍 Anomaly Details")
                        st.dataframe(anomaly_results["anomaly_data"], use_container_width=True)
            
            elif analysis_type == "Comparative Analysis":
                st.subheader("📊 Comparative Business Analysis")
                
                # Revenue by different dimensions
                if 'Revenue' in df.columns:
                    for col in ['Region', 'Product', 'Channel', 'Segment']:
                        if col in df.columns:
                            st.subheader(f"💰 Revenue by {col}")
                            revenue_by_category = df.groupby(col)['Revenue'].sum().reset_index()
                            fig = px.bar(
                                revenue_by_category,
                                x=col,
                                y='Revenue',
                                title=f"Revenue by {col}",
                                template="plotly_white"
                            )
                            st.plotly_chart(fig, use_container_width=True)
            
            # Reset analysis selection
            st.session_state.selected_analysis = None

if __name__ == "__main__":
    main()

"""
AnalyticaCore AI - Revised Pricing Strategy
Following project coding instructions and SME business context
Minimum €99/month positioning for professional AI analytics
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class AnalyticaCoreAIPricing:
    """
    Pricing strategy class following project guidelines
    SME-focused AI analytics with professional positioning
    """
    
    def __init__(self):
        self.company_name = "AnalyticaCore AI"
        self.minimum_price = 99
        self.target_market = "SME businesses"
        
    def get_pricing_tiers(self) -> Dict[str, Any]:
        """
        Returns pricing tiers with €99 minimum entry point
        Following SME business context and competitive positioning
        """
        return {
            "essential": {
                "price": "€99/month",
                "annual_discount": "€999/year (2 months free)",
                "target": "Small businesses (5-25 employees)",
                "positioning": "Professional AI analytics entry level",
                "features": [
                    "AI-powered data analysis (up to 50k rows)",
                    "Revenue forecasting (3-month predictions)",
                    "Customer segmentation analysis", 
                    "Basic anomaly detection",
                    "Monthly business reports",
                    "Email support",
                    "GDPR compliant processing"
                ],
                "data_limit": "50,000 rows/month",
                "forecast_horizon": "3 months",
                "support": "Email (48h response)"
            },
            
            "professional": {
                "price": "€199/month", 
                "annual_discount": "€1,990/year (2 months free)",
                "target": "Growing SMEs (25-100 employees)",
                "positioning": "Main target - comprehensive SME solution",
                "features": [
                    "All Essential features",
                    "Advanced ML forecasting (12-month predictions)",
                    "Real-time anomaly alerts",
                    "Custom business dashboards",
                    "API access for integrations",
                    "Weekly automated reports",
                    "Priority email + chat support",
                    "Advanced customer lifetime value analysis"
                ],
                "data_limit": "500,000 rows/month", 
                "forecast_horizon": "12 months",
                "support": "Email + Chat (24h response)"
            },
            
            "business": {
                "price": "€399/month",
                "annual_discount": "€3,990/year (2 months free)", 
                "target": "Established SMEs (100-500 employees)",
                "positioning": "Premium SME/lower mid-market",
                "features": [
                    "All Professional features",
                    "Multi-location data analysis",
                    "Custom AI model training",
                    "White-label reporting",
                    "Dedicated account manager",
                    "Phone support",
                    "On-demand consulting (2h/month included)",
                    "Advanced predictive analytics"
                ],
                "data_limit": "2,000,000 rows/month",
                "forecast_horizon": "18 months", 
                "support": "Phone + Email + Chat (12h response)"
            },
            
            "enterprise": {
                "price": "€799/month",
                "annual_discount": "€7,990/year (2 months free)",
                "target": "Mid-market companies (500+ employees)",
                "positioning": "Enterprise-lite solution",
                "features": [
                    "All Business features", 
                    "Unlimited data processing",
                    "Custom integrations development",
                    "On-premise deployment option",
                    "24/7 dedicated support",
                    "Monthly strategy consultations",
                    "Custom AI model development",
                    "SLA guarantees"
                ],
                "data_limit": "Unlimited",
                "forecast_horizon": "24 months",
                "support": "24/7 dedicated support team"
            }
        }
    
    def get_value_justification(self) -> Dict[str, str]:
        """
        Returns value justification for €99+ pricing
        Following business context and competitive positioning
        """
        return {
            "market_comparison": "Traditional BI tools: €200-500/month per user",
            "consultant_alternative": "Business analyst: €500-1000/day", 
            "enterprise_alternative": "Enterprise analytics: €5000-20000/month",
            "roi_calculation": "Typical 300-500% ROI within 6 months",
            "time_savings": "50-80 hours/month of manual analysis eliminated",
            "decision_speed": "Reduce decision-making time by 60-80%"
        }
