# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-28 06:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flutter', '0003_remove_info_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='transactionReference',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
