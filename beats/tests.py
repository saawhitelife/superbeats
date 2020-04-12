from django.test import TestCase
from django.urls import resolve
from beats.views import home_page
from django.http import HttpRequest
# Create your tests here.


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_add_new_beat_POST_request(self):
        response = self.client.post('/', data={'beat_title': 'Saawhitelife - Sin City Soul'})
        self.assertIn('Saawhitelife - Sin City Soul', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')