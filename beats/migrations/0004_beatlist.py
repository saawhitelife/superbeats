# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2020-04-17 05:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beats', '0003_auto_20200413_0527'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeatList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
