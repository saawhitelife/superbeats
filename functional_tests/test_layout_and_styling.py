from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys

class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Saawhitelife visits superbeats
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He sees that input field is centered
        input_box = self.browser.find_element_by_id('id_new_beat_input')
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2,
                               512,
                               delta=10)
        # Saawhitelife enters his beat title and gets onto his
        # beat list page
        input_box.send_keys('Saawhitelife - Fata Morgana')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_rows_in_table('1: Saawhitelife - Fata Morgana')

        # Saa sees that the input field is well-centered too there
        input_box = self.browser.find_element_by_id('id_new_beat_input')
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2,
                               512,
                               delta=10)