# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-06 05:00
from __future__ import unicode_literals

from django.db import migrations, models


def migrate(apps, editor):
    Song = apps.get_model('boards', 'Song')
    for s in Song.objects.all():
        res = s.votes.aggregate(models.Avg('score'))
        s.score = res['score__avg'] or 0
        s.save()

class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0008_merge_20170605_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='score',
            field=models.FloatField(default=0.0),
        ),
        migrations.RunPython(migrate, reverse_code=migrations.RunPython.noop),
    ]