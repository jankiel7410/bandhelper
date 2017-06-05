# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-05 15:39
from __future__ import unicode_literals

from django.db import migrations

from django.db import migrations


def migrate(apps, editor):
    List = apps.get_model('boards', 'List')
    List.objects.filter(name='Propositions').update(position=0)
    List.objects.filter(name='To try').update(position=1)
    List.objects.filter(name='Accepted').update(position=2)


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0006_auto_20170604_2029'),
    ]

    operations = [
        migrations.RunPython(migrate, reverse_code=migrations.RunPython.noop)
    ]
