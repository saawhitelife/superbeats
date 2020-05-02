from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest
import time

class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')
    def test_cannot_add_empty_list_items(self):
        # Saawhitelife visits superbeats and tries to create
        # a new beat with an empty name
        self.browser.get(self.live_server_url)
        self.get_input_box().send_keys(Keys.ENTER)

        # Smart browser does not let it
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_title:invalid'))

        # Saa starts typing and error disappears
        self.get_input_box().send_keys('Saawhitelife - Fata Morgana')
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_title:valid'))

        # Saa can send it
        self.get_input_box().send_keys(Keys.ENTER)
        self.wait_for_rows_in_table('1: Saawhitelife - Fata Morgana')

        # Saawhitelife tries again with an empty beat name
        self.get_input_box().send_keys(Keys.ENTER)

        # And again it fails
        self.wait_for_rows_in_table('1: Saawhitelife - Fata Morgana')
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_title:invalid'))

        # He can continue typing and presses enter
        self.get_input_box().send_keys('Saawhitelife - Wah me!')
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_title:valid'))
        self.get_input_box().send_keys(Keys.ENTER)
        self.wait_for_rows_in_table('1: Saawhitelife - Fata Morgana')
        self.wait_for_rows_in_table('2: Saawhitelife - Wah me!')

    def test_cannot_add_duplicates(self):
        # Saa visits superbeats and adds his beat
        self.browser.get(self.live_server_url)
        self.get_input_box().send_keys('Saawhitelife - Grimoire')
        self.get_input_box().send_keys(Keys.ENTER)
        self.wait_for_rows_in_table('1: Saawhitelife - Grimoire')

        # Not to say occasionally, but intentionally
        # crazy producer enters same beat name again
        self.get_input_box().send_keys('Saawhitelife - Grimoire')
        self.get_input_box().send_keys(Keys.ENTER)

        # Saa sees a message saying smth about duplicates
        self.wait_for(lambda: self.assertIn(
            'Care duplicates bro',
            self.get_error_element().text
            ))

    def test_error_messages_disappear_on_input(self):
        # Saa starts a new list and raises a frontend validation error
        self.browser.get(self.live_server_url)
        self.get_input_box().send_keys('Saawhitelife - Catharsis')
        self.get_input_box().send_keys(Keys.ENTER)
        self.wait_for_rows_in_table('1: Saawhitelife - Catharsis')
        self.get_input_box().send_keys('Saawhitelife - Catharsis')
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # Saa starts typing something and the error
        # message disappears
        self.get_input_box().send_keys('something')
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))