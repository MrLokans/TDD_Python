from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):

        self.browser.get(self.server_url)

        # User tries to submit an empty list item
        # He hits enter on the empty input box

        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # the home page refreshes showing an error
        # that list items can not be empty
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # He tries to submit list item again, with some text, which now works
        self.browser.find_element_by_id('id_new_item').send_keys('Remember the milk\n')
        self.check_for_row_in_list_table('1: Remember the milk')

        # The user tries to to submit a second blank list item
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # which also results in warning message
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element_by_id('id_new_item').send_keys('Remember the tea\n')
        self.check_for_row_in_list_table('1: Remember the milk')
        self.check_for_row_in_list_table('2: Remember the tea')
