from .base import FunctionalTest
from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

TEST_EMAIL = 'saawhitelife@gmail.com'
SUBJECT = 'Superbeats login link'

class LoginTest(FunctionalTest):
    def test_login(self):
        # In the evening Saa wants to add his
        # huge new beat to the system.
        # He notices an input field labeled like it is
        # available to login by email now.
        # He is surprised and tries it
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_id('id_email').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertIn(
            'We\'ve sent an email for login. Kindly check your mail for the link.',
            self.browser.find_element_by_tag_name('body').text
        ))

        # Saa gots the email and finds a link over there
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(SUBJECT, email.subject)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Saa willingly clicks on the link
        self.browser.get(url)

        # Wow! Logged in!
        self.wait_for(lambda: self.browser.find_element_by_link_text('Logout'))
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)
