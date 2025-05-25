import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
from dotenv import load_dotenv

# Load environment variables from .env file for sensitive credentials
load_dotenv()

BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")
# BrowserStack hub URL for remote WebDriver connections
BROWSERSTACK_URL = f"http://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub.browserstack.com/wd/hub"

# Base URL of your React application (frontend).
# IMPORTANT: For BrowserStack Local, this should be your local machine's address.
# BrowserStack Local will tunnel this traffic.
APP_URL = "http://localhost:3000"

@pytest.fixture(scope="module")
def driver():
    """
    Pytest fixture to initialize and tear down the Selenium WebDriver
    for remote execution on BrowserStack.
    This fixture runs once per test module.
    """
    if not BROWSERSTACK_USERNAME or not BROWSERSTACK_ACCESS_KEY:
        raise ValueError("BrowserStack credentials not found in .env file. Please ensure BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY are set.")

    # Define desired capabilities for the test session on BrowserStack.
    # You can customize these to test on different OS, browsers, and versions.
    desired_cap = {
        'bstack:options': {
            'os': 'Windows',
            'osVersion': '10',
            'browserName': 'Chrome',
            'browserVersion': 'latest',
            'projectName': 'E-commerce App Tests',
            'buildName': 'Frontend UI Validation Build',
            'sessionName': 'Cart and Payments Flow Tests',
            'debug': 'true',       # Enable debug logging for the session
            'networkLogs': 'true', # Capture network traffic logs
            'consoleLogs': 'info', # Capture browser console logs
            'local': 'true'        # Crucial for testing localhost URLs via BrowserStack Local
        }
    }

    print(f"\nAttempting to connect to BrowserStack at {BROWSERSTACK_URL}")
    # Initialize the Remote WebDriver to connect to BrowserStack's grid
    browser = webdriver.Remote(
        command_executor=BROWSERSTACK_URL,
        desired_capabilities=desired_cap
    )
    print(f"Connected to BrowserStack. Navigating to {APP_URL}")
    browser.get(APP_URL) # Navigate to the application URL

    yield browser # Provide the WebDriver instance to the tests

    # Teardown: This code runs after all tests in the module are finished
    print("Test session finished. Quitting WebDriver.")
    browser.quit()