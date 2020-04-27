from django.test import TestCase
from beats.models import Beat, BeatList
from django.core.exceptions import ValidationError


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

    def test_cannot_save_empty_beats(self):
        beat_list = BeatList.objects.create()
        beat = Beat.objects.create(beat_list=beat_list, title='')
        with self.assertRaises(ValidationError):
            beat.save()
            beat.full_clean()