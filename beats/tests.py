from django.test import TestCase
from django.urls import resolve
from beats.views import home_page
from django.http import HttpRequest
# Create your tests here.


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')