from django.test import TestCase
from unittest.mock import patch, call
from accounts.models import Token

class SendLoginEmailViewTest(TestCase):
    @patch('accounts.views.send_mail')
    def test_sends_mail_after_post(self, mock_send_mail):
        self.client.post('/accounts/send_login_email/',
                                    data={'email': 'a@b.c'})

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Superbeats login link')
        self.assertEqual(from_email, 'noreply@superbeats')
        self.assertEqual(to_list, ['a@b.c'])

    def test_redirects_to_home_page_after_email_is_sent(self):
        response = self.client.post('/accounts/send_login_email/',
                         data={'email': 'a@b.c'})
        self.assertRedirects(response, '/')

    def test_adds_success_message_after_email_sent(self):
        response = self.client.post('/accounts/send_login_email/',
                                    data={'email': 'a@b.c'},
                                    follow=True)
        message = list(response.context['messages'])[0]
        self.assertEqual(message.message, 'We\'ve sent an email for'
                    ' login. Kindly check your mail for the link.'
                    )
        self.assertEqual(message.tags, 'success')

    @patch('accounts.views.messages')
    def test_add_success_message_with_mock(self, mock_messages):
        response = self.client.post('/accounts/send_login_email/',
                                    data={'email': 'a@b.c'})
        expected_message = 'We\'ve sent an email for'\
                    ' login. Kindly check your mail for the link.'
        self.assertEqual(
            mock_messages.success.call_args,
            call(response.wsgi_request, expected_message)
        )

    def test_token_is_created_for_email(self):
        response = self.client.post('/accounts/send_login_email/',
                                    data={'email': 'a@b.c'})
        token = Token.objects.first()
        self.assertEqual(token.email, 'a@b.c')

    @patch('accounts.views.send_mail')
    def test_login_url_is_generated_using_token_uid(self, mock_send_mail):
        response = self.client.post('/accounts/send_login_email/',
                                    data={'email': 'a@b.c'})
        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    def test_redirects_to_home_page_after_clicking_link_from_email(self, mock_auth):
        response = self.client.get('/accounts/login?token=abcdxyz114')
        self.assertRedirects(response, '/')

    def test_calls_auth_with_uid_sent_from_email(self, mock_auth):
        self.client.get('/accounts/login?token=abcdxyz114')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abcdxyz114')
        )

    def test_calls_login_with_user_if_user_exists(self, mock_auth):
        response = self.client.get('/accounts/login?token=abcdxyz114')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_authenticate_did_not_return_user(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abcdxyz114')
        self.assertFalse(mock_auth.login.called)
