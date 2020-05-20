from django.test import TestCase
from beats.models import Beat, BeatList
from beats.forms import BeatForm, EMPTY_BEAT_ERROR, ExistingBeatListBeatForm, DUPLICATE_BEAT_ERROR
from django.contrib.auth import get_user_model
from unittest import skip
from unittest.mock import patch, Mock
from django.http import HttpRequest
from beats.views import new_beat_list
import unittest

User = get_user_model()


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_add_new_beat_POST_request(self):
        response = self.client.post('/beat_list/new', data={'title': 'Saawhitelife - Sin City Soul'})

        self.assertEqual(Beat.objects.count(), 1)
        new_beat = Beat.objects.first()
        self.assertEqual(new_beat.title, 'Saawhitelife - Sin City Soul')

    def test_home_page_uses_correct_form_model(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], BeatForm)


class BeatsViewTest(TestCase):
    def post_invalid_input(self):
        beat_list = BeatList.objects.create()
        return self.client.post(f'/beat_list/{beat_list.id}/',
                                data={'title': ''})

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
                data={'title': 'Beat for adding beats to a list test'})

        self.assertEqual(Beat.objects.count(), 1)

        new_beat = Beat.objects.first()
        self.assertEqual(new_beat.title, 'Beat for adding beats to a list test')
        self.assertEqual(new_beat.beat_list, beat_list)

    def test_post_redirects_to_beat_list_view(self):
        beat_list = BeatList.objects.create()
        another_beat_list = BeatList.objects.create()

        response = self.client.post(f'/beat_list/{beat_list.id}/',
                         data={'title': 'Beat for adding beats to a list test'})

        self.assertRedirects(response, f'/beat_list/{beat_list.id}/')

    def test_view_contains_beat_form(self):
        beat_list = BeatList.objects.create()
        beat = Beat.objects.create(title='Beat for test', beat_list=beat_list)
        response = self.client.get(f'/beat_list/{beat_list.id}/')
        self.assertIsInstance(response.context['form'], ExistingBeatListBeatForm)
        self.assertContains(response, 'name="title"')

    def test_invalid_input_isnt_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Beat.objects.count(), 0)

    def test_invalid_input_returns_to_beats_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'beats.html')

    def test_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingBeatListBeatForm)

    def test_invalid_input_shows_errors_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, EMPTY_BEAT_ERROR)

    def test_duplicates_error_ends_up_on_beat_list_page(self):
        beat_list = BeatList.objects.create()
        beat = Beat.objects.create(title='Beat 1', beat_list=beat_list)
        response = self.client.post(f'/beat_list/{beat_list.id}/',
                                    data={'title': 'Beat 1'}, follow=True)

        self.assertContains(response, DUPLICATE_BEAT_ERROR)
        self.assertTemplateUsed(response, 'beats.html')
        self.assertEqual(Beat.objects.count(), 1)

class NewBeatListViewIntegratedTest(TestCase):
    def test_add_new_beat_POST_request(self):
        self.client.post('/beat_list/new', data={'title': 'Saawhitelife - Sin City Soul'})
        self.assertEqual(Beat.objects.count(), 1)
        new_beat = Beat.objects.first()
        self.assertEqual(new_beat.title, 'Saawhitelife - Sin City Soul')

    def test_no_items_saved_on_invalid_input_and_errors_are_shown(self):
        response = self.client.post('/beat_list/new', data={'title': ''})
        self.assertEqual(BeatList.objects.count(), 0)
        self.assertContains(response, EMPTY_BEAT_ERROR)

    def test_beat_list_is_saved_for_authenticated_user(self):
        user = User.objects.create(email='a@b.c')
        self.client.force_login(user)
        self.client.post('/beat_list/new', data={'title': 'Saawhitelife - Catharsis'})
        beat_list = BeatList.objects.first()
        self.assertEqual(beat_list.owner, user)

@patch('beats.views.NewBeatListForm')
class NewBeatListViewUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.request = HttpRequest()
        self.request.POST['title'] = 'Saawhitelife - Grimoire'
        self.request.user = Mock()

    def test_view_passes_post_data_to_NewBeatListForm(self, mockNewBeatListForm):
        new_beat_list(self.request)
        mockNewBeatListForm.assert_called_once_with(data=self.request.POST)

    def test_form_saves_owner_if_valid(self, mockNewBeatListForm):
        mock_form = mockNewBeatListForm.return_value
        mock_form.is_valid.return_value = True
        new_beat_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('beats.views.redirect')
    def test_redirect_to_object_saved_by_form_if_valid(self,
        mockRedirect,
        mockNewBeatListForm
    ):
        mock_form = mockNewBeatListForm.return_value
        mock_form.is_valid.return_value = True

        response = new_beat_list(self.request)

        self.assertEqual(mockRedirect.return_value, response)
        mockRedirect.assert_called_once_with(mock_form.save.return_value)

    @patch('beats.views.render')
    def test_redirects_to_home_page_if_form_is_invalid(self,
        mockRender,
        mockNewBeatListForm
    ):
        mock_form = mockNewBeatListForm.return_value
        mock_form.is_valid.return_value = False

        response = new_beat_list(self.request)
        self.assertEqual(response, mockRender.return_value)
        mockRender.assert_called_once_with(
            self.request, 'home.html', {'form': mock_form}
        )

    def test_form_does_not_save_if_is_not_valid(self,
        mockNewBeatListForm
    ):
        mock_form = mockNewBeatListForm.return_value
        mock_form.is_valid.return_value = False
        new_beat_list(self.request)
        self.assertFalse(mock_form.save.called)



class MyBeatListTest(TestCase):
    def test_my_beat_list_url_renders_my_beat_list_template(self):
        User.objects.create(email='a@b.c')
        response = self.client.get('/beat_list/users/a@b.c/')
        self.assertTemplateUsed(response, 'my_beat_lists.html')

    def test_my_beat_lists_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@email.com')
        correct_user = User.objects.create(email='correct@email.com')
        response = self.client.get('/beat_list/users/correct@email.com/')
        self.assertEqual(response.context['owner'], correct_user)


