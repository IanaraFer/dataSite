"""
Base Page Object for Selenium Tests
This class provides common functionality for all page objects in the Selenium tests.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """
    Base class for all page objects in the Selenium tests.
    Provides common methods for interacting with web pages.
    """

    def __init__(self, driver):
        """
        Initialize the base page with a WebDriver instance.

        Args:
            driver: The Selenium WebDriver instance.
        """
        self.driver = driver

    def wait_for_element(self, by: By, value: str, timeout: int = 10):
        """
        Wait for an element to be present on the page.

        Args:
            by: The method to locate the element (e.g., By.ID, By.XPATH).
            value: The value to locate the element.
            timeout: The maximum time to wait for the element to be present.

        Returns:
            The located WebElement.
        """
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def click_element(self, by: By, value: str):
        """
        Click on an element located by the specified method.

        Args:
            by: The method to locate the element (e.g., By.ID, By.XPATH).
            value: The value to locate the element.
        """
        element = self.wait_for_element(by, value)
        element.click()

    def enter_text(self, by: By, value: str, text: str):
        """
        Enter text into an input field located by the specified method.

        Args:
            by: The method to locate the element (e.g., By.ID, By.XPATH).
            value: The value to locate the element.
            text: The text to enter into the input field.
        """
        element = self.wait_for_element(by, value)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, by: By, value: str) -> str:
        """
        Get the text of an element located by the specified method.

        Args:
            by: The method to locate the element (e.g., By.ID, By.XPATH).
            value: The value to locate the element.

        Returns:
            The text of the located element.
        """
        element = self.wait_for_element(by, value)
        return element.text
