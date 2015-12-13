import time

from .base import FunctionalTest


TEST_EMAIL = 'user@mockmyid.com'


class LoginTest(FunctionalTest):

    def test_login_with_persona(self):

        # User clicks 'Sign in' link for the first time
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # Persona login forms appears
        self.switch_to_new_window('Mozilla Persona')

        self.browser.find_element_by_id('authentication_email')\
                    .send_keys(TEST_EMAIL)

        self.browser.find_element_by_tag_name('button').click()

        self.switch_to_new_window('To-Do')

        # User now sees that he is logged in
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out(email=TEST_EMAIL)

        # logout state is persistent after refresh
        self.browser.refresh()
        self.wait_to_be_logged_out(email=TEST_EMAIL)

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
