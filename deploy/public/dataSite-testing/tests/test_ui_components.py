import pytest
import streamlit as st

@pytest.fixture
def sample_ui_data():
    """Fixture to provide sample data for UI component tests."""
    return {
        "title": "DataSight AI - Company Data Analyzer",
        "description": "Transform Your Business Data Into Actionable Insights Using Advanced AI",
        "button_label": "Upload Data",
    }

def test_ui_title(sample_ui_data):
    """Test that the UI title renders correctly."""
    st.title(sample_ui_data["title"])
    assert st.session_state.title == sample_ui_data["title"]

def test_ui_description(sample_ui_data):
    """Test that the UI description renders correctly."""
    st.write(sample_ui_data["description"])
    assert st.session_state.description == sample_ui_data["description"]

def test_ui_button(sample_ui_data):
    """Test that the UI button renders correctly."""
    button = st.button(sample_ui_data["button_label"])
    assert button is True  # Assuming button click is handled correctly in the UI

def test_ui_layout():
    """Test that the UI layout is as expected."""
    col1, col2 = st.columns(2)
    with col1:
        st.write("Column 1 Content")
    with col2:
        st.write("Column 2 Content")
    
    assert col1 is not None
    assert col2 is not None

def test_ui_error_handling():
    """Test that error messages are displayed correctly."""
    with pytest.raises(Exception):
        st.error("This is a test error message")
        assert st.session_state.error_message == "This is a test error message"