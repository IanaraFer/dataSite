"""
DataSight AI - Enhanced Test Version with Diagnostics
Following the project's coding instructions and SME business context
"""

import streamlit as st
import sys
import os
from pathlib import Path
import logging
from datetime import datetime

# Configure logging following project guidelines
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration following Streamlit best practices
st.set_page_config(
    page_title="DataSight AI - System Test",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class SystemDiagnostics:
    """System diagnostics class following project coding guidelines"""
    
    def __init__(self):
        """Initialize diagnostics with proper error handling"""
        self.company_name = "AnalyticaCore AI"
        self.contact_email = "founder@analyticacoreai.com"
        self.platform_name = "DataSight AI"
        
    def check_python_environment(self) -> dict:
        """
        Check Python environment and dependencies
        Following project guidelines for comprehensive error handling
        """
        diagnostics = {
            'python_version': sys.version,
            'python_path': sys.executable,
            'working_directory': os.getcwd(),
            'streamlit_available': False,
            'pandas_available': False,
            'numpy_available': False,
            'errors': []
        }
        
        try:
            import streamlit as st_check
            diagnostics['streamlit_available'] = True
            diagnostics['streamlit_version'] = st_check.__version__
        except ImportError as e:
            diagnostics['errors'].append(f"Streamlit import error: {str(e)}")
            
        try:
            import pandas as pd
            diagnostics['pandas_available'] = True
            diagnostics['pandas_version'] = pd.__version__
        except ImportError as e:
            diagnostics['errors'].append(f"Pandas import error: {str(e)}")
            
        try:
            import numpy as np
            diagnostics['numpy_available'] = True
            diagnostics['numpy_version'] = np.__version__
        except ImportError as e:
            diagnostics['errors'].append(f"Numpy import error: {str(e)}")
            
        return diagnostics
    
    def generate_test_data(self) -> tuple:
        """
        Generate test business data following SME use cases
        Returns tuple of (success, data_or_error)
        """
        try:
            import pandas as pd
            import numpy as np
            
            # Generate realistic SME business data following project context
            dates = pd.date_range('2023-01-01', periods=100, freq='D')
            
            # SME revenue patterns with seasonality
            base_revenue = 15000
            seasonality = 3000 * np.sin(np.arange(100) / 365 * 2 * np.pi)
            noise = np.random.normal(0, 1000, 100)
            revenue = base_revenue + seasonality + noise
            revenue = np.maximum(revenue, 1000)  # Ensure positive values
            
            df = pd.DataFrame({
                'Date': dates,
                'Revenue': revenue.round(2),
                'Customers': np.random.randint(50, 150, 100),
                'Product_Category': np.random.choice(['Electronics', 'Clothing', 'Home'], 100),
                'Channel': np.random.choice(['Online', 'Store', 'Mobile'], 100),
                'Region': np.random.choice(['North', 'South', 'East', 'West'], 100)
            })
            
            return True, df
            
        except Exception as e:
            logger.error(f"Test data generation error: {str(e)}")
            return False, str(e)

def render_header():
    """Render application header following UI best practices"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; text-align: center;">
            🤖 DataSight AI - System Diagnostics
        </h1>
        <p style="color: white; margin: 0; text-align: center; opacity: 0.9;">
            Testing AI-Powered Company Data Analysis Platform
        </p>
        <p style="color: white; margin: 0; text-align: center; font-size: 0.9rem;">
            📧 Contact: founder@analyticacoreai.com | 🏢 AnalyticaCore AI
        </p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """
    Main application entry point following project guidelines
    Implements comprehensive error handling and diagnostics
    """
    try:
        # Render header
        render_header()
        
        # Initialize diagnostics
        diagnostics = SystemDiagnostics()
        
        # Sidebar with system info
        with st.sidebar:
            st.header("🔧 System Information")
            st.write(f"**Platform:** {diagnostics.platform_name}")
            st.write(f"**Company:** {diagnostics.company_name}")
            st.write(f"**Contact:** {diagnostics.contact_email}")
            st.write(f"**Python:** {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
            st.write(f"**Working Dir:** {Path.cwd().name}")
        
        # Main content tabs
        tab1, tab2, tab3 = st.tabs(["🔍 System Check", "📊 Data Test", "🚀 Quick Start"])
        
        with tab1:
            st.header("🔍 System Diagnostics")
            
            with st.spinner("Running system diagnostics..."):
                diag_results = diagnostics.check_python_environment()
            
            # Display Python info
            st.subheader("🐍 Python Environment")
            col1, col2 = st.columns(2)
            
            with col1:
                st.code(f"Version: {diag_results['python_version']}")
                st.code(f"Executable: {diag_results['python_path']}")
                
            with col2:
                st.code(f"Working Directory: {diag_results['working_directory']}")
            
            # Package status
            st.subheader("📦 Package Status")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if diag_results['streamlit_available']:
                    st.success(f"✅ Streamlit {diag_results.get('streamlit_version', 'Unknown')}")
                else:
                    st.error("❌ Streamlit Not Available")
                    
            with col2:
                if diag_results['pandas_available']:
                    st.success(f"✅ Pandas {diag_results.get('pandas_version', 'Unknown')}")
                else:
                    st.error("❌ Pandas Not Available")
                    
            with col3:
                if diag_results['numpy_available']:
                    st.success(f"✅ NumPy {diag_results.get('numpy_version', 'Unknown')}")
                else:
                    st.error("❌ NumPy Not Available")
            
            # Error reporting
            if diag_results['errors']:
                st.subheader("⚠️ Issues Found")
                for error in diag_results['errors']:
                    st.error(error)
                    
                st.subheader("🔧 Recommended Solutions")
                st.markdown("""
                **To fix missing packages:**
                
                1. **Activate virtual environment:**
                   ```bash
                   venv\\Scripts\\activate
                   ```
                
                2. **Install missing packages:**
                   ```bash
                   pip install streamlit pandas numpy
                   ```
                
                3. **Or run installation script:**
                   ```bash
                   install.bat
                   ```
                """)
            else:
                st.success("🎉 All systems operational!")
        
        with tab2:
            st.header("📊 Data Processing Test")
            
            if st.button("🧪 Run Data Test", use_container_width=True):
                with st.spinner("Testing data processing capabilities..."):
                    success, result = diagnostics.generate_test_data()
                
                if success:
                    st.success("✅ Data processing test successful!")
                    
                    # Display sample data
                    st.subheader("📋 Sample SME Business Data")
                    st.dataframe(result.head(10), use_container_width=True)
                    
                    # Basic analytics
                    st.subheader("📈 Basic Analytics Test")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        total_revenue = result['Revenue'].sum()
                        st.metric("💰 Total Revenue", f"€{total_revenue:,.0f}")
                        
                    with col2:
                        avg_revenue = result['Revenue'].mean()
                        st.metric("📊 Average Revenue", f"€{avg_revenue:,.0f}")
                        
                    with col3:
                        total_customers = result['Customers'].sum()
                        st.metric("👥 Total Customers", f"{total_customers:,}")
                        
                    with col4:
                        data_points = len(result)
                        st.metric("📈 Data Points", f"{data_points}")
                    
                    # Simple visualization test
                    try:
                        st.subheader("📊 Visualization Test")
                        st.line_chart(result.set_index('Date')['Revenue'])
                        st.success("✅ Chart rendering successful!")
                    except Exception as e:
                        st.error(f"❌ Chart rendering failed: {str(e)}")
                        
                else:
                    st.error(f"❌ Data test failed: {result}")
        
        with tab3:
            st.header("🚀 Quick Start Guide")
            
            st.markdown("""
            ### Welcome to DataSight AI Platform
            
            **For SME Business Data Analysis**
            
            #### 🎯 What This Platform Does:
            - **Revenue Forecasting** using AI/ML algorithms
            - **Customer Segmentation** for targeted marketing
            - **Business Trend Analysis** for strategic planning
            - **Automated Insights** for data-driven decisions
            
            #### 📋 Setup Checklist:
            """)
            
            # Dynamic checklist based on diagnostics
            diag_results = diagnostics.check_python_environment()
            
            checklist_items = [
                ("Python 3.11+", sys.version_info >= (3, 11)),
                ("Streamlit", diag_results['streamlit_available']),
                ("Pandas", diag_results['pandas_available']),
                ("NumPy", diag_results['numpy_available'])
            ]
            
            for item, status in checklist_items:
                if status:
                    st.success(f"✅ {item}")
                else:
                    st.error(f"❌ {item}")
            
            all_good = all(status for _, status in checklist_items)
            
            if all_good:
                st.success("🎉 **System Ready!** You can now run the full DataSight AI platform.")
                
                if st.button("🚀 Launch Full Platform", use_container_width=True):
                    st.markdown("""
                    **To launch the full platform:**
                    
                    1. Open terminal in your project directory
                    2. Activate virtual environment: `venv\\Scripts\\activate`
                    3. Run: `streamlit run app.py`
                    4. Open browser to: `http://localhost:8501`
                    """)
            else:
                st.warning("⚠️ **Setup Required** - Please install missing dependencies first.")
                
                if st.button("📥 Show Installation Commands", use_container_width=True):
                    st.code("""
# Windows Command Prompt
cd c:\\Users\\35387\\Desktop\\dataSite
python -m venv venv
venv\\Scripts\\activate
pip install --upgrade pip
pip install streamlit pandas numpy
streamlit run app_test.py
                    """)
            
            # Contact and support
            st.markdown("---")
            st.markdown(f"""
            **Need Help?**
            - 📧 Email: {diagnostics.contact_email}
            - 🏢 Company: {diagnostics.company_name}
            - 🌐 Platform: {diagnostics.platform_name}
            """)
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error(f"Critical error: {str(e)}")
        
        # Emergency diagnostic info
        st.markdown("### 🆘 Emergency Diagnostics")
        st.code(f"""
Python Version: {sys.version}
Python Path: {sys.executable}
Working Directory: {os.getcwd()}
Error: {str(e)}
        """)
        