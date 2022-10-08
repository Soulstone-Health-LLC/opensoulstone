'''
tests/test_login.py
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.login import Login


# ------------------------------------------------------------------------------
# Site
# ------------------------------------------------------------------------------
LOCAL = "http://127.0.0.1:5000"


# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------
EMAIL = "rodneygauna+hh@gmail.com"
VALID_PASSWORD = "rodneygauna hh"


# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------
def test_login_exists():
    """Test - Login page exisits"""

    driver = webdriver.Chrome()

    # When the user navigates to the site
    driver.get(LOCAL)

    # Then the user should see the login form
    login_page = Login(driver)

    assert login_page.map.login_form.is_displayed()
    driver.quit()


def test_login_successful():
    """Test - Successfully login into the application"""

    driver = webdriver.Chrome()

    # Given the user navigates to the site
    driver.get(LOCAL)

    # And enters their login information
    login_page = Login(driver)

    login_page.sendkeys_email(EMAIL)
    login_page.sendkeys_password(VALID_PASSWORD)

    # When the user clicks Log In
    login_page.click_login()

    # Then the user should see the success banner
    message = 'Success! Logged in successfully'

    success_banner = driver.find_element(By.CLASS_NAME, "alert-inner--text")

    assert message in success_banner.text
    driver.quit()
