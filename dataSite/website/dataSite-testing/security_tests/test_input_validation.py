import pytest
import pandas as pd
from pathlib import Path
from dataSite import DataAnalyzer

@pytest.fixture
def analyzer():
    return DataAnalyzer()

@pytest.mark.parametrize("input_data, expected", [
    ({"sales_revenue": 1000, "customers": 10}, True),
    ({"sales_revenue": -100, "customers": 10}, False),
    ({"sales_revenue": 1000, "customers": -5}, False),
    ({"sales_revenue": None, "customers": 10}, False),
    ({"sales_revenue": 1000}, False),  # Missing required field
])
def test_input_validation(analyzer, input_data, expected):
    df = pd.DataFrame([input_data])
    result = analyzer.validate_uploaded_data(df, "test_input.csv")
    assert result == expected

def test_file_size_limit(analyzer):
    large_file_path = Path("test_data/invalid_samples/large_file.csv")
    df = pd.read_csv(large_file_path)
    result = analyzer.validate_uploaded_data(df, large_file_path.name)
    assert result is False

def test_malformed_data(analyzer):
    malformed_file_path = Path("test_data/invalid_samples/malformed_data.csv")
    df = pd.read_csv(malformed_file_path)
    result = analyzer.validate_uploaded_data(df, malformed_file_path.name)
    assert result is False

def test_empty_file(analyzer):
    empty_file_path = Path("test_data/edge_cases/empty_file.csv")
    df = pd.read_csv(empty_file_path)
    result = analyzer.validate_uploaded_data(df, empty_file_path.name)
    assert result is False

def test_single_row_file(analyzer):
    single_row_file_path = Path("test_data/edge_cases/single_row.csv")
    df = pd.read_csv(single_row_file_path)
    result = analyzer.validate_uploaded_data(df, single_row_file_path.name)
    assert result is True  # Assuming single row is valid

def test_missing_columns(analyzer):
    missing_columns_file_path = Path("test_data/edge_cases/missing_columns.csv")
    df = pd.read_csv(missing_columns_file_path)
    result = analyzer.validate_uploaded_data(df, missing_columns_file_path.name)
    assert result is False