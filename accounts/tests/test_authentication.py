from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = get_user_model()

class AuthenticateTest(TestCase):
    def test_returns_None_if_no_such_token(self):
        result = PasswordlessAuthenticationBackend().authenticate(
            'non-existing-token'
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        email = 'a@b.c'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(
            token.uid
        )
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        email = 'a@b.c'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(
            token.uid
        )
        self.assertEqual(existing_user, user)

class GetUserTest(TestCase):
    def test_gets_user_if_email_exists(self):
        User.objects.create(email='a@b.c')
        desired_user = User.objects.create(email='d@e.f')
        found_user = PasswordlessAuthenticationBackend().get_user('d@e.f')
        self.assertEqual(desired_user, found_user)

    def test_get_user_returns_none_if_email_does_not_exist(self):
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user('ola@la.nu')
        )
