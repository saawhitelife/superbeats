from django.test import TestCase
from django.urls import resolve
from beats.views import home_page
from django.http import HttpRequest
# Create your tests here.


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page(self):
        home = resolve('/')
        self.assertEqual(home.func, home_page)
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(HttpRequest)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Superbeats</title>', html)
        self.assertTrue(html.endswith('</html>'))