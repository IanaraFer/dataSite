import pytest
import pandas as pd
from dataSite.app import DataAnalyzer

@pytest.fixture
def data_analyzer():
    """Fixture to create a DataAnalyzer instance for testing."""
    return DataAnalyzer()

def test_load_sample_data(data_analyzer):
    """Test the loading of sample data."""
    df = data_analyzer.load_sample_data()
    assert not df.empty, "Sample data should not be empty"
    assert len(df) == 1000, "Sample data should contain 1000 records"
    assert 'sales_revenue' in df.columns, "Sample data should contain 'sales_revenue' column"

def test_validate_uploaded_data_valid(data_analyzer):
    """Test validation of valid uploaded data."""
    valid_data = {
        'date': pd.date_range(start='2023-01-01', periods=10),
        'sales_revenue': [1000] * 10,
        'customers': [10] * 10
    }
    df = pd.DataFrame(valid_data)
    assert data_analyzer.validate_uploaded_data(df, "valid_data.csv") is True

def test_validate_uploaded_data_empty(data_analyzer):
    """Test validation of empty uploaded data."""
    df = pd.DataFrame()
    assert data_analyzer.validate_uploaded_data(df, "empty_data.csv") is False

def test_validate_uploaded_data_insufficient_columns(data_analyzer):
    """Test validation of data with insufficient columns."""
    df = pd.DataFrame({'date': pd.date_range(start='2023-01-01', periods=10)})
    assert data_analyzer.validate_uploaded_data(df, "insufficient_columns.csv") is False

def test_perform_comprehensive_analysis(data_analyzer):
    """Test comprehensive analysis on sample data."""
    df = data_analyzer.load_sample_data()
    results = data_analyzer.perform_comprehensive_analysis(df)
    assert 'financial' in results, "Results should contain financial analysis"
    assert 'customers' in results, "Results should contain customer analysis"
    assert 'operations' in results, "Results should contain operational analysis"