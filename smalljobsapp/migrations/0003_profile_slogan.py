# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-18 22:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smalljobsapp', '0002_gig'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='slogan',
            field=models.CharField(default='My slogan', max_length=500),
            preserve_default=False,
        ),
    ]
