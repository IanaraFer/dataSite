from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pytest

class TestFileUploadUI:
    @pytest.fixture(scope="class")
    def setup(self):
        # Set up the Selenium WebDriver
        self.driver = webdriver.Chrome()  # Ensure you have the ChromeDriver installed
        self.driver.get("http://localhost:8501")  # URL of the Streamlit app
        yield
        self.driver.quit()

    def test_file_upload(self, setup):
        # Locate the file upload element
        upload_element = self.driver.find_element(By.XPATH, "//input[@type='file']")
        
        # Upload a valid file
        upload_element.send_keys("path/to/your/test_data/valid_samples/sample_business_data.csv")
        
        # Wait for the file to be processed
        time.sleep(5)  # Adjust the sleep time as necessary for your app's processing time
        
        # Check for success message or any UI changes
        success_message = self.driver.find_element(By.CLASS_NAME, "success-message")
        assert "Data Uploaded Successfully" in success_message.text

    def test_invalid_file_upload(self, setup):
        # Locate the file upload element
        upload_element = self.driver.find_element(By.XPATH, "//input[@type='file']")
        
        # Upload an invalid file
        upload_element.send_keys("path/to/your/test_data/invalid_samples/malformed_data.csv")
        
        # Wait for the file to be processed
        time.sleep(5)  # Adjust the sleep time as necessary for your app's processing time
        
        # Check for error message
        error_message = self.driver.find_element(By.CLASS_NAME, "error-message")
        assert "Validation Error" in error_message.text

    def test_large_file_upload(self, setup):
        # Locate the file upload element
        upload_element = self.driver.find_element(By.XPATH, "//input[@type='file']")
        
        # Upload a large file
        upload_element.send_keys("path/to/your/test_data/invalid_samples/large_file.csv")
        
        # Wait for the file to be processed
        time.sleep(5)  # Adjust the sleep time as necessary for your app's processing time
        
        # Check for error message
        error_message = self.driver.find_element(By.CLASS_NAME, "error-message")
        assert "File too large" in error_message.text

    def test_empty_file_upload(self, setup):
        # Locate the file upload element
        upload_element = self.driver.find_element(By.XPATH, "//input[@type='file']")
        
        # Upload an empty file
        upload_element.send_keys("path/to/your/test_data/edge_cases/empty_file.csv")
        
        # Wait for the file to be processed
        time.sleep(5)  # Adjust the sleep time as necessary for your app's processing time
        
        # Check for error message
        error_message = self.driver.find_element(By.CLASS_NAME, "error-message")
        assert "Validation Error" in error_message.text

    def test_single_row_file_upload(self, setup):
        # Locate the file upload element
        upload_element = self.driver.find_element(By.XPATH, "//input[@type='file']")
        
        # Upload a single row file
        upload_element.send_keys("path/to/your/test_data/edge_cases/single_row.csv")
        
        # Wait for the file to be processed
        time.sleep(5)  # Adjust the sleep time as necessary for your app's processing time
        
        # Check for warning message
        warning_message = self.driver.find_element(By.CLASS_NAME, "warning-message")
        assert "Data Quality Warning" in warning_message.text

    def test_missing_columns_file_upload(self, setup):
        # Locate the file upload element
        upload_element = self.driver.find_element(By.XPATH, "//input[@type='file']")
        
        # Upload a file with missing columns
        upload_element.send_keys("path/to/your/test_data/edge_cases/missing_columns.csv")
        
        # Wait for the file to be processed
        time.sleep(5)  # Adjust the sleep time as necessary for your app's processing time
        
        # Check for error message
        error_message = self.driver.find_element(By.CLASS_NAME, "error-message")
        assert "Validation Error" in error_message.text