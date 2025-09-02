import pytest
import streamlit as st
from dataSite.app import main

@pytest.fixture
def client():
    """Fixture to create a Streamlit test client."""
    # Create a test client for the Streamlit app
    return st.test_client(main)

def test_streamlit_app_load(client):
    """Test that the Streamlit app loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert "DataSight AI - Company Data Analyzer" in response.text

def test_sidebar_navigation(client):
    """Test sidebar navigation functionality."""
    response = client.get("/")
    assert response.status_code == 200
    assert "🎛️ DataSight AI Control Panel" in response.text

def test_sample_data_loading(client):
    """Test loading of sample data."""
    response = client.get("/?data_source=sample")
    assert response.status_code == 200
    assert "✅ Sample Data Loaded Successfully!" in response.text

def test_file_upload(client):
    """Test file upload functionality."""
    # Simulate file upload
    with open("test_data/valid_samples/sample_business_data.csv", "rb") as f:
        response = client.post("/upload", files={"file": f})
    assert response.status_code == 200
    assert "✅ Data Uploaded Successfully!" in response.text

def test_forecasting(client):
    """Test AI forecasting functionality."""
    response = client.get("/forecast")
    assert response.status_code == 200
    assert "🔮 AI-Powered Sales Forecasting" in response.text

def test_insights_generation(client):
    """Test generation of AI insights."""
    response = client.get("/insights")
    assert response.status_code == 200
    assert "💡 AI-Generated Business Insights" in response.text

def test_export_actions(client):
    """Test export actions functionality."""
    response = client.get("/export")
    assert response.status_code == 200
    assert "📋 Export & Actions" in response.text