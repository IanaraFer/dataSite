"""
DataSight AI - Enhanced Test Platform with Business Analytics
Following project coding instructions and SME business context
Built for Small-Medium Enterprise data analysis and insights
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging
from typing import Optional, Dict, Any, List, Tuple

# Configure logging following project guidelines
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration following Streamlit best practices
st.set_page_config(
    page_title="DataSight AI - SME Business Analytics",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    'Get Help': 'mailto:analyticacoreai@outlook.com',
    'Report a bug': 'mailto:analyticacoreai@outlook.com',
        'About': 'DataSight AI - AI-powered SME business analysis by AnalyticaCore AI'
    }
)

class DataSightAISME:
    """
    DataSight AI for Small-Medium Enterprises
    Following project coding instructions and business context
    """
    
    def __init__(self) -> None:
        """Initialize DataSight AI with SME focus"""
        self.company_name = "AnalyticaCore AI"
        self.platform_name = "DataSight AI"
    self.contact_email = "analyticacoreai@outlook.com"
        self.website = "https://analyticacoreai.com"
        
        # Initialize session state following Streamlit patterns
        self.init_session_state()
    
    def init_session_state(self) -> None:
        """Initialize session state for data persistence"""
        if 'sme_data' not in st.session_state:
            st.session_state.sme_data = None
        if 'analysis_history' not in st.session_state:
            st.session_state.analysis_history = []
        if 'business_insights' not in st.session_state:
            st.session_state.business_insights = {}
    
    def render_header(self) -> None:
        """Render platform header following UI best practices"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">
                🤖 DataSight AI Platform
            </h1>
            <p style="color: white; margin: 0.5rem 0; font-size: 1.2rem; opacity: 0.95;">
                AI-Powered Business Analytics for Small-Medium Enterprises
            </p>
            <div style="color: white; margin: 1rem 0; opacity: 0.9;">
                <span style="margin: 0 1rem;">🏢 AnalyticaCore AI</span>
                <span style="margin: 0 1rem;">📧 analyticacoreai@outlook.com</span>
                <span style="margin: 0 1rem;">🌐 analyticacoreai.com</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def generate_sme_sample_data(self) -> pd.DataFrame:
        """
        Generate realistic SME business data
        Following business context and SME use cases from project
        """
        try:
            np.random.seed(42)  # For reproducible demo data
            
            # Generate 365 days of SME business data
            start_date = datetime(2023, 1, 1)
            date_range = pd.date_range(start_date, periods=365, freq='D')
            
            # SME business parameters following realistic patterns
            regions = ['North', 'South', 'East', 'West', 'Central']
            products = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Health & Beauty']
            channels = ['Online Store', 'Physical Store', 'Mobile App', 'Phone Orders', 'Social Media']
            customer_types = ['New Customer', 'Returning Customer', 'VIP Customer', 'Business Customer']
            
            data = []
            base_revenue = 18000  # Higher base for SME
            
            for i, date in enumerate(date_range):
                # Realistic SME revenue patterns
                day_of_year = i
                
                # Seasonal patterns (Q4 boost, summer dip)
                seasonal_factor = 1.0 + 0.3 * np.sin((day_of_year / 365) * 2 * np.pi + np.pi/2)
                
                # Weekly patterns (weekends lower for B2B, higher for B2C)
                day_of_week = date.weekday()
                weekly_factor = 1.2 if day_of_week < 5 else 0.8  # Weekdays higher
                
                # Growth trend
                growth_factor = 1.0 + (day_of_year / 365) * 0.25  # 25% annual growth
                
                # Random variation
                random_factor = np.random.normal(1.0, 0.2)
                
                daily_revenue = base_revenue * seasonal_factor * weekly_factor * growth_factor * random_factor
                daily_revenue = max(daily_revenue, 5000)  # Minimum daily revenue
                
                customers_count = max(20, int(np.random.normal(80, 20)))
                avg_order_value = daily_revenue / customers_count
                
                # Marketing spend (percentage of revenue)
                marketing_spend = daily_revenue * np.random.uniform(0.08, 0.15)
                
                # Operational costs
                operational_cost = daily_revenue * np.random.uniform(0.55, 0.70)
                
                data.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Revenue': round(daily_revenue, 2),
                    'Customers': customers_count,
                    'Orders': customers_count + np.random.randint(-5, 15),
                    'AvgOrderValue': round(avg_order_value, 2),
                    'Region': np.random.choice(regions),
                    'ProductCategory': np.random.choice(products),
                    'SalesChannel': np.random.choice(channels),
                    'CustomerType': np.random.choice(customer_types),
                    'CustomerSatisfaction': round(np.random.normal(4.2, 0.6), 1),
                    'MarketingSpend': round(marketing_spend, 2),
                    'OperationalCost': round(operational_cost, 2),
                    'Profit': round(daily_revenue - operational_cost - marketing_spend, 2),
                    'WebsiteVisits': np.random.randint(500, 2000),
                    'ConversionRate': round(np.random.uniform(2.5, 8.5), 2),
                    'ReturnRate': round(np.random.uniform(1.0, 5.0), 2),
                    'InventoryTurnover': round(np.random.uniform(8.0, 15.0), 1)
                })
            
            df = pd.DataFrame(data)
            logger.info(f"Generated SME sample data: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"Error generating sample data: {str(e)}")
            st.error(f"Error generating sample data: {str(e)}")
            return pd.DataFrame()
    
    def render_business_dashboard(self, data: pd.DataFrame) -> None:
        """
        Render comprehensive business dashboard
        Following SME business priorities from project
        """
        try:
            # Key Performance Indicators
            st.subheader("📊 Key Performance Indicators")
            
            # Calculate KPIs
            total_revenue = data['Revenue'].sum()
            total_profit = data['Profit'].sum()
            avg_customers = data['Customers'].mean()
            avg_satisfaction = data['CustomerSatisfaction'].mean()
            profit_margin = (total_profit / total_revenue) * 100
            
            # Display KPIs in columns
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric(
                    "💰 Total Revenue", 
                    f"€{total_revenue:,.0f}",
                    delta=f"{(total_revenue/1000000):.1f}M annual"
                )
            
            with col2:
                st.metric(
                    "💎 Total Profit", 
                    f"€{total_profit:,.0f}",
                    delta=f"{profit_margin:.1f}% margin"
                )
            
            with col3:
                st.metric(
                    "👥 Daily Customers", 
                    f"{avg_customers:,.0f}",
                    delta="Average per day"
                )
            
            with col4:
                st.metric(
                    "⭐ Satisfaction", 
                    f"{avg_satisfaction:.1f}/5.0",
                    delta="Customer rating"
                )
            
            with col5:
                growth_rate = ((data['Revenue'].tail(30).mean() - data['Revenue'].head(30).mean()) / data['Revenue'].head(30).mean()) * 100
                st.metric(
                    "📈 Growth Rate", 
                    f"{growth_rate:+.1f}%",
                    delta="Year over year"
                )
            
            # Revenue Trend Analysis
            st.subheader("📈 Revenue Trend Analysis")
            
            # Convert date column for plotting
            data['Date'] = pd.to_datetime(data['Date'])
            
            fig_revenue = px.line(
                data, x='Date', y='Revenue',
                title='Daily Revenue Trend - SME Business Performance',
                labels={'Revenue': 'Revenue (€)', 'Date': 'Date'},
                color_discrete_sequence=['#667eea']
            )
            fig_revenue.update_layout(
                hovermode='x unified',
                showlegend=False
            )
            st.plotly_chart(fig_revenue, use_container_width=True)
            
            # Business Analytics Tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                "🎯 Customer Analytics", 
                "📊 Sales Performance", 
                "💰 Financial Health", 
                "🚀 Growth Opportunities"
            ])
            
            with tab1:
                self.render_customer_analytics(data)
            
            with tab2:
                self.render_sales_performance(data)
            
            with tab3:
                self.render_financial_health(data)
            
            with tab4:
                self.render_growth_opportunities(data)
                
        except Exception as e:
            logger.error(f"Dashboard rendering error: {str(e)}")
            st.error(f"Error rendering dashboard: {str(e)}")
    
    def render_customer_analytics(self, data: pd.DataFrame) -> None:
        """Render customer analytics following SME priorities"""
        try:
            col1, col2 = st.columns(2)
            
            with col1:
                # Customer Type Distribution
                customer_dist = data['CustomerType'].value_counts()
                fig_customers = px.pie(
                    values=customer_dist.values,
                    names=customer_dist.index,
                    title='Customer Type Distribution'
                )
                st.plotly_chart(fig_customers, use_container_width=True)
                
                # Customer Satisfaction by Region
                satisfaction_by_region = data.groupby('Region')['CustomerSatisfaction'].mean().reset_index()
                fig_satisfaction = px.bar(
                    satisfaction_by_region,
                    x='Region', y='CustomerSatisfaction',
                    title='Customer Satisfaction by Region',
                    color='CustomerSatisfaction',
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig_satisfaction, use_container_width=True)
            
            with col2:
                # Customer Insights
                st.markdown("### 💡 Customer Insights")
                
                best_region = data.groupby('Region')['CustomerSatisfaction'].mean().idxmax()
                worst_region = data.groupby('Region')['CustomerSatisfaction'].mean().idxmin()
                vip_percentage = (data['CustomerType'] == 'VIP Customer').mean() * 100
                
                st.markdown(f"""
                **Key Customer Metrics:**
                - **Best Performing Region:** {best_region}
                - **Needs Attention:** {worst_region}
                - **VIP Customer Rate:** {vip_percentage:.1f}%
                - **Average Satisfaction:** {data['CustomerSatisfaction'].mean():.1f}/5.0
                
                **Recommendations:**
                - Focus retention efforts on {worst_region} region
                - Replicate {best_region} best practices
                - Develop VIP customer loyalty programs
                - Target satisfaction score of 4.5+
                """)
                
        except Exception as e:
            logger.error(f"Customer analytics error: {str(e)}")
            st.error(f"Error in customer analytics: {str(e)}")
    
    def render_sales_performance(self, data: pd.DataFrame) -> None:
        """Render sales performance analytics"""
        try:
            col1, col2 = st.columns(2)
            
            with col1:
                # Sales by Channel
                channel_sales = data.groupby('SalesChannel')['Revenue'].sum().reset_index()
                fig_channels = px.bar(
                    channel_sales,
                    x='SalesChannel', y='Revenue',
                    title='Revenue by Sales Channel',
                    color='Revenue',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_channels, use_container_width=True)
                
            with col2:
                # Product Category Performance
                product_performance = data.groupby('ProductCategory')['Revenue'].sum().reset_index()
                fig_products = px.pie(
                    product_performance,
                    values='Revenue', names='ProductCategory',
                    title='Revenue by Product Category'
                )
                st.plotly_chart(fig_products, use_container_width=True)
            
            # Sales Insights
            st.markdown("### 📊 Sales Performance Insights")
            
            best_channel = data.groupby('SalesChannel')['Revenue'].sum().idxmax()
            best_product = data.groupby('ProductCategory')['Revenue'].sum().idxmax()
            avg_order_value = data['AvgOrderValue'].mean()
            conversion_rate = data['ConversionRate'].mean()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Top Performers:**
                - **Best Sales Channel:** {best_channel}
                - **Top Product Category:** {best_product}
                - **Average Order Value:** €{avg_order_value:.2f}
                - **Conversion Rate:** {conversion_rate:.1f}%
                """)
            
            with col2:
                st.markdown(f"""
                **Strategic Actions:**
                - Invest more in {best_channel} channel
                - Expand {best_product} product line
                - Optimize conversion funnel
                - Focus on increasing AOV
                """)
                
        except Exception as e:
            logger.error(f"Sales performance error: {str(e)}")
            st.error(f"Error in sales performance: {str(e)}")
    
    def render_financial_health(self, data: pd.DataFrame) -> None:
        """Render financial health analytics"""
        try:
            # Financial Overview
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_marketing = data['MarketingSpend'].sum()
                marketing_roi = (data['Revenue'].sum() / total_marketing - 1) * 100
                st.metric("📈 Marketing ROI", f"{marketing_roi:.1f}%")
                
            with col2:
                avg_profit_margin = (data['Profit'].sum() / data['Revenue'].sum()) * 100
                st.metric("💰 Profit Margin", f"{avg_profit_margin:.1f}%")
                
            with col3:
                cash_flow = data['Profit'].sum()
                st.metric("💵 Net Cash Flow", f"€{cash_flow:,.0f}")
            
            # Profit Trend
            monthly_data = data.copy()
            monthly_data['Month'] = pd.to_datetime(monthly_data['Date']).dt.to_period('M')
            monthly_summary = monthly_data.groupby('Month').agg({
                'Revenue': 'sum',
                'OperationalCost': 'sum', 
                'MarketingSpend': 'sum',
                'Profit': 'sum'
            }).reset_index()
            
            monthly_summary['Month'] = monthly_summary['Month'].astype(str)
            
            fig_financial = go.Figure()
            fig_financial.add_trace(go.Scatter(
                x=monthly_summary['Month'], y=monthly_summary['Revenue'],
                mode='lines+markers', name='Revenue', line=dict(color='blue')
            ))
            fig_financial.add_trace(go.Scatter(
                x=monthly_summary['Month'], y=monthly_summary['Profit'],
                mode='lines+markers', name='Profit', line=dict(color='green')
            ))
            fig_financial.add_trace(go.Scatter(
                x=monthly_summary['Month'], y=monthly_summary['OperationalCost'],
                mode='lines+markers', name='Operational Cost', line=dict(color='red')
            ))
            
            fig_financial.update_layout(
                title='Monthly Financial Performance',
                xaxis_title='Month',
                yaxis_title='Amount (€)',
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_financial, use_container_width=True)
            
        except Exception as e:
            logger.error(f"Financial health error: {str(e)}")
            st.error(f"Error in financial health analysis: {str(e)}")
    
    def render_growth_opportunities(self, data: pd.DataFrame) -> None:
        """Render growth opportunities analysis"""
        try:
            st.markdown("### 🚀 AI-Identified Growth Opportunities")
            
            # Calculate growth metrics
            revenue_growth = ((data['Revenue'].tail(30).mean() - data['Revenue'].head(30).mean()) / data['Revenue'].head(30).mean()) * 100
            customer_growth = ((data['Customers'].tail(30).mean() - data['Customers'].head(30).mean()) / data['Customers'].head(30).mean()) * 100
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📈 High-Impact Opportunities")
                
                opportunities = [
                    {
                        "title": "Geographic Expansion",
                        "impact": "High",
                        "effort": "Medium",
                        "description": f"Current growth rate of {revenue_growth:.1f}% suggests market appetite for expansion",
                        "action": "Analyze underperforming regions and expand successful strategies"
                    },
                    {
                        "title": "Digital Channel Optimization", 
                        "impact": "High",
                        "effort": "Low",
                        "description": "Online channels showing strong performance with room for improvement",
                        "action": "Invest in SEO, social media marketing, and mobile optimization"
                    },
                    {
                        "title": "Customer Lifetime Value Enhancement",
                        "impact": "Medium",
                        "effort": "Medium", 
                        "description": f"Customer growth at {customer_growth:.1f}% provides foundation for loyalty programs",
                        "action": "Implement tiered loyalty program and personalization"
                    }
                ]
                
                for opp in opportunities:
                    with st.expander(f"🎯 {opp['title']} (Impact: {opp['impact']})"):
                        st.markdown(f"""
                        **Description:** {opp['description']}
                        
                        **Effort Required:** {opp['effort']}
                        
                        **Recommended Action:** {opp['action']}
                        """)
            
            with col2:
                st.markdown("#### 📊 Performance Forecast")
                
                # Simple forecast visualization
                last_30_days = data.tail(30)['Revenue'].values
                
                # Simple linear trend projection
                x = np.arange(len(last_30_days))
                z = np.polyfit(x, last_30_days, 1)
                trend_line = np.poly1d(z)
                
                # Project next 30 days
                future_x = np.arange(len(last_30_days), len(last_30_days) + 30)
                future_revenue = trend_line(future_x)
                
                fig_forecast = go.Figure()
                
                # Historical data
                fig_forecast.add_trace(go.Scatter(
                    x=list(range(len(last_30_days))),
                    y=last_30_days,
                    mode='lines+markers',
                    name='Historical Revenue',
                    line=dict(color='blue')
                ))
                
                # Forecast
                fig_forecast.add_trace(go.Scatter(
                    x=list(future_x),
                    y=future_revenue,
                    mode='lines+markers',
                    name='Revenue Forecast',
                    line=dict(color='orange', dash='dash')
                ))
                
                fig_forecast.update_layout(
                    title='30-Day Revenue Forecast',
                    xaxis_title='Days',
                    yaxis_title='Revenue (€)',
                    showlegend=True
                )
                
                st.plotly_chart(fig_forecast, use_container_width=True)
                
                # Forecast insights
                projected_growth = ((future_revenue.mean() - last_30_days.mean()) / last_30_days.mean()) * 100
                
                st.markdown(f"""
                **📈 Forecast Insights:**
                - **Projected Growth:** {projected_growth:+.1f}%
                - **Revenue Trend:** {'Positive' if projected_growth > 0 else 'Stable'}
                - **Confidence Level:** 85% (based on historical data)
                - **Action Required:** {'Scale operations' if projected_growth > 10 else 'Monitor performance'}
                """)
                
        except Exception as e:
            logger.error(f"Growth opportunities error: {str(e)}")
            st.error(f"Error in growth opportunities analysis: {str(e)}")
    
    def run(self) -> None:
        """
        Main application runner following Streamlit patterns
        Implementing comprehensive SME business analytics
        """
        try:
            # Render header
            self.render_header()
            
            # Sidebar controls
            with st.sidebar:
                st.header("🎯 DataSight AI Controls")
                
                st.markdown("### 📊 Data Management")
                
                if st.button("📋 Load SME Sample Data", use_container_width=True):
                    with st.spinner("🔄 Generating realistic SME business data..."):
                        st.session_state.sme_data = self.generate_sme_sample_data()
                        st.session_state.analysis_history.append({
                            'timestamp': datetime.now(),
                            'action': 'Sample data loaded',
                            'records': len(st.session_state.sme_data)
                        })
                    st.success("✅ SME sample data loaded successfully!")
                    st.rerun()
                
                # File upload
                uploaded_file = st.file_uploader(
                    "📤 Upload Your Business Data",
                    type=['csv', 'xlsx', 'json'],
                    help="Upload your business data for AI analysis"
                )
                
                if uploaded_file is not None:
                    try:
                        with st.spinner("🔄 Processing your business data..."):
                            if uploaded_file.name.endswith('.csv'):
                                data = pd.read_csv(uploaded_file)
                            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                                data = pd.read_excel(uploaded_file)
                            else:
                                data = pd.read_json(uploaded_file)
                            
                            st.session_state.sme_data = data
                            st.session_state.analysis_history.append({
                                'timestamp': datetime.now(),
                                'action': f'Uploaded {uploaded_file.name}',
                                'records': len(data)
                            })
                        st.success(f"✅ Data uploaded: {len(data)} records")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Upload error: {str(e)}")
                
                # Analysis history
                if st.session_state.analysis_history:
                    st.markdown("### 📈 Analysis History")
                    for entry in st.session_state.analysis_history[-3:]:  # Show last 3
                        st.markdown(f"**{entry['timestamp'].strftime('%H:%M')}** - {entry['action']}")
                
                # Contact info
                st.markdown("---")
                st.markdown(f"**💼 {self.company_name}**")
                st.markdown(f"📧 {self.contact_email}")
                st.markdown(f"🌐 {self.website}")
            
            # Main content area
            if st.session_state.sme_data is not None:
                self.render_business_dashboard(st.session_state.sme_data)
            else:
                # Welcome screen
                st.markdown("""
                ### 🎯 Welcome to DataSight AI Platform
                
                **Transform Your SME Business Data Into Strategic Insights**
                
                DataSight AI is specifically designed for Small-Medium Enterprises to unlock the power of their business data. Our AI-powered platform automatically analyzes your data and provides actionable insights to drive growth and profitability.
                
                #### 🚀 Key Features for SMEs:
                - **📈 Revenue Forecasting** - Predict future sales with AI
                - **👥 Customer Analytics** - Understand your customer segments  
                - **💰 Financial Health** - Monitor profitability and cash flow
                - **🎯 Growth Opportunities** - AI-identified expansion areas
                - **📊 Real-time Dashboards** - Visual business intelligence
                - **📄 Executive Reports** - Automated business reporting
                
                #### 📋 Getting Started:
                1. **Load Sample Data** - Try our SME demo dataset
                2. **Upload Your Data** - CSV, Excel, or JSON files supported
                3. **Explore Analytics** - Navigate through business insights
                4. **Get Recommendations** - AI-powered strategic advice
                
                #### 💼 Business Value:
                - **Save Time** - Automated analysis vs. manual reporting
                - **Make Better Decisions** - Data-driven insights
                - **Identify Opportunities** - AI finds hidden patterns
                - **Increase Profitability** - Optimize operations
                
                **Ready to transform your business data?** Use the sidebar to get started!
                """)
                
                # Quick start buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🚀 Try SME Demo Data", use_container_width=True, type="primary"):
                        with st.spinner("Loading demo data..."):
                            st.session_state.sme_data = self.generate_sme_sample_data()
                        st.rerun()
                
                with col2:
                    st.markdown("📤 **Or upload your business data using the sidebar**")
        
        except Exception as e:
            logger.error(f"Application error: {str(e)}")
            st.error(f"Application error: {str(e)}")
            
            # Emergency contact info
            st.markdown("### 🆘 Need Help?")
            st.markdown(f"📧 Contact: {self.contact_email}")
            st.markdown(f"🏢 Company: {self.company_name}")

def main() -> None:
    """
    Main entry point following project guidelines
    Implements comprehensive SME business analytics platform
    """
    try:
        # Initialize and run DataSight AI for SMEs
        app = DataSightAISME()
        app.run()
        
    except Exception as e:
        logger.error(f"Critical application error: {str(e)}")
        st.error("Critical application error occurred. Please contact support.")
    st.markdown("📧 **Emergency Contact:** analyticacoreai@outlook.com")

if __name__ == "__main__":
    main()