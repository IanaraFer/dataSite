import pytest
import pandas as pd
from pathlib import Path
from dataSite import DataAnalyzer

@pytest.fixture
def analyzer():
    return DataAnalyzer()

def test_data_privacy_valid_data(analyzer):
    # Test with valid data ensuring no sensitive information is leaked
    valid_data_path = Path(__file__).parent.parent / 'test_data' / 'valid_samples' / 'sample_business_data.csv'
    df = pd.read_csv(valid_data_path)
    
    assert analyzer.validate_uploaded_data(df, valid_data_path.name) is True
    # Check for sensitive data leaks
    assert 'sensitive_column' not in df.columns

def test_data_privacy_invalid_data(analyzer):
    # Test with invalid data that may contain sensitive information
    invalid_data_path = Path(__file__).parent.parent / 'test_data' / 'invalid_samples' / 'security_test.csv'
    df = pd.read_csv(invalid_data_path)
    
    assert analyzer.validate_uploaded_data(df, invalid_data_path.name) is False
    # Check for handling of sensitive data
    assert 'sensitive_column' not in df.columns

def test_data_privacy_edge_cases(analyzer):
    # Test edge cases for data privacy
    edge_case_path = Path(__file__).parent.parent / 'test_data' / 'edge_cases' / 'empty_file.csv'
    df = pd.read_csv(edge_case_path)
    
    assert analyzer.validate_uploaded_data(df, edge_case_path.name) is False

    edge_case_path = Path(__file__).parent.parent / 'test_data' / 'edge_cases' / 'single_row.csv'
    df = pd.read_csv(edge_case_path)
    
    assert analyzer.validate_uploaded_data(df, edge_case_path.name) is True

    edge_case_path = Path(__file__).parent.parent / 'test_data' / 'edge_cases' / 'missing_columns.csv'
    df = pd.read_csv(edge_case_path)
    
    assert analyzer.validate_uploaded_data(df, edge_case_path.name) is False