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

        self.assertEqual(Beat.objects.count(), 1)
        new_beat = Beat.objects.first()
        self.assertEqual(new_beat.title, 'Saawhitelife - Sin City Soul')

    def test_redirects_after_post_request(self):
        response = self.client.post('/', data={'beat_title': 'Saawhitelife - Sin City Soul'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/the-unique-url')

    def test_save_beat_only_on_post_request(self):
        self.client.get('/')
        self.assertEqual(Beat.objects.count(), 0)

    def test_display_all_beats(self):
        beat_1 = Beat.objects.create(title='Beat 1')
        beat_2 = Beat.objects.create(title='Beat 2')

        response = self.client.get('/')

        self.assertIn('Beat 1', response.content.decode())
        self.assertIn('Beat 2', response.content.decode())

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
