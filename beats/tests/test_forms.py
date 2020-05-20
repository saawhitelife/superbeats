from django.test import TestCase
from beats.forms import BeatForm, EMPTY_BEAT_ERROR, ExistingBeatListBeatForm, DUPLICATE_BEAT_ERROR, NewBeatListForm
from beats.models import Beat, BeatList
import unittest
from unittest.mock import patch, Mock


class BeatFormTest(TestCase):
    def test_form_contains_beat_title_input(self):
        form = BeatForm()
        self.assertIn('placeholder="Enter new beat name"', form.as_p())
        self.assertIn('class="form-control input-lg', form.as_p())

    def test_blank_field_validation(self):
        form = BeatForm(data={'title': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'],
                         [EMPTY_BEAT_ERROR])


class ExistingBeatListBeatFormTest(TestCase):
    def test_form_contains_beat_title_input(self):
        beat_list = BeatList.objects.create()
        form = ExistingBeatListBeatForm(for_beat_list=beat_list)
        self.assertIn('placeholder="Enter new beat name"', form.as_p())
        self.assertIn('class="form-control input-lg', form.as_p())

    def test_blank_field_validation(self):
        beat_list = BeatList.objects.create()
        form = ExistingBeatListBeatForm(for_beat_list=beat_list, data={'title': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'],
                         [EMPTY_BEAT_ERROR])

    def test_form_validation_for_duplicate_items(self):
        beat_list = BeatList.objects.create()
        Beat.objects.create(title='Beat for duplicate test', beat_list=beat_list)
        form = ExistingBeatListBeatForm(data={'title': 'Beat for duplicate test'}, for_beat_list=beat_list)
        form2 = ExistingBeatListBeatForm(data={'title': 'Beat for duplicate test 2'}, for_beat_list=beat_list)
        form2.save()

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], [DUPLICATE_BEAT_ERROR])

    def test_form_saves_beat(self):
        beat_list = BeatList.objects.create()
        form = ExistingBeatListBeatForm(data={'title': 'Beat for form save test'}, for_beat_list=beat_list)
        beat = form.save()
        for beat in beat_list.beat_set.all():
            print(beat.title)
        self.assertEqual(beat, Beat.objects.all()[0])

class NewBeatListFormTest(unittest.TestCase):
    @patch('beats.forms.BeatList.create_new')
    def test_creates_new_list_if_user_is_not_authenticated(self,
        mock_BeatList_create_new
    ):
        user = Mock(is_authenticated=False)
        form = NewBeatListForm(data={'title': 'Saawhitelife - Grimoire'})
        form.is_valid()
        form.save(owner=user)
        mock_BeatList_create_new.assert_called_once_with(
            first_beat_title='Saawhitelife - Grimoire'
        )

    @patch('beats.forms.BeatList.create_new')
    def test_creates_new_list_if_user_is_authenticated(self,
        mock_BeatList_create_new
    ):
        user = Mock(is_authenticated=True)
        form = NewBeatListForm(data={'title': 'Saawhitelife - Grimoire'})
        form.is_valid()
        form.save(owner=user)
        mock_BeatList_create_new.assert_called_once_with(
            first_beat_title='Saawhitelife - Grimoire',
            owner=user
        )

    @patch('beats.forms.BeatList.create_new')
    def test_form_create_new_returns_new_list_objects(self,
        mock_BeatList_create_new
    ):
        user = Mock(is_authenticated = True)
        form = NewBeatListForm(data={'title': 'Saawhitelife - Hard Rain'})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(mock_BeatList_create_new.return_value, response)
