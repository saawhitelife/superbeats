from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys

class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Saawhitelife visits superbeats
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He sees that input field is centered
        input_box = self.get_input_box()
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2,
                               512,
                               delta=10)
        # Saawhitelife enters his beat title and gets onto his
        # beat list page
        self.add_beat_to_beat_list('Saawhitelife - Fata Morgana')

        # Saa sees that the input field is well-centered too there
        input_box = self.get_input_box()
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2,
                               512,
                               delta=10)