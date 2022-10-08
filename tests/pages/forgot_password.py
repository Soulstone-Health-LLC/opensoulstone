'''
tests/pages/forgot_password.py
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from selenium.webdriver.common.by import By


# ------------------------------------------------------------------------------
# Page Objects - Soulstone - Login
# ------------------------------------------------------------------------------
class ForgotPassword:
    '''
    Test - Reset Password Request Page Object
    '''

    def __init__(self, driver):
        self.map = ForgotPasswordMap(driver)

    def sendkeys_email(self, email):
        '''
        Tests - Reset Password Request - Types out the arg "email" in the
        email input
        '''

        self.map.email_input.send_keys(email)

    def click_request_reset_password(self):
        '''
        Test - Reset Password Request - Clicks the "Request Password Reset"
        button
        '''

        self.map.request_reset_password_button.click()


# ------------------------------------------------------------------------------
# Page Map - Soulstone - Loginn
# ------------------------------------------------------------------------------
class ForgotPasswordMap:
    '''
    Test - Reset Password Request Page Map
    '''

    def __init__(self, driver):
        self._driver = driver

    @property
    def logo_image(self):
        '''
        Test - Reset Password Request - Locates the logo on the page
        '''

        return self._driver.find_element(By.CLASS_NAME, 'header-brand-img')

    @property
    def title_text(self):
        '''
        Test - Reset Password Request - Locates the title on the page
        '''

        return self._driver.find_element(By.CLASS_NAME, 'login100-form-title')

    @property
    def email_input(self):
        '''
        Test - Reset Password Request - Locates the "Email" input on the page
        '''

        return self._driver.find_element(By.ID, 'email')

    @property
    def request_reset_password_button(self):
        '''
        Test - Reset Password Request - Locates the "Request Password Reset"
        button
        '''

        return self._driver.find_element(By.ID, 'submit')
