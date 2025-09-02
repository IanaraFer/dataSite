import pytest
import pandas as pd
from dataSite import DataAnalyzer

@pytest.fixture
def valid_data():
    """Fixture to provide valid sample data for testing."""
    return pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=10),
        'sales_revenue': [100, 150, 200, 250, 300, 350, 400, 450, 500, 550],
        'customers': [10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    })

@pytest.fixture
def invalid_data():
    """Fixture to provide invalid sample data for testing."""
    return pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=10),
        'sales_revenue': [100, None, 200, 250, None, 350, 400, None, 500, 550],
        'customers': [10, 15, None, 25, 30, 35, None, 45, 50, 55]
    })

def test_validate_uploaded_data_valid(valid_data):
    """Test that valid data passes validation."""
    analyzer = DataAnalyzer()
    assert analyzer.validate_uploaded_data(valid_data, "valid_data.csv") is True

def test_validate_uploaded_data_invalid(invalid_data):
    """Test that invalid data fails validation."""
    analyzer = DataAnalyzer()
    assert analyzer.validate_uploaded_data(invalid_data, "invalid_data.csv") is False

def test_validate_uploaded_data_empty():
    """Test that empty data fails validation."""
    analyzer = DataAnalyzer()
    empty_data = pd.DataFrame()
    assert analyzer.validate_uploaded_data(empty_data, "empty_data.csv") is False

def test_validate_uploaded_data_missing_columns():
    """Test that data with missing columns fails validation."""
    analyzer = DataAnalyzer()
    missing_columns_data = pd.DataFrame({
        'sales_revenue': [100, 150, 200]
    })
    assert analyzer.validate_uploaded_data(missing_columns_data, "missing_columns.csv") is False

def test_validate_uploaded_data_large_file():
    """Test that large data fails validation based on row limit."""
    analyzer = DataAnalyzer()
    large_data = pd.DataFrame({'A': range(100001)})  # Exceeds max_rows limit
    assert analyzer.validate_uploaded_data(large_data, "large_file.csv") is False