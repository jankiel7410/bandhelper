# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-04 20:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0005_auto_20170604_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='board_memberships', to='boards.Board')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='board_memberships', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='board',
            name='members',
            field=models.ManyToManyField(related_name='shared_boards', through='boards.BoardMembership', to=settings.AUTH_USER_MODEL),
        ),
    ]