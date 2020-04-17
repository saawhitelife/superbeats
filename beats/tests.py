from django.test import TestCase
from beats.models import Beat, BeatList
from django.urls import resolve
from beats.views import home_page
from django.http import HttpRequest
# Create your tests here.


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_add_new_beat_POST_request(self):
        response = self.client.post('/beat_list/new', data={'beat_title': 'Saawhitelife - Sin City Soul'})

        self.assertEqual(Beat.objects.count(), 1)
        new_beat = Beat.objects.first()
        self.assertEqual(new_beat.title, 'Saawhitelife - Sin City Soul')

class BeatAndBeatListModelsTest(TestCase):
    def test_can_save_and_retrieve_beats(self):
        beat_list = BeatList()
        beat_list.save()

        first_beat = Beat()
        first_beat.title = 'Saawhitelife - Sin City Soul'
        first_beat.beat_list = beat_list
        first_beat.save()

        second_beat = Beat()
        second_beat.title = 'Saawhitelife - Grimoire'
        second_beat.beat_list = beat_list

        second_beat.save()

        saved_beat_list = BeatList.objects.first()
        self.assertEqual(beat_list, saved_beat_list)

        beats = Beat.objects.all()

        self.assertEqual(beats.count(), 2)

        self.assertEqual(beats[0].title, 'Saawhitelife - Sin City Soul')
        self.assertEqual(beats[0].beat_list, beat_list)
        self.assertEqual(beats[1].title, 'Saawhitelife - Grimoire')
        self.assertEqual(beats[1].beat_list, beat_list)

class BeatsViewTest(TestCase):
    def test_display_all_beats(self):
        beat_list = BeatList()
        beat_list.save()
        beat_1 = Beat.objects.create(title='Beat 1', beat_list=beat_list)
        beat_2 = Beat.objects.create(title='Beat 2', beat_list=beat_list)

        response = self.client.get('/beats/the-unique-url/')
        print(response)
        self.assertIn('Beat 1', response.content.decode())
        self.assertIn('Beat 2', response.content.decode())
    def test_use_beats_template(self):
        response = self.client.get('/beats/the-unique-url/')
        self.assertTemplateUsed(response, 'beats.html')

class NewBeatListTest(TestCase):
    def test_add_new_beat_POST_request(self):
        self.client.post('/beat_list/new', data={'beat_title': 'Saawhitelife - Sin City Soul'})
        self.assertEqual(Beat.objects.count(), 1)
        new_beat = Beat.objects.first()
        self.assertEqual(new_beat.title, 'Saawhitelife - Sin City Soul')

    def test_redirects_after_post_request(self):
        response = self.client.post('/beat_list/new', data={'beat_title': 'Saawhitelife - Sin City Soul'})
        self.assertRedirects(response, '/beats/the-unique-url/')