from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class NewBeatTest(FunctionalTest):
    def test_one_user_can_start_a_list_of_beats_and_access_it_via_url(self):
        # You visit superbeats
        self.browser.get(self.live_server_url)

        # You see heading and title
        self.assertIn('Superbeats', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Superbeats', header_text)

        # superbeats offers you to enter your first beat title
        input_box = self.get_input_box()
        self.assertEqual('Enter new beat name',
                         input_box.get_attribute('placeholder'))

        # You enter beat title and press enter. Page refreshes
        # and you see the beat title on the page
        input_box.send_keys('Saawhitelife - Sin City Soul')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_rows_in_table('1: Saawhitelife - Sin City Soul')

        # superbeats still offer to enter another beat name
        # You enter second beat name and press enter
        input_box = self.get_input_box()
        input_box.send_keys('Saawhitelife - Grimoire')
        input_box.send_keys(Keys.ENTER)
        # Page refreshes and both beats are now in the list
        self.wait_for_rows_in_table('1: Saawhitelife - Sin City Soul')
        self.wait_for_rows_in_table('2: Saawhitelife - Grimoire')
        # You see generated link for the list. The site
        # stored it for you

        # You visit the link and see the list there

        # Quit browser

    def test_multiple_users_can_start_lists_at_different_URLS(self):
        # Saawhitelife visits superbeats
        self.browser.get(self.live_server_url)

        # Saawhitelife enters his new beat title and presses enter
        # Saawhitelife sees his beat in the list on the page
        self.add_beat_to_beat_list('Saawhitelife - Sin City Soul')

        # JayZ sees that browser generated a new URL for him
        saawhitelife_beat_list_url = self.browser.current_url

        # ... and it is a valid URL
        self.assertRegex(saawhitelife_beat_list_url, '/beat_list/.+')

        # Now JayZ comes to visit superbeats
        self.browser.quit()
        self.browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        self.browser.get(self.live_server_url)

        # JayZ doesnt see Saawhitelife's beats
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Saawhitelife - Sin City Soul', page_text)
        self.assertNotIn('Saawhitelife - Grimoire', page_text)

        # JayZ enters enter his beat title
        self.add_beat_to_beat_list('JayZ - Dirt Off Your Shoulders')

        # JayZ sees that superbeats generated URL for his list of beats
        jayz_beat_list_url = self.browser.current_url

        # It is a valid URL
        self.assertRegex(jayz_beat_list_url, '/beat_list/.+')

        # Saawhitelife's list url doesnt equal JayZ's
        self.assertNotEqual(jayz_beat_list_url, saawhitelife_beat_list_url)

        # Still no saawhitelife's beats on the page
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Saawhitelife - Sin City Soul', page_text)
        self.assertNotIn('Saawhitelife - Grimoire', page_text)
