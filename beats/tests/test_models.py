from django.test import TestCase
from beats.models import Beat, BeatList
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class BeatListModelTest(TestCase):
    def test_get_absolute_url(self):
        beat_list = BeatList.objects.create()
        self.assertEqual(beat_list.get_absolute_url(), f'/beat_list/{beat_list.id}/')

    def test_create_new_creates_beat_list_and_first_beat(self):
        beat_list = BeatList.create_new(first_beat_title='Saawhitelife - Grimoire')
        new_beat = Beat.objects.first()
        self.assertEqual(new_beat.title, 'Saawhitelife - Grimoire')
        new_beat_list = BeatList.objects.first()
        self.assertEqual(new_beat.beat_list, new_beat_list)

    def test_create_new_optionally_saves_owner(self):
        user = User.objects.create()
        BeatList.create_new(first_beat_title='Saawhitelife - Catharsis',
                            owner=user)
        new_list = BeatList.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_beat_lists_can_have_owners(self):
        BeatList(owner=User())

    def test_beat_list_owner_is_optional(self):
        BeatList().full_clean()

    def test_create_returns_new_list_object(self):
        created = BeatList.create_new(first_beat_title='Saawhitelife - Catharsis')
        beat_list = BeatList.objects.first()
        self.assertEqual(created, beat_list)

    def test_first_beat_title_in_beat_list_will_be_beat_list_name(self):
        beat_list = BeatList.objects.create()
        Beat.objects.create(title='Saawhitelife - Fata Morgana', beat_list=beat_list)
        Beat.objects.create(title='Saawhitelife - Catharsis', beat_list=beat_list)
        self.assertEqual(beat_list.name, 'Saawhitelife - Fata Morgana')

class BeatModelsTest(TestCase):
    def test_default_beat_title(self):
        beat = Beat()
        self.assertEqual(beat.title, '')

    def test_beat_related_to_beat_list(self):
        beat_list = BeatList.objects.create()
        beat = Beat()
        beat.beat_list = beat_list
        beat.save()
        self.assertIn(beat, beat_list.beat_set.all())

    def test_cannot_save_empty_beats(self):
        beat_list = BeatList.objects.create()
        beat = Beat.objects.create(beat_list=beat_list, title='')
        with self.assertRaises(ValidationError):
            beat.save()
            beat.full_clean()

    def test_raises_validation_error_on_duplicates(self):
        beat_list = BeatList.objects.create()
        beat = Beat.objects.create(title='Beat 1', beat_list=beat_list)
        with self.assertRaises(ValidationError):
            beat = Beat(title='Beat 1', beat_list=beat_list)
            beat.full_clean()
            # beat.save()

    def test_can_save_same_item_to_another_list(self):
        beat_list = BeatList.objects.create()
        beat_list2 = BeatList.objects.create()
        Beat.objects.create(title='Beat 1', beat_list=beat_list)
        beat2 = Beat(title='Beat 1', beat_list=beat_list2)
        beat2.full_clean()

    def test_beat_list_ordering(self):
        beat_list = BeatList.objects.create()
        beat1 = Beat.objects.create(title='Beat 1', beat_list=beat_list)
        beat2 = Beat.objects.create(title='Beat 2', beat_list=beat_list)
        beat3 = Beat.objects.create(title='Beat 3', beat_list=beat_list)
        self.assertEqual(list(Beat.objects.all()),
                         [beat1, beat2, beat3])

    def test_string_representation(self):
        beat_list = BeatList.objects.create()
        beat = Beat.objects.create(title='Beat 1', beat_list=beat_list)
        self.assertEqual(str(beat), 'Beat 1')

