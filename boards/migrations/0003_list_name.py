# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-21 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20170521_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]