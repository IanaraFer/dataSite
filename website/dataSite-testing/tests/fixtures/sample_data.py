from typing import Dict, Any
import pandas as pd
import numpy as np

def generate_sample_business_data(n_records: int = 1000) -> Dict[str, Any]:
    """
    Generate realistic sample business data for testing purposes.

    Args:
        n_records (int): Number of records to generate.

    Returns:
        Dict[str, Any]: A dictionary containing sample data.
    """
    # Set seed for reproducibility
    np.random.seed(42)

    # Generate date range
    date_range = pd.date_range(start='2023-01-01', end='2024-01-01', periods=n_records)

    # Generate business metrics
    base_sales = 15000
    trend = np.linspace(0, 5000, n_records)
    seasonality = 3000 * np.sin(np.arange(n_records) * 2 * np.pi / 365)
    weekly_pattern = 1000 * np.sin(np.arange(n_records) * 2 * np.pi / 7)
    noise = np.random.normal(0, 2000, n_records)

    # Create sample data
    data = {
        'date': date_range,
        'sales_revenue': np.maximum(base_sales + trend + seasonality + weekly_pattern + noise, 1000),
        'customers': np.random.poisson(150, n_records),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n_records, p=[0.3, 0.25, 0.25, 0.2]),
        'product_category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Sports'], n_records, p=[0.4, 0.3, 0.2, 0.1]),
        'customer_satisfaction': np.clip(np.random.normal(4.2, 0.8, n_records), 1, 5),
        'marketing_spend': np.random.uniform(2000, 8000, n_records),
        'employee_count': np.random.poisson(25, n_records),
        'operational_cost': np.random.uniform(8000, 15000, n_records),
        'orders': np.random.poisson(50, n_records),
        'website_visits': np.random.poisson(1000, n_records)
    }

    return data

# Sample data generation for testing
if __name__ == "__main__":
    sample_data = generate_sample_business_data()
    print(sample_data)