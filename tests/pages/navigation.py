'''
tests/pages/navigation.py
'''

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from selenium.webdriver.common.by import By


# ------------------------------------------------------------------------------
# Page Objects - Soulstone - Navigation
# ------------------------------------------------------------------------------
class LeftNav:
    '''
    Tests - Left Navigation Object
    '''

    def __init__(self, driver):
        self.map = LeftNavMap(driver)

    def goto_dashboard_page(self):
        '''
        Test - Left Navigation - Clicks on the DASHBOARD link in the
        navigation bar
        '''

        self.map.dashboard_link.click()

    def goto_people_page(self):
        '''
        Test - Left Navigation - Clicks on the PEOPLE link in the navigation
        bar
        '''

        self.map.people_link.click()

    def goto_visit_notes_page(self):
        '''
        Test - Left Navigation - Clicks on the VISIT NOTES link in the
        navigationn bar
        '''

        self.map.visit_notes_link.click()

    def goto_billing_page(self):
        '''
        Test - Left Navigation - Clicks on the BILLING link in the navigation
        bar
        '''

        self.map.billing_link.click()

    def goto_settings_page(self):
        '''
        Test - Left Navigation - Clicks on the SETTINGS link in the navigation
        bar
        '''

        self.map.settings_link.click()

    def goto_settings_practice_information_page(self):
        '''
        Test - Left Navigation - Clicks on the SETTINGS > PRACTICE INFORMATION
        link
        in the navigation bar
        '''

        self.map.settings_practice_information_link.click()

    def goto_settings_user_maintenance_page(self):
        '''
        Test - Left Navigation - Clicks on the SETTINGS > USER MAINTENANCE link
        in the navigation bar
        '''

        self.map.settings_user_maintenance_link.click()

    def goto_settings_billing_charges_page(self):
        '''
        Test - Left Navigation - Clicks on the SETTINGS > BILLING CHARGES link
        in the navigation bar
        '''

        self.map.settings_billing_charges_link.click()


# ------------------------------------------------------------------------------
# Page Map - Soulstone - Navigation
# ------------------------------------------------------------------------------
class LeftNavMap:
    '''
    Tests - Left Navigation Map
    '''

    def __init__(self, driver):
        self._driver = driver

    @property
    def dashboard_link(self):
        '''
        Tests - Left Navigation - Location of the DASHBOARD link in the
        navigation bar
        '''

        return self._driver.find_element(By.ID, 'dashboard_link')

    @property
    def people_link(self):
        '''
        Tests - Left Navigation - Location of the PEOPLE link in the
        navigation bar
        '''

        return self._driver.find_element(By.ID, 'people_link')

    @property
    def visit_notes_link(self):
        '''
        Tests - Left Navigation - Location of the VISIT NOTES link in the
        navigation bar
        '''

        return self._driver.find_element(By.ID, 'visit_notes_link')

    @property
    def billing_link(self):
        '''
        Tests - Left Navigation - Location of the BILLING link in the
        navigation bar
        '''

        return self._driver.find_element(By.ID, 'billing_link')

    @property
    def settings_link(self):
        '''
        Tests - Left Navigation - Lcoation of the SETTINGS link in the
        navigation bar
        '''

        return self._driver.find_element(By.ID, 'settings_link')

    @property
    def settings_practice_information_link(self):
        '''
        Tests - Left Navigation - Location of the SETTINGS > PRACTICE
        INFORMATION link in the navigation bar
        '''

        return self._driver.find_element(By.ID,
                                         'settings_practice_information_link')

    @property
    def settings_user_maintenance_link(self):
        '''
        Tests - Left Navigation - Location of the SETTINGS > USER MAINTENANCE
        link in the navigation bar
        '''

        return self._driver.find_element(By.ID,
                                         'settings_user_maintenance_link')

    @property
    def settings_billing_charges_link(self):
        '''
        Tests - Left Navigation - Location of the SETTINGS > BILLING CHARGES
        link in the navigation bar
        '''

        return self._driver.find_element(By.ID,
                                         'settings_billing_charges_link')
