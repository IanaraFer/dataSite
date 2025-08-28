from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class MainPage:
    """
    Page object for the main page of the DataSight AI application.
    Encapsulates the elements and actions available on the main page.
    """

    def __init__(self, driver: WebDriver):
        """
        Initializes the MainPage object with a WebDriver instance.

        Args:
            driver (WebDriver): The WebDriver instance used to interact with the browser.
        """
        self.driver = driver
        self.url = "http://localhost:8501"  # Update with the actual URL if needed

    def open(self):
        """Opens the main page of the application."""
        self.driver.get(self.url)

    def get_title(self) -> str:
        """Returns the title of the main page."""
        return self.driver.title

    def is_element_present(self, by: By, value: str) -> bool:
        """
        Checks if an element is present on the page.

        Args:
            by (By): The method to locate the element (e.g., By.ID, By.XPATH).
            value (str): The value to locate the element.

        Returns:
            bool: True if the element is present, False otherwise.
        """
        try:
            self.driver.find_element(by, value)
            return True
        except:
            return False

    def click_button(self, by: By, value: str):
        """
        Clicks a button on the main page.

        Args:
            by (By): The method to locate the button (e.g., By.ID, By.XPATH).
            value (str): The value to locate the button.
        """
        button = self.driver.find_element(by, value)
        button.click()

    def get_element_text(self, by: By, value: str) -> str:
        """
        Retrieves the text of an element on the main page.

        Args:
            by (By): The method to locate the element (e.g., By.ID, By.XPATH).
            value (str): The value to locate the element.

        Returns:
            str: The text of the element.
        """
        element = self.driver.find_element(by, value)
        return element.text

    # Add more methods as needed to interact with the main page elements.