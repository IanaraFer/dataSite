"""
AI-Powered Company Data Analyzer
Main application entry point with Streamlit interface
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="AI Company Data Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🤖 AI-Powered Company Data Analyzer</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose Analysis Type", [
        "📤 Data Upload", 
        "📈 Forecasting", 
        "👥 Customer Segmentation", 
        "🔍 Anomaly Detection",
        "📊 Business Intelligence Dashboard"
    ])
    
    if page == "📤 Data Upload":
        data_upload_page()
    elif page == "📈 Forecasting":
        forecasting_page()
    elif page == "👥 Customer Segmentation":
        segmentation_page()
    elif page == "🔍 Anomaly Detection":
        anomaly_detection_page()
    elif page == "📊 Business Intelligence Dashboard":
        dashboard_page()

def data_upload_page():
    st.header("📤 Data Upload & Preview")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your company dataset", 
        type=['csv', 'xlsx', 'xls'],
        help="Supported formats: CSV, Excel"
    )
    
    if uploaded_file is not None:
        try:
            # Read the file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Store in session state
            st.session_state['data'] = df
            
            st.success(f"✅ Successfully loaded {len(df)} rows and {len(df.columns)} columns")
            
            # Data preview
            st.subheader("Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            # Data summary
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Rows", f"{len(df):,}")
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                st.metric("Numeric Columns", len(df.select_dtypes(include=[np.number]).columns))
            with col4:
                st.metric("Missing Values", f"{df.isnull().sum().sum():,}")
            
            # Column information
            st.subheader("Column Information")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes,
                'Missing Values': df.isnull().sum(),
                'Unique Values': [df[col].nunique() for col in df.columns]
            })
            st.dataframe(col_info, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")

def forecasting_page():
    st.header("📈 Sales & Revenue Forecasting")
    
    if 'data' not in st.session_state:
        st.warning("Please upload data first in the Data Upload section.")
        return
    
    df = st.session_state['data']
    
    # Column selection
    col1, col2 = st.columns(2)
    with col1:
        date_column = st.selectbox("Select Date Column", df.columns)
    with col2:
        value_column = st.selectbox("Select Value Column (Sales/Revenue)", 
                                   df.select_dtypes(include=[np.number]).columns)
    
    if st.button("Generate Forecast"):
        try:
            # Prepare data for Prophet
            forecast_df = df[[date_column, value_column]].copy()
            forecast_df.columns = ['ds', 'y']
            forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
            forecast_df = forecast_df.dropna()
            
            # Create and fit Prophet model
            model = Prophet(
                daily_seasonality=False,
                weekly_seasonality=True,
                yearly_seasonality=True
            )
            model.fit(forecast_df)
            
            # Make future predictions
            future = model.make_future_dataframe(periods=90)  # 90 days forecast
            forecast = model.predict(future)
            
            # Plot forecast
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=forecast_df['ds'], 
                y=forecast_df['y'],
                mode='lines+markers',
                name='Historical Data',
                line=dict(color='blue')
            ))
            
            # Forecast
            fig.add_trace(go.Scatter(
                x=forecast['ds'], 
                y=forecast['yhat'],
                mode='lines',
                name='Forecast',
                line=dict(color='red', dash='dash')
            ))
            
            # Confidence intervals
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat_upper'],
                fill=None,
                mode='lines',
                line_color='rgba(0,0,0,0)',
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat_lower'],
                fill='tonexty',
                mode='lines',
                line_color='rgba(0,0,0,0)',
                name='Confidence Interval',
                fillcolor='rgba(255,0,0,0.2)'
            ))
            
            fig.update_layout(
                title="Sales/Revenue Forecast",
                xaxis_title="Date",
                yaxis_title="Value",
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Key insights
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.subheader("🔍 Key Insights")
            
            last_actual = forecast_df['y'].iloc[-1]
            next_month_forecast = forecast[forecast['ds'] > forecast_df['ds'].max()]['yhat'].iloc[:30].mean()
            growth_rate = ((next_month_forecast - last_actual) / last_actual) * 100
            
            st.write(f"• **Current Value**: ${last_actual:,.2f}")
            st.write(f"• **Next Month Forecast**: ${next_month_forecast:,.2f}")
            st.write(f"• **Expected Growth**: {growth_rate:+.1f}%")
            
            if growth_rate > 5:
                st.write("• 📈 **Strong growth expected** - Consider increasing inventory or capacity")
            elif growth_rate < -5:
                st.write("• 📉 **Decline predicted** - Review marketing strategies or market conditions")
            else:
                st.write("• 📊 **Stable trend** - Maintain current strategies")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error generating forecast: {str(e)}")

def segmentation_page():
    st.header("👥 Customer Segmentation Analysis")
    
    if 'data' not in st.session_state:
        st.warning("Please upload data first in the Data Upload section.")
        return
    
    df = st.session_state['data']
    
    # Select features for clustering
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    selected_features = st.multiselect("Select features for segmentation", numeric_columns)
    
    if len(selected_features) >= 2 and st.button("Perform Segmentation"):
        try:
            # Prepare data
            cluster_data = df[selected_features].dropna()
            
            # Standardize features
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(cluster_data)
            
            # Perform K-means clustering
            n_clusters = st.slider("Number of segments", 2, 8, 4)
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(scaled_data)
            
            # Add cluster labels to original data
            cluster_df = cluster_data.copy()
            cluster_df['Segment'] = [f'Segment {i+1}' for i in clusters]
            
            # Visualize clusters (2D projection)
            if len(selected_features) >= 2:
                fig = px.scatter(
                    cluster_df, 
                    x=selected_features[0], 
                    y=selected_features[1],
                    color='Segment',
                    title="Customer Segments Visualization",
                    height=600
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Segment analysis
            st.subheader("📊 Segment Analysis")
            
            segment_summary = cluster_df.groupby('Segment')[selected_features].agg(['mean', 'count']).round(2)
            st.dataframe(segment_summary, use_container_width=True)
            
            # Recommendations
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.subheader("💡 Marketing Recommendations")
            
            for i in range(n_clusters):
                segment_data = cluster_df[cluster_df['Segment'] == f'Segment {i+1}']
                st.write(f"**Segment {i+1}** ({len(segment_data)} customers):")
                
                # Generate segment characteristics
                characteristics = []
                for feature in selected_features[:2]:  # Analyze top 2 features
                    avg_value = segment_data[feature].mean()
                    overall_avg = cluster_df[feature].mean()
                    if avg_value > overall_avg * 1.1:
                        characteristics.append(f"High {feature.lower()}")
                    elif avg_value < overall_avg * 0.9:
                        characteristics.append(f"Low {feature.lower()}")
                
                if characteristics:
                    st.write(f"  • Characteristics: {', '.join(characteristics)}")
                else:
                    st.write(f"  • Characteristics: Average across all metrics")
                
                st.write(f"  • Size: {len(segment_data)} customers ({len(segment_data)/len(cluster_df)*100:.1f}%)")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error performing segmentation: {str(e)}")

def anomaly_detection_page():
    st.header("🔍 Anomaly Detection")
    
    if 'data' not in st.session_state:
        st.warning("Please upload data first in the Data Upload section.")
        return
    
    df = st.session_state['data']
    
    # Select column for anomaly detection
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    selected_column = st.selectbox("Select column for anomaly detection", numeric_columns)
    
    if st.button("Detect Anomalies"):
        try:
            # Calculate statistics
            data_series = df[selected_column].dropna()
            
            # Use IQR method for anomaly detection
            Q1 = data_series.quantile(0.25)
            Q3 = data_series.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Identify anomalies
            anomalies = data_series[(data_series < lower_bound) | (data_series > upper_bound)]
            
            # Visualization
            fig = go.Figure()
            
            # Normal data points
            normal_data = data_series[(data_series >= lower_bound) & (data_series <= upper_bound)]
            fig.add_trace(go.Scatter(
                x=normal_data.index,
                y=normal_data.values,
                mode='markers',
                name='Normal Data',
                marker=dict(color='blue', size=6)
            ))
            
            # Anomalies
            fig.add_trace(go.Scatter(
                x=anomalies.index,
                y=anomalies.values,
                mode='markers',
                name='Anomalies',
                marker=dict(color='red', size=10, symbol='x')
            ))
            
            # Add threshold lines
            fig.add_hline(y=upper_bound, line_dash="dash", line_color="red", 
                         annotation_text="Upper Threshold")
            fig.add_hline(y=lower_bound, line_dash="dash", line_color="red", 
                         annotation_text="Lower Threshold")
            
            fig.update_layout(
                title=f"Anomaly Detection - {selected_column}",
                xaxis_title="Index",
                yaxis_title=selected_column,
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Data Points", len(data_series))
            with col2:
                st.metric("Anomalies Found", len(anomalies))
            with col3:
                st.metric("Anomaly Rate", f"{len(anomalies)/len(data_series)*100:.1f}%")
            
            # Show anomalies table
            if len(anomalies) > 0:
                st.subheader("🚨 Detected Anomalies")
                anomaly_df = pd.DataFrame({
                    'Index': anomalies.index,
                    'Value': anomalies.values,
                    'Deviation': ['High' if x > upper_bound else 'Low' for x in anomalies.values]
                })
                st.dataframe(anomaly_df, use_container_width=True)
                
                # Insights
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.subheader("💡 Insights")
                st.write(f"• Found {len(anomalies)} anomalous data points")
                st.write(f"• {len(anomalies[anomalies > upper_bound])} values are unusually high")
                st.write(f"• {len(anomalies[anomalies < lower_bound])} values are unusually low")
                st.write("• These anomalies may indicate data quality issues, unusual business events, or opportunities for investigation")
                st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error detecting anomalies: {str(e)}")

def dashboard_page():
    st.header("📊 Business Intelligence Dashboard")
    
    if 'data' not in st.session_state:
        st.warning("Please upload data first in the Data Upload section.")
        return
    
    df = st.session_state['data']
    
    # Quick statistics
    st.subheader("📈 Quick Statistics")
    
    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Average Value", f"{numeric_df.mean().mean():.2f}")
        with col2:
            st.metric("Max Value", f"{numeric_df.max().max():.2f}")
        with col3:
            st.metric("Min Value", f"{numeric_df.min().min():.2f}")
        with col4:
            st.metric("Data Quality", f"{(1-df.isnull().sum().sum()/(len(df)*len(df.columns)))*100:.1f}%")
    
    # Correlation heatmap
    if len(numeric_df.columns) > 1:
        st.subheader("🔗 Feature Correlations")
        
        corr_matrix = numeric_df.corr()
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Heatmap",
            color_continuous_scale='RdBu'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Distribution plots
    st.subheader("📊 Data Distributions")
    
    if not numeric_df.empty:
        selected_column = st.selectbox("Select column for distribution analysis", numeric_df.columns)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram
            fig_hist = px.histogram(
                df, 
                x=selected_column, 
                title=f"Distribution of {selected_column}",
                nbins=30
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Box plot
            fig_box = px.box(
                df, 
                y=selected_column, 
                title=f"Box Plot of {selected_column}"
            )
            st.plotly_chart(fig_box, use_container_width=True)

if __name__ == "__main__":
    main()
