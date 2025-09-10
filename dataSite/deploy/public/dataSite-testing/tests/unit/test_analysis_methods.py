import pytest
import pandas as pd
from dataSite import DataAnalyzer

@pytest.fixture
def sample_data():
    """Fixture to provide sample data for testing."""
    return pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=10),
        'sales_revenue': [100, 150, 200, 250, 300, 350, 400, 450, 500, 550],
        'customers': [10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    })

def test_financial_analysis(sample_data):
    """Test financial analysis methods."""
    analyzer = DataAnalyzer()
    results = analyzer._analyze_financial_metrics(sample_data, 'sales_revenue')
    
    assert results['total_revenue'] == 3250
    assert results['avg_daily_revenue'] == 325.0
    assert results['median_revenue'] == 325.0
    assert results['revenue_std'] == pytest.approx(150.0, rel=1e-2)
    assert results['max_revenue'] == 550
    assert results['min_revenue'] == 100

def test_customer_analysis(sample_data):
    """Test customer analysis methods."""
    analyzer = DataAnalyzer()
    results = analyzer._analyze_customer_metrics(sample_data, 'customers')
    
    assert results['total_customers'] == 275
    assert results['avg_daily_customers'] == 27.5
    assert results['peak_customers'] == 55

def test_operational_analysis(sample_data):
    """Test operational analysis methods."""
    sample_data['customer_satisfaction'] = [4, 4.5, 5, 3.5, 4, 4.2, 4.8, 4.9, 5, 4.1]
    analyzer = DataAnalyzer()
    results = analyzer._analyze_operational_metrics(sample_data, 'customer_satisfaction')
    
    assert results['avg_satisfaction'] == pytest.approx(4.41, rel=1e-2)
    assert results['high_satisfaction_rate'] == pytest.approx(80.0, rel=1e-2)

def test_geographic_analysis(sample_data):
    """Test geographic analysis methods."""
    sample_data['region'] = ['North', 'South', 'East', 'West', 'North', 'South', 'East', 'West', 'North', 'South']
    analyzer = DataAnalyzer()
    results = analyzer._analyze_geographic_performance(sample_data, 'region', 'sales_revenue')
    
    assert results['top_region'] == 'North'
    assert len(results['regional_performance']) == 4

def test_product_analysis(sample_data):
    """Test product analysis methods."""
    sample_data['product_category'] = ['Electronics', 'Clothing', 'Home', 'Sports', 'Electronics', 'Clothing', 'Home', 'Sports', 'Electronics', 'Clothing']
    analyzer = DataAnalyzer()
    results = analyzer._analyze_product_performance(sample_data, 'product_category', 'sales_revenue')
    
    assert results['top_category'] == 'Electronics'
    assert len(results['category_performance']) == 4

def test_trend_analysis(sample_data):
    """Test trend analysis methods."""
    analyzer = DataAnalyzer()
    results = analyzer._analyze_trends(sample_data, 'date', 'sales_revenue')
    
    assert 'trend_direction' in results
    assert 'trend_strength' in results
    assert 'r_squared' in results