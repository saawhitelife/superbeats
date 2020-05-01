from unittest import TestCase
from beats.forms import BeatForm, EMPTY_BEAT_ERROR, ExistingBeatListBeatForm, DUPLICATE_BEAT_ERROR
from beats.models import Beat, BeatList

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

    def test_form_saves_beat_to_a_beat_list(self):
        beat_list = BeatList.objects.create()
        form = BeatForm(data={'title': 'Beat for form test'})
        new_beat = form.save(for_beat_list=beat_list)
        self.assertEqual(new_beat, Beat.objects.first())
        self.assertEqual(new_beat.title, 'Beat for form test')
        self.assertEqual(new_beat.beat_list, beat_list)

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
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_BEAT_ERROR])