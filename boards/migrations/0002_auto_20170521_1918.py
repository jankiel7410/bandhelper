# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-21 19:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='proposed_songs',
        ),
        migrations.RemoveField(
            model_name='list',
            name='song',
        ),
        migrations.AddField(
            model_name='list',
            name='position',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='list',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='boards.List'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='list',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lists', to='boards.Board'),
        ),
    ]
