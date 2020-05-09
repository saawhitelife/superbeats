from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Token
from django.contrib import auth

User = get_user_model()


# Create your tests here.
class UserModelTest(TestCase):
    def test_model_is_valid_with_email_field_only(self):
        user = User(email='test@test.com')
        user.full_clean()

    def test_email_is_pk(self):
        user = User(email='a@b.c')
        self.assertEqual(user.pk, 'a@b.c')\

    def test_ordering_is_by_email(self):
        user_1 = User.objects.create(email='c@b.a')
        user_2 = User.objects.create(email='a@b.c')
        users = User.objects.all()
        self.assertEqual([user_2, user_1], list(users))

    def test_no_problem_with_auth_login(self):
        user = User.objects.create(email='a@b.c')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)

class TokenModelTest(TestCase):
    def test_link_user_with_uid_token(self):
        token_1 = Token.objects.create(email='a@b.c')
        token_2 = Token.objects.create(email='a@b.c')
        self.assertNotEqual(token_1.uid, token_2.uid)

