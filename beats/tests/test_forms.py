from unittest import TestCase
from beats.forms import BeatForm, EMPTY_BEAT_ERROR
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