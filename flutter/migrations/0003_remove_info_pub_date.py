# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-27 13:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flutter', '0002_auto_20161026_2150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='info',
            name='pub_date',
        ),
    ]
