import time

from selenium.webdriver.support.ui import WebDriverWait

from .base import FunctionalTest


class LoginTest(FunctionalTest):

    def test_login_with_persona(self):

        # User clicks 'Sign in' link for the first time
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # Persona login forms appears
        self.switch_to_new_window('Mozilla Persona')

        self.browser.find_element_by_id('authentication_email')\
                    .send_keys('user@mockmyid.com')

        self.browser.find_element_by_tag_name('button').click()

        self.switch_to_new_window('To-Do')

        # User now sees that he is logged in
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('user@mockmyid.com', navbar.text)

    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail('Could not find window')

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id))
