from typing import Any, Dict
import pandas as pd

def load_test_data(file_path: str) -> pd.DataFrame:
    """
    Load test data from a specified file path.
    
    Args:
        file_path (str): The path to the data file.
        
    Returns:
        pd.DataFrame: The loaded data as a DataFrame.
    """
    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            return pd.read_excel(file_path)
        elif file_path.endswith('.json'):
            return pd.read_json(file_path)
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        raise RuntimeError(f"Error loading data from {file_path}: {str(e)}")

def assert_data_frame_equal(df1: pd.DataFrame, df2: pd.DataFrame, check_dtype: bool = True) -> None:
    """
    Assert that two DataFrames are equal, with an option to check data types.
    
    Args:
        df1 (pd.DataFrame): The first DataFrame.
        df2 (pd.DataFrame): The second DataFrame.
        check_dtype (bool): Whether to check data types as well.
        
    Raises:
        AssertionError: If the DataFrames are not equal.
    """
    try:
        pd.testing.assert_frame_equal(df1, df2, check_dtype=check_dtype)
    except AssertionError as e:
        raise AssertionError(f"DataFrames are not equal: {str(e)}")

def generate_mock_data(num_records: int) -> Dict[str, Any]:
    """
    Generate mock data for testing purposes.
    
    Args:
        num_records (int): The number of records to generate.
        
    Returns:
        Dict[str, Any]: A dictionary containing mock data.
    """
    return {
        'sales_revenue': [1000 + i * 10 for i in range(num_records)],
        'customers': [i % 100 for i in range(num_records)],
        'date': pd.date_range(start='2023-01-01', periods=num_records).tolist()
    }