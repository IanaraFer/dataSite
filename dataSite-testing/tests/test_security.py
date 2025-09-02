import pytest
import pandas as pd
from pathlib import Path
from dataSite import DataAnalyzer

@pytest.fixture
def analyzer():
    return DataAnalyzer()

def test_file_upload_security(analyzer):
    # Test for file upload security
    test_file = Path("test_data/invalid_samples/security_test.csv")
    assert test_file.exists(), "Security test file does not exist"
    
    df = pd.read_csv(test_file)
    assert analyzer.validate_uploaded_data(df, test_file.name), "File upload validation failed"

def test_input_validation(analyzer):
    # Test for input validation
    invalid_input = "<script>alert('XSS')</script>"
    assert not analyzer.validate_input(invalid_input), "Input validation failed for malicious input"

def test_data_privacy(analyzer):
    # Test for data privacy compliance
    sensitive_data = {"email": "test@example.com", "ssn": "123-45-6789"}
    assert analyzer.check_data_privacy(sensitive_data), "Data privacy check failed"

def test_file_size_limit(analyzer):
    # Test for file size limit
    large_file = Path("test_data/invalid_samples/large_file.csv")
    assert large_file.exists(), "Large file does not exist"
    
    df = pd.read_csv(large_file)
    assert len(df) <= analyzer.max_file_size_mb * 1024 * 1024, "File size exceeds the limit"