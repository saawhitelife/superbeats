from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_rows_in_table(self, text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_beats_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)