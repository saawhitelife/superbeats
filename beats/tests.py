from django.test import TestCase
from django.urls import resolve
from beats.views import home_page
# Create your tests here.


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page(self):
        home = resolve('/')
        self.assertEqual(home.func, home_page)