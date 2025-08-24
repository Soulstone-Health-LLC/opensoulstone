'''
tests/test_login.py
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from pages.login import Login


# ------------------------------------------------------------------------------
# Site
# ------------------------------------------------------------------------------
LOCAL = "http://127.0.0.1:5000"


# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------
EMAIL = "test.user@example.com"
VALID_PASSWORD = "secure_test_password"


# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------
def test_login_exists(browserChrome):
    """Test - Login page exisits"""

    # Page variables
    login_page = Login(browserChrome)

    # Given the login page is displayed
    login_page.load()

    # When the user enters their email and password
    login_page.sendkeys_email(EMAIL)
    login_page.sendkeys_password(VALID_PASSWORD)

    # Then the user should see the success banner
    message = 'Success! Logged in successfully'

    success_banner = driver.find_element(By.CLASS_NAME, "alert-inner--text")

    assert message in success_banner.text
