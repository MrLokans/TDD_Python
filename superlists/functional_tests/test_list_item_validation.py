from .base import FunctionalTest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip


class ItemValidationTest(FunctionalTest):

    @skip
    def test_cannot_add_empty_list_items(self):

        # User tries to submit an empty list item
        # He hits enter on the empty input box

        # the home page refreshes showing an error
        # that list items can not be empty

        # He tries to submit list item again, with some text, which now works
        # The user tries to to submit a second blank list item
        # which also results in warning message

        self.fail('Correct me.')
