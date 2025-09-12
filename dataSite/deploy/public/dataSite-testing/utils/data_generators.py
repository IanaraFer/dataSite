"""
DataSight AI - Data Generators for Testing

This module contains functions to generate test data for various scenarios
to ensure comprehensive testing of the DataSight AI platform.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_business_data(num_records: int = 1000) -> pd.DataFrame:
    """
    Generate a sample business dataset for testing purposes.

    Args:
        num_records (int): The number of records to generate.

    Returns:
        pd.DataFrame: A DataFrame containing sample business data.
    """
    np.random.seed(42)  # For reproducibility
    date_range = pd.date_range(start='2023-01-01', periods=num_records)

    data = {
        'date': date_range,
        'sales_revenue': np.random.uniform(1000, 50000, num_records),
        'customers': np.random.poisson(100, num_records),
        'region': np.random.choice(['North', 'South', 'East', 'West'], num_records),
        'product_category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Sports'], num_records),
        'customer_satisfaction': np.random.uniform(1, 5, num_records),
        'marketing_spend': np.random.uniform(500, 5000, num_records),
        'employee_count': np.random.randint(1, 100, num_records),
        'operational_cost': np.random.uniform(1000, 20000, num_records),
        'orders': np.random.poisson(20, num_records),
        'website_visits': np.random.poisson(500, num_records)
    }

    return pd.DataFrame(data)

def generate_invalid_data() -> pd.DataFrame:
    """
    Generate a DataFrame with invalid data for testing error handling.

    Returns:
        pd.DataFrame: A DataFrame containing invalid data.
    """
    data = {
        'date': [datetime.now()] * 10,
        'sales_revenue': ['invalid'] * 10,
        'customers': [None] * 10,
        'region': [None] * 10,
        'product_category': [None] * 10,
        'customer_satisfaction': [None] * 10,
        'marketing_spend': [None] * 10,
        'employee_count': [None] * 10,
        'operational_cost': [None] * 10,
        'orders': [None] * 10,
        'website_visits': [None] * 10
    }

    return pd.DataFrame(data)

def generate_edge_case_data() -> pd.DataFrame:
    """
    Generate a DataFrame with edge case data for testing.

    Returns:
        pd.DataFrame: A DataFrame containing edge case data.
    """
    data = {
        'date': [datetime.now()],
        'sales_revenue': [0],
        'customers': [0],
        'region': ['North'],
        'product_category': ['Electronics'],
        'customer_satisfaction': [1],
        'marketing_spend': [0],
        'employee_count': [1],
        'operational_cost': [0],
        'orders': [0],
        'website_visits': [0]
    }

    return pd.DataFrame(data)