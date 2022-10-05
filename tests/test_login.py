# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By


# ----------------------------------------------------------------------------------------------------------------------
# Site
# ----------------------------------------------------------------------------------------------------------------------
local = 'http://127.0.0.1:5000'


# ----------------------------------------------------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------------------------------------------------
def test_login():
    '''Test - Successfully login into the application'''
    driver = webdriver.Chrome()

    # Given the user navigates to the site
    driver.get(local)

    # And enters their login information
    user_email = 'rodneygauna+hh@gmail.com'
    user_password = 'rodneygauna+hh'

    email_input = driver.find_element(By.ID, 'email')
    password_input = driver.find_element(By.ID, 'password')

    email_input.send_keys(user_email)
    password_input.send_keys(user_password)

    # When the user clicks Log In
    login_button = driver.find_element(By.ID, 'submit')

    login_button.click()

    # Then the user should see the success banner
    success_banner_message = 'Success! Logged in successfully'

    success_banner = driver.find_element(By.CLASS_NAME, 'alert-inner--text')

    assert success_banner_message in success_banner.text
    driver.close()
