from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import unittest
from selenium.webdriver.common.keys import Keys
import time
import unittest
from django.test import LiveServerTestCase

MAX_WAIT = 10


class NewBeatTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

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


    def test_one_user_can_start_a_list_of_beats_and_access_it_via_url(self):
        # You visit superbeats
        self.browser.get(self.live_server_url)

        # You see heading and title
        self.assertIn('Superbeats', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Superbeats', header_text)

        # superbeats offers you to enter your first beat title
        input_box = self.browser.find_element_by_id('id_new_beat_input')
        self.assertEqual('Enter new beat name',
                         input_box.get_attribute('placeholder'))

        # You enter beat title and press enter. Page refreshes
        # and you see the beat title on the page
        input_box.send_keys('Saawhitelife - Sin City Soul')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_rows_in_table('1: Saawhitelife - Sin City Soul')

        # superbeats still offer to enter another beat name
        # You enter second beat name and press enter
        input_box = self.browser.find_element_by_id('id_new_beat_input')
        input_box.send_keys('Saawhitelife - Grimoire')
        input_box.send_keys(Keys.ENTER)
        # Page refreshes and both beats are now in the list
        self.wait_for_rows_in_table('1: Saawhitelife - Sin City Soul')
        self.wait_for_rows_in_table('2: Saawhitelife - Grimoire')
        self.fail('Test end')
        # You see generated link for the list. The site
        # stored it for you

        # You visit the link and see the list there

        # Quit browser

    def test_multiple_users_can_start_lists_at_different_URLS(self):
        # Saawhitelife visits superbeats
        self.browser.get(self.live_server_url)

        # Saawhitelife enters his new beat title and presses enter
        input_box = self.browser.find_element_by_id('id_new_beat_input')
        input_box.send_keys('Saawhitelife - Sin City Soul')
        input_box.send_keys(Keys.ENTER)

        # Saawhitelife sees his beat in the list on the page
        self.wait_for_rows_in_table('1: Saawhitelife - Sin City Soul')

        # JayZ sees that browser generated a new URL for him
        saawhitelife_beat_list_url = self.browser.current_url

        # ... and it is a valid URL
        self.assertRegex(saawhitelife_beat_list_url, '/beats/.+')

        # Now JayZ comes to visit superbeats
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        # JayZ doesnt see Saawhitelife's beats
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Saawhitelife - Sin City Soul', page_text)
        self.assertNotIn('Saawhitelife - Grimoire', page_text)

        # JayZ enters enter his beat title
        input_box = self.browser.find_element_by_id('id_new_beat_input')
        input_box.send_keys('JayZ - Dirt Off Your Shoulders')

        # JayZ presses enter and sees his beat on the page
        input_box.send_keys(Keys.ENTER)
        self.wait_for_rows_in_table('1: JayZ - Dirt Off Your Shoulders')

        # JayZ sees that superbeats generated URL for his list of beats
        jayz_beat_list_url = self.browser.current_url

        # It is a valid URL
        self.assertRegex(jayz_beat_list_url, '/beats/.+')

        # Saawhitelife's list url doesnt equal JayZ's
        self.assertEqual(jayz_beat_list_url, saawhitelife_beat_list_url)

        # Still no saawhitelife's beats on the page
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Saawhitelife - Sin City Soul', page_text)
        self.assertNotIn('Saawhitelife - Grimoire', page_text)


if __name__ == '__main__':
    unittest.main(warnings='ignore')