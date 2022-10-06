# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from tests.pages.login import Login
from tests.pages.forgot_password import ForgotPassword


# ------------------------------------------------------------------------------
# Site
# ------------------------------------------------------------------------------
local = "http://127.0.0.1:5000"

# ------------------------------------------------------------------------------
# Global Variables
# ------------------------------------------------------------------------------
email = "rodneygauna@gmail.com"


# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------
def test_forgot_password_successful():
    """Test - Successfully request a password reset"""

    driver = webdriver.Chrome()

    # Given the user navigates to the site
    driver.get(local)

    # And clicks the forgot password button
    login_page = Login(driver)

    login_page.click_forgot_password()

    # When the user enters their email
    forgot_password_page = ForgotPassword(driver)

    forgot_password_page.sendkeys_email(email)

    # And clicks the Request Password Reset button
    forgot_password_page.click_request_reset_password()

    # Then the user should see a success banner
    success_banner_message = f"Success! An email to {email} with a reset password link."
    success_banner = driver.find_element(By.CLASS_NAME, "alert-inner--text")

    assert success_banner_message in success_banner
