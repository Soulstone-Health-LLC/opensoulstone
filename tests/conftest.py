
"""
This module contains shared fixtures
"""

# ---------------------------------------------------------------
# Imports
# ---------------------------------------------------------------

import pytest
import selenium.webdriver


# ---------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------

@pytest.fixture
def browserChrome():
    # Initialize the ChromeDriver instance
    b = selenium.webdriver.Chrome()

    # Make its calls wait up to 10 seconds for elements to appear
    b.implicitly_wait(10)

    # Return the WebDriver instance for the setup
    yield b

    # Quit the WebDriver instance for the cleanup
    b.quit()


@pytest.fixture
def browserFirefox():
    # Initialize the ChromeDriver instance
    b = selenium.webdriver.Firefox()

    # Make its calls wait up to 10 seconds for elements to appear
    b.implicitly_wait(10)

    # Return the WebDriver instance for the setup
    yield b

    # Quit the WebDriver instance for the cleanup
    b.quit()