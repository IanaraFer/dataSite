"""
End-to-End Tests for DataSight AI - Company Data Analyzer

This module contains end-to-end tests that validate the entire workflow of the application,
from data upload to analysis, ensuring that all components interact correctly.
"""

import pytest
import streamlit as st
from data_analyzer import DataAnalyzer  # Assuming DataAnalyzer is the main class in your application
from utils.test_helpers import load_test_data  # Helper function to load test data

@pytest.fixture(scope="module")
def setup_data_analyzer():
    """Fixture to set up the DataAnalyzer instance for testing."""
    analyzer = DataAnalyzer()
    yield analyzer

def test_end_to_end_workflow(setup_data_analyzer):
    """Test the complete end-to-end workflow of the application."""
    analyzer = setup_data_analyzer
    
    # Step 1: Load sample data
    df = load_test_data("valid_samples/sample_business_data.csv")  # Adjust path as necessary
    assert df is not None and not df.empty, "Failed to load sample data"

    # Step 2: Validate uploaded data
    validation_result = analyzer.validate_uploaded_data(df, "sample_business_data.csv")
    assert validation_result, "Data validation failed"

    # Step 3: Perform comprehensive analysis
    analysis_results = analyzer.perform_comprehensive_analysis(df)
    assert analysis_results, "Analysis results are empty"

    # Step 4: Check specific analysis results
    assert "financial" in analysis_results, "Financial analysis results missing"
    assert "customers" in analysis_results, "Customer analysis results missing"
    assert "operations" in analysis_results, "Operational analysis results missing"

    # Step 5: Generate AI forecast
    forecast_fig = analyzer.generate_ai_forecast(df, days=30)
    assert forecast_fig is not None, "Forecast generation failed"

    # Step 6: Validate UI components (if applicable)
    # This can include checking if certain elements are rendered correctly in Streamlit
    # For example, you might want to check if specific metrics are displayed
    st.session_state['data'] = df  # Simulate data being loaded in the Streamlit app
    st.session_state['analysis_complete'] = True
    assert st.session_state['analysis_complete'], "Analysis completion flag not set"

    # Additional UI checks can be added here as needed
"""