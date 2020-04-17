from django.db import models

class BeatList(models.Model):
    pass

class Beat(models.Model):
    title = models.TextField(default='')
    beat_list = models.ForeignKey(BeatList, default=None)