from selenium import webdriver
import unittest


class NewBeatTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_of_beats_and_access_it_via_url(self):
        # You visit superbeats
        self.browser.get('http:/localhost:8000')

        # You see heading and title
        self.assertIn('Superbeats', self.browser.title)
        self.fail('Test end')

        # superbeats offers you to enter your first beat title
        # You enter beat title and press enter. Page refreshes
        # and you see thhe beat title on the page

        # superbeats still offer to enter another beat name
        # You enter second beat name and press enter

        # Page refreshes and both beats are now in the list

        # You see generated link for the list. The site
        # stored it for you

        # You visit the link and see the list there

        # Quit browser


if __name__ == '__main__':
    unittest.main(warnings='ignore')