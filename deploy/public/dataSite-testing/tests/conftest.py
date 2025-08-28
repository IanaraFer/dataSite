import pytest

@pytest.fixture(scope="session")
def sample_data():
    """Fixture to provide sample data for tests."""
    # Load or generate sample data here
    return {
        "sample_business_data": "path/to/sample_business_data.csv",
        "sample_sales_data": "path/to/sample_sales_data.xlsx",
        "sample_customer_data": "path/to/sample_customer_data.json"
    }

@pytest.fixture(scope="function")
def mock_data():
    """Fixture to provide mock data for individual tests."""
    return {
        "mock_key": "mock_value"
    }