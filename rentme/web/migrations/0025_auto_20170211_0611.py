# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-11 06:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0024_auto_20170211_0402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geographiclocation',
            name='easting',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='geographiclocation',
            name='northing',
            field=models.IntegerField(default=-1),
        ),
    ]