import pytest
import pandas as pd
from dataSite.app import DataAnalyzer

@pytest.fixture
def sample_forecasting_data():
    """Fixture to provide sample data for forecasting tests."""
    date_range = pd.date_range(start='2023-01-01', periods=100)
    sales_revenue = pd.Series([100 + i * 10 for i in range(100)])
    return pd.DataFrame({'date': date_range, 'sales_revenue': sales_revenue})

def test_forecast_accuracy(sample_forecasting_data):
    """Test the accuracy of the AI forecasting method."""
    analyzer = DataAnalyzer()
    forecast_days = 30
    forecast_fig = analyzer.generate_ai_forecast(sample_forecasting_data, forecast_days)
    
    assert forecast_fig is not None, "Forecast figure should not be None"
    assert len(forecast_fig.data) > 0, "Forecast figure should contain data"
    assert 'AI Forecast' in [trace.name for trace in forecast_fig.data], "Forecast figure should include AI Forecast trace"

def test_forecast_with_insufficient_data():
    """Test forecasting with insufficient data."""
    analyzer = DataAnalyzer()
    insufficient_data = pd.DataFrame({'date': [], 'sales_revenue': []})
    
    forecast_fig = analyzer.generate_ai_forecast(insufficient_data, 30)
    
    assert forecast_fig is None, "Forecast figure should be None for insufficient data"

def test_forecast_with_invalid_data():
    """Test forecasting with invalid data."""
    analyzer = DataAnalyzer()
    invalid_data = pd.DataFrame({'date': ['invalid_date'], 'sales_revenue': ['not_a_number']})
    
    forecast_fig = analyzer.generate_ai_forecast(invalid_data, 30)
    
    assert forecast_fig is None, "Forecast figure should be None for invalid data"