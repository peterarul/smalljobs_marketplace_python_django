# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-20 00:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smalljobsapp', '0004_purchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
