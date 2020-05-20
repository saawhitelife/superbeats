from django.db import models
from django.urls import reverse
from django.conf import settings

class BeatList(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='beat_lists',
                              blank=True,
                              null=True)

    def get_absolute_url(self):
        return reverse('beat_list',
                       args=[self.id])

    @staticmethod
    def create_new(first_beat_title, owner=None):
        beat_list = BeatList.objects.create(owner=owner)
        Beat.objects.create(title=first_beat_title, beat_list=beat_list)
        return beat_list

    @property
    def name(self):
        return self.beat_set.first().title

class Beat(models.Model):
    title = models.TextField(default='')
    beat_list = models.ForeignKey(BeatList, default=None)

    class Meta:
        ordering = ('id',)
        unique_together = ('title', 'beat_list')

    def __str__(self):
        return self.title