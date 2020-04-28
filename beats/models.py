from django.db import models
from django.urls import reverse

class BeatList(models.Model):
    def get_absolute_url(self):
        return reverse('beat_list',
                       args=[self.id])

class Beat(models.Model):
    title = models.TextField(default='')
    beat_list = models.ForeignKey(BeatList, default=None)