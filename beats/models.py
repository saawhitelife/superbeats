from django.db import models

class Beat(models.Model):
    title = models.TextField(default='')