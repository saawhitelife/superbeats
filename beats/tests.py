from django.test import TestCase
from beats.models import Beat
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

class BeatModelTest(TestCase):
    def test_can_save_and_retrieve_beats(self):
        first_beat = Beat()
        first_beat.title = 'Saawhitelife - Sin City Soul'
        first_beat.save()

        second_beat = Beat()
        second_beat.title = 'Saawhitelife - Grimoire'
        second_beat.save()

        beats = Beat.objects.all()

        self.assertEqual(beats.count(), 2)

        self.assertEqual(beats[0].title, 'Saawhitelife - Sin City Soul')
        self.assertEqual(beats[1].title, 'Saawhitelife - Grimoire')
