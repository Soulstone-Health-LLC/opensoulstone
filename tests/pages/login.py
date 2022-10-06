# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from selenium.webdriver.common.by import By


# ------------------------------------------------------------------------------
# Page Objects - Soulstone - Login
# ------------------------------------------------------------------------------
class Login:
    def __init__(self, driver):
        self.map = LoginMap(driver)

    def sendkeys_email(self, email):
        self.map.email_input.send_keys(email)

    def sendkeys_password(self, password):
        self.map.password_input.send_keys(password)

    def click_login(self):
        self.map.login_button.click()

    def click_forgot_password(self):
        self.map.forgot_password_button.click()


# ------------------------------------------------------------------------------
# Page Map - Soulstone - Loginn
# ------------------------------------------------------------------------------
class LoginMap:
    def __init__(self, driver):
        self._driver = driver

    @property
    def logo_image(self):
        return self._driver.find_element(By.CLASS_NAME, 'header-brand-img')

    @property
    def title_text(self):
        return self._driver.find_element(By.CLASS_NAME, 'login100-form-title')

    @property
    def login_form(self):
        return self._driver.find_element(By.CLASS_NAME, 'login100-form')

    @property
    def email_input(self):
        return self._driver.find_element(By.ID, 'email')

    @property
    def password_input(self):
        return self._driver.find_element(By.ID, 'password')

    @property
    def login_button(self):
        return self._driver.find_element(By.ID, 'submit')

    @property
    def forgot_password_button(self):
        return self._driver.find_element(By.ID, 'forgot_password')
