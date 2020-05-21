from .base import FunctionalTest
from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import os
import poplib
import time

SUBJECT = 'Superbeats login link'

class LoginTest(FunctionalTest):
    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.gmail.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['GOOGLE_PASSWORD'])
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_login(self):
        # In the evening Saa wants to add his
        # huge new beat to the system.
        # He notices an input field labeled like it is
        # available to login by email now.
        # He is surprised and tries it
        if self.staging_server:
            test_email = 'saa1white1life@gmail.com'
        else:
            test_email = 'saawhitelife@gmail.com'
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_email').send_keys(test_email)
        self.browser.find_element_by_id('id_email').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertIn(
            'We\'ve sent an email for login. Kindly check your mail for the link.',
            self.browser.find_element_by_tag_name('body').text
        ))
        # Saa gots the email and finds a link over there
        body = self.wait_for_email(test_email, SUBJECT)
        self.assertIn('Please use this url for login:', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Saa willingly clicks on the link
        self.browser.get(url)

        # Wow! Logged in!
        self.wait_for_user_to_login(test_email)

        # Now he quits superbeats
        self.browser.find_element_by_link_text('Logout').click()

        # Done quitting
        self.wait_for_user_to_logout(test_email)