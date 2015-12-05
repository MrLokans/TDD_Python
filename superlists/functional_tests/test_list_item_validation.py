from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):

        self.browser.get(self.server_url)

        # User tries to submit an empty list item
        # He hits enter on the empty input box

        self.browser.find_element_by_id('id_text').send_keys('\n')

        # the home page refreshes showing an error
        # that list items can not be empty
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # He tries to submit list item again, with some text, which now works
        self.browser.find_element_by_id('id_text').send_keys('Remember the milk\n')
        self.check_for_row_in_list_table('1: Remember the milk')

        # The user tries to to submit a second blank list item
        self.browser.find_element_by_id('id_text').send_keys('\n')

        # which also results in warning message
        self.check_for_row_in_list_table('1: Remember the milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element_by_id('id_text').send_keys('Remember the tea\n')
        self.check_for_row_in_list_table('1: Remember the milk')
        self.check_for_row_in_list_table('2: Remember the tea')

    def test_cannot_add_duplicate_items(self):
        # User goes to the home page and starts a new lsit
        self.browser.get(self.server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy laptop\n')
        self.check_for_row_in_list_table('1: Buy laptop')

        # He accidentally tries to add the same item
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy laptop\n')

        # He sees a helpful error message
        self.check_for_row_in_list_table('1. Buy laptop')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You've already got this in your list")
    