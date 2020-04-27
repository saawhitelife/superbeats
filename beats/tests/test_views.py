from django.test import TestCase
from beats.models import Beat, BeatList

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


class BeatsViewTest(TestCase):
    def test_display_beats_for_correct_list(self):
        correct_beat_list = BeatList()
        correct_beat_list.save()
        beat_1 = Beat.objects.create(title='Beat 1', beat_list=correct_beat_list)
        beat_2 = Beat.objects.create(title='Beat 2', beat_list=correct_beat_list)

        another_beat_list = BeatList.objects.create()
        another_beat_1 = Beat.objects.create(title='Another Beat 1', beat_list=another_beat_list)
        another_beat_2 = Beat.objects.create(title='Another Beat 2', beat_list=another_beat_list)

        response = self.client.get(f'/beat_list/{correct_beat_list.id}/')

        self.assertNotIn('Another Beat 1', response.content.decode())
        self.assertNotIn('Another Beat 2', response.content.decode())
        self.assertIn('Beat 1', response.content.decode())
        self.assertIn('Beat 2', response.content.decode())

    def test_use_beats_template(self):
        beat_list = BeatList.objects.create()
        response = self.client.get(f'/beat_list/{beat_list.id}/')
        self.assertTemplateUsed(response, 'beats.html')

    def test_pass_correct_list_id_to_template(self):
        beat_list = BeatList.objects.create()
        other_beat_list = BeatList.objects.create()
        response = self.client.get(f'/beat_list/{beat_list.id}/')
        self.assertEqual(response.context['beat_list'], beat_list)

    def test_can_add_beat_to_an_existing_beat_list(self):
        beat_list = BeatList.objects.create()
        another_beat_list = BeatList.objects.create()

        self.client.post(f'/beat_list/{beat_list.id}/',
                data={'beat_title': 'Beat for adding beats to a list test'})

        self.assertEqual(Beat.objects.count(), 1)

        new_beat = Beat.objects.first()
        self.assertEqual(new_beat.title, 'Beat for adding beats to a list test')
        self.assertEqual(new_beat.beat_list, beat_list)

    def test_validations_errors_a_passed_to_template(self):
        response = self.client.post('/beat_list/new', data={'beat_title': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = 'You cant submit an empty beat'
        self.assertContains(response, expected_error)

    def test_validation_errors_end_up_on_beat_list_page(self):
        beat_list = BeatList.objects.create()
        response = self.client.post(f'/beat_list/{beat_list.id}/',
                         data={'beat_title': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'beats.html')
        self.assertContains(response, 'You cant submit an empty beat')


    def test_post_redirects_to_beat_list_view(self):
        beat_list = BeatList.objects.create()
        another_beat_list = BeatList.objects.create()

        response = self.client.post(f'/beat_list/{beat_list.id}/',
                         data={'beat_title': 'Beat for adding beats to a list test'})

        self.assertRedirects(response, f'/beat_list/{beat_list.id}/')

class NewBeatListTest(TestCase):
    def test_add_new_beat_POST_request(self):
        self.client.post('/beat_list/new', data={'beat_title': 'Saawhitelife - Sin City Soul'})
        self.assertEqual(Beat.objects.count(), 1)
        new_beat = Beat.objects.first()
        self.assertEqual(new_beat.title, 'Saawhitelife - Sin City Soul')

    def test_redirects_after_post_request(self):
        response = self.client.post('/beat_list/new', data={'beat_title': 'Saawhitelife - Sin City Soul'})
        new_beat_list = BeatList.objects.first()
        self.assertRedirects(response, f'/beat_list/{new_beat_list.id}/')

    def test_empty_items_arent_saved(self):
        self.client.post('/beat_list/new', data={'beat_title': ''})
        self.assertEqual(BeatList.objects.count(), 0)
        self.assertEqual(Beat.objects.count(), 0)