from django.conf import settings
from .base import FunctionalTest
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

User = get_user_model()

class UserBeatList(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## place cookie
        ## use 404 for that
        self.browser.get(self.live_server_url + '/404')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/'
        ))

    def test_beat_lists_are_saved_for_logged_in_users(self):
        email = 'a@b.c'
        self.browser.get(self.live_server_url)
        self.wait_for_user_to_logout(email)

        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_for_user_to_login(email)


