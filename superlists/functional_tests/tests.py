import unittest

from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        # self.browser.implicitly_wait(3)

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retreive_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )
        inputbox.send_keys("Buy a jug of milk.")
        user_list_url = self.browser.current_url
        inputbox.send_keys(Keys.ENTER)
        # self.assertRegex(user_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy a jug of milk.')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Drink a jug of milk.")
        inputbox.send_keys(Keys.ENTER)


        self.check_for_row_in_list_table('2: Drink a jug of milk.')
        self.check_for_row_in_list_table('1: Buy a jug of milk.')

        # Now a new user Francine visits the site

        ## We use a new browser session to make sure that no information
        ## from the previous user is coming through from cookies, LocalStorage etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francine visits the home page. There is not sign of the previously created list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy a jug of milk.', page_text)
        self.assertNotIn('Drink a jug', page_text)

        # Francine starts a new list by entering a new item. 
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francine gets her unique URL
        francine_list_url = self.browser.current_url
        self.assertRegex(francine_list_url, '/lists/.+')
        self.assertNotEqual(francine_list_url, user_list_url)

        # No trace of previous user
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy a jug of milk.', page_text)
        self.assertNotIn('Drink a jug', page_text)

    def test_layout_and_styling(self):
        # Andrew goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He notices the input box is centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('testing\n')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=5)