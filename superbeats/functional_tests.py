from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewBeatTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_text_in_table_rows(self, text):
        table = self.browser.find_element_by_id('id_beats_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(text, [row.text for row in rows])

    def test_can_start_a_list_of_beats_and_access_it_via_url(self):
        # You visit superbeats
        self.browser.get('http:/localhost:8000')

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
        time.sleep(1)
        self.check_for_text_in_table_rows('1: Saawhitelife - Sin City Soul')

        # superbeats still offer to enter another beat name
        # You enter second beat name and press enter
        input_box = self.browser.find_element_by_id('id_new_beat_input')
        input_box.send_keys('Saawhitelife - Grimoire')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        # Page refreshes and both beats are now in the list
        self.check_for_text_in_table_rows('1: Saawhitelife - Sin City Soul')
        self.check_for_text_in_table_rows('2: Saawhitelife - Grimoire')
        self.fail('Test end')
        # You see generated link for the list. The site
        # stored it for you

        # You visit the link and see the list there

        # Quit browser


if __name__ == '__main__':
    unittest.main(warnings='ignore')