# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 12:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rateMyCourse', '0004_auto_20171030_2027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='department',
        ),
        migrations.RemoveField(
            model_name='user',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='user',
            name='reported',
        ),
        migrations.RemoveField(
            model_name='user',
            name='school',
        ),
    ]
