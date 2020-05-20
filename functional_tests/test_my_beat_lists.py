from django.conf import settings
from .base import FunctionalTest
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .management.commands.create_session import create_pre_authenticated_session
from .server_tools import create_session_on_server

User = get_user_model()

class MyBeatList(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)
        ## place cookie
        ## use 404 for that
        self.browser.get(self.live_server_url + '/404')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/'
        ))

    def test_superbeats_can_remember_user(self):
        email = 'a@b.c'
        self.browser.get(self.live_server_url)
        self.wait_for_user_to_logout(email)

        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_for_user_to_login(email)

    def test_beat_lists_are_saved_for_logged_in_users_as_their_lists(self):
        # Saa is a superbeats known user
        # He is logged in
        self.create_pre_authenticated_session('saawhitelife@gmail.com')
        self.browser.get(self.live_server_url)
        self.add_beat_to_beat_list('Saawhitelife - My Face')
        self.add_beat_to_beat_list('Saawhitelife - Catharsis')
        first_list_url = self.browser.current_url

        # Now there's My Beatlists link.
        # He clicks on it
        self.browser.find_element_by_link_text('My Beatlists').click()

        # The list is there and its name based on the
        # first added element
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Saawhitelife - My Face')
        )
        self.browser.find_element_by_link_text('Saawhitelife - My Face').click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,  first_list_url
            )
        )

        # Saa creates the second list
        # just to see if it appears on in hist beatlists
        self.browser.get(self.live_server_url)
        self.add_beat_to_beat_list('Saawhitelife - Wah me!')
        second_list_url = self.browser.current_url
        self.browser.find_element_by_link_text('My Beatlists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Saawhitelife - Wah me!')
        )
        self.browser.find_element_by_link_text('Saawhitelife - Wah me!').click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                second_list_url
            )
        )

        # Saawhitelife logs out and there is
        # no My Beatlists link now
        self.browser.find_element_by_link_text('Logout').click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements_by_link_text('My Beatlists'),
                []
            )
        )



