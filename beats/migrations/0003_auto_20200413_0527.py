# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2020-04-13 05:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beats', '0002_beat_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beat',
            old_name='text',
            new_name='title',
        ),
    ]
