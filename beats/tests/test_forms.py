from unittest import TestCase
from beats.forms import BeatForm, EMPTY_BEAT_ERROR

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
