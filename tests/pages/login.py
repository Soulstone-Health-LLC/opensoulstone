'''
tests/pages/login.py
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from selenium.webdriver.common.by import By


# ------------------------------------------------------------------------------
# Page Objects - Soulstone - Login
# ------------------------------------------------------------------------------
class Login:
    '''
    Tests - Login Page Object
    '''

    # URL
    LOCAL = "http://127.0.0.1:5000"

    def __init__(self, driver):
        self.map = LoginMap(driver)

    # Loads the page
    def load(self):
        '''
        Navigate to the login page
        '''

        self.map.get(self.LOCAL)

    def sendkeys_email(self, email):
        '''
        Tests - Login - Types out the arg "email" in the email input
        '''

        self.map.email_input.send_keys(email)

    def sendkeys_password(self, password):
        '''
        Tests - Login - Types out the arg "password" in the password
        input
        '''

        self.map.password_input.send_keys(password)

    def click_login(self):
        '''
        Tests - Login - Clicks the "Login" button
        '''

        self.map.login_button.click()

    def click_forgot_password(self):
        '''
        Tests - Login - Clicks the "Forgot Password" button
        '''

        self.map.forgot_password_button.click()


# ------------------------------------------------------------------------------
# Page Map - Soulstone - Loginn
# ------------------------------------------------------------------------------
class LoginMap:
    '''
    Tests - Login Page Map
    '''

    def __init__(self, driver):
        self._driver = driver

    @property
    def logo_image(self):
        '''
        Tests - Login - Locates the logo on the page
        '''

        return self._driver.find_element(By.CLASS_NAME, 'header-brand-img')

    @property
    def title_text(self):
        '''
        Tests - Login - Locates the page's title
        '''

        return self._driver.find_element(By.CLASS_NAME, 'login100-form-title')

    @property
    def login_form(self):
        '''
        Tests - Login - Locates the login form on the page
        '''

        return self._driver.find_element(By.CLASS_NAME, 'login100-form')

    @property
    def email_input(self):
        '''
        Tests - Login - Locates the "Email" input on the page
        '''

        return self._driver.find_element(By.ID, 'email')

    @property
    def password_input(self):
        '''Tests - Login - Locates the "Password" input on the page
        '''

        return self._driver.find_element(By.ID, 'password')

    @property
    def login_button(self):
        '''
        Tests - Login - Locates the "Login" button on the page
        '''

        return self._driver.find_element(By.ID, 'submit')

    @property
    def forgot_password_button(self):
        '''
        Tests - Login - Locates the "Forgot Password" button on the page
        '''

        return self._driver.find_element(By.ID, 'forgot_password')
