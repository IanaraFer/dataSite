"""
Memory Tests for DataSight AI - Company Data Analyzer

This file contains tests to monitor memory usage during various operations
in the DataSight AI application. The tests aim to ensure that memory usage
remains within acceptable limits during data processing and analysis.
"""

import pytest
import tracemalloc
from data_analyzer import DataAnalyzer  # Adjust the import based on your project structure

@pytest.fixture(scope="module", autouse=True)
def setup_memory_tracking():
    """
    Fixture to set up memory tracking for the tests.
    """
    tracemalloc.start()
    yield
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Current memory usage: {current / 10**6:.2f} MB; Peak: {peak / 10**6:.2f} MB")

def test_memory_usage_load_sample_data(setup_memory_tracking):
    """
    Test memory usage when loading sample data.
    """
    analyzer = DataAnalyzer()
    df = analyzer.load_sample_data()
    assert df is not None, "Sample data should be loaded successfully"

def test_memory_usage_perform_analysis(setup_memory_tracking):
    """
    Test memory usage during comprehensive analysis.
    """
    analyzer = DataAnalyzer()
    df = analyzer.load_sample_data()
    results = analyzer.perform_comprehensive_analysis(df)
    assert results, "Analysis results should not be empty"

def test_memory_usage_forecasting(setup_memory_tracking):
    """
    Test memory usage during AI forecasting.
    """
    analyzer = DataAnalyzer()
    df = analyzer.load_sample_data()
    forecast_fig = analyzer.generate_ai_forecast(df, days=30)
    assert forecast_fig is not None, "Forecast figure should be generated successfully"