from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
from datetime import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os
from .server_tools import reset_database
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps')

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.options = webdriver.FirefoxOptions()
        self.gecko = '/usr/local/bin/geckodriver'
        self.options.add_argument('-headless')
        self.browser = webdriver.Firefox(executable_path=self.gecko, firefox_options=self.options)
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.\
            format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)
    def _test_has_failed(self):
        return any(error for (method, error) in self._outcome.errors)

    def add_beat_to_beat_list(self, beat_title):
        num_rows = len(self.browser.find_elements_by_css_selector('#id_beats_table tr'))
        self.get_input_box().send_keys(beat_title)
        self.get_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_rows_in_table(f'{item_number}: {beat_title}')

    def wait(fn):
        def wrap(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except(AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)
        return wrap

    @wait
    def wait_for(self, fn):
        return fn()

    def get_input_box(self):
        return self.browser.find_element_by_id('id_title')

    @wait
    def wait_for_user_to_login(self, email):
        self.browser.find_element_by_link_text('Logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_for_user_to_logout(self, email):
        self.browser.find_element_by_id('id_email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    @wait
    def wait_for_rows_in_table(self, text):
            table = self.browser.find_element_by_id('id_beats_table')
            rows = table.find_elements_by_tag_name('tr')
            self.assertIn(text, [row.text for row in rows])