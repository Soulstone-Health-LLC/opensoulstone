# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from selenium.webdriver.common.by import By


# ------------------------------------------------------------------------------
# Page Objects - Soulstone - Login
# ------------------------------------------------------------------------------
class ForgotPassword:
    def __init__(self, driver):
        self.map = ForgotPasswordMap(driver)

    def sendkeys_email(self, email):
        self.map.email_input.send_keys(email)

    def click_request_reset_password(self):
        self.map.request_reset_password_button.click()


# ------------------------------------------------------------------------------
# Page Map - Soulstone - Loginn
# ------------------------------------------------------------------------------
class ForgotPasswordMap:
    def __init__(self, driver):
        self._driver = driver

    @property
    def logo_image(self):
        return self._driver.find_element(By.CLASS_NAME, 'header-brand-img')

    @property
    def title_text(self):
        return self._driver.find_element(By.CLASS_NAME, 'login100-form-title')

    @property
    def email_input(self):
        return self._driver.find_element(By.ID, 'email')

    @property
    def request_reset_password_button(self):
        return self._driver.find_element(By.ID, 'submit')
