from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest
import time

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Saawhitelife visits superbeats and tries to create
        # a new beat with an empty name
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_beat_input').send_keys(Keys.ENTER)

        # Pages refreshes and says it is impossible to create
        # empty-named beats
        self.wait_for(lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                'You cant submit an empty beat'
            ))

        # Saawhitelife tries again, with a real beat name
        # and it works
        self.browser.find_element_by_id('id_new_beat_input').send_keys('Saawhitelife - Fata Morgana')
        self.browser.find_element_by_id('id_new_beat_input').send_keys(Keys.ENTER)
        self.wait_for_rows_in_table('1: Saawhitelife - Fata Morgana')

        # Saawhitelife tries again with an empty beat name
        self.browser.find_element_by_id('id_new_beat_input').send_keys(Keys.ENTER)

        # And again it fails
        self.wait_for(lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                'You cant submit an empty beat'
            ))
        # He can fix it anyway
        self.browser.find_element_by_id('id_new_beat_input').send_keys('Saawhitelife - Wah me!')
        self.browser.find_element_by_id('id_new_beat_input').send_keys(Keys.ENTER)
        self.wait_for_rows_in_table('1: Saawhitelife - Fata Morgana')
        self.wait_for_rows_in_table('2: Saawhitelife - Wah me!')