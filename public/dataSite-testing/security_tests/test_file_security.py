import pytest
import pandas as pd
from pathlib import Path
from dataSite import DataAnalyzer

@pytest.fixture
def analyzer():
    """Fixture to create a DataAnalyzer instance for testing."""
    return DataAnalyzer()

def test_file_upload_security(analyzer):
    """Test to ensure that uploaded files are secure and do not contain harmful content."""
    # Define the path to the test file
    test_file_path = Path(__file__).parent / 'test_data/invalid_samples/security_test.csv'
    
    # Attempt to load the file
    df = pd.read_csv(test_file_path)
    
    # Validate the uploaded data
    assert analyzer.validate_uploaded_data(df, test_file_path.name) is False, "File upload should be rejected due to security issues."

def test_file_size_limit(analyzer):
    """Test to ensure that file size limits are enforced."""
    # Define the path to a large test file
    large_file_path = Path(__file__).parent / 'test_data/invalid_samples/large_file.csv'
    
    # Attempt to load the file
    df = pd.read_csv(large_file_path)
    
    # Validate the uploaded data
    assert analyzer.validate_uploaded_data(df, large_file_path.name) is False, "File upload should be rejected due to size limit."

def test_malformed_file(analyzer):
    """Test to ensure that malformed files are handled correctly."""
    # Define the path to a malformed test file
    malformed_file_path = Path(__file__).parent / 'test_data/invalid_samples/malformed_data.csv'
    
    # Attempt to load the file
    df = pd.read_csv(malformed_file_path)
    
    # Validate the uploaded data
    assert analyzer.validate_uploaded_data(df, malformed_file_path.name) is False, "Malformed file should not be accepted."