import pytest
import pandas as pd
from pathlib import Path
from dataSite.app import DataAnalyzer

@pytest.fixture
def analyzer():
    """Fixture to create a DataAnalyzer instance for testing."""
    return DataAnalyzer()

def test_valid_file_upload_csv(analyzer):
    """Test uploading a valid CSV file."""
    file_path = Path(__file__).parent.parent / 'test_data/valid_samples/sample_business_data.csv'
    df = pd.read_csv(file_path)
    assert analyzer.validate_uploaded_data(df, file_path.name) is True

def test_valid_file_upload_excel(analyzer):
    """Test uploading a valid Excel file."""
    file_path = Path(__file__).parent.parent / 'test_data/valid_samples/sample_sales_data.xlsx'
    df = pd.read_excel(file_path)
    assert analyzer.validate_uploaded_data(df, file_path.name) is True

def test_valid_file_upload_json(analyzer):
    """Test uploading a valid JSON file."""
    file_path = Path(__file__).parent.parent / 'test_data/valid_samples/sample_customer_data.json'
    df = pd.read_json(file_path)
    assert analyzer.validate_uploaded_data(df, file_path.name) is True

def test_invalid_file_upload_malformed(analyzer):
    """Test uploading a malformed CSV file."""
    file_path = Path(__file__).parent.parent / 'test_data/invalid_samples/malformed_data.csv'
    df = pd.read_csv(file_path)
    assert analyzer.validate_uploaded_data(df, file_path.name) is False

def test_invalid_file_upload_large(analyzer):
    """Test uploading a large CSV file."""
    file_path = Path(__file__).parent.parent / 'test_data/invalid_samples/large_file.csv'
    df = pd.read_csv(file_path)
    assert analyzer.validate_uploaded_data(df, file_path.name) is False

def test_edge_case_empty_file(analyzer):
    """Test uploading an empty CSV file."""
    file_path = Path(__file__).parent.parent / 'test_data/edge_cases/empty_file.csv'
    df = pd.read_csv(file_path)
    assert analyzer.validate_uploaded_data(df, file_path.name) is False

def test_edge_case_single_row(analyzer):
    """Test uploading a single row CSV file."""
    file_path = Path(__file__).parent.parent / 'test_data/edge_cases/single_row.csv'
    df = pd.read_csv(file_path)
    assert analyzer.validate_uploaded_data(df, file_path.name) is True

def test_edge_case_missing_columns(analyzer):
    """Test uploading a CSV file missing required columns."""
    file_path = Path(__file__).parent.parent / 'test_data/edge_cases/missing_columns.csv'
    df = pd.read_csv(file_path)
    assert analyzer.validate_uploaded_data(df, file_path.name) is False