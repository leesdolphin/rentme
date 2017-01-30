# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 12:44
from __future__ import unicode_literals

from django.db import migrations
import rentme.web.models._utils
import trademe.models.enums


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_auto_20170130_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='allows_pickups',
            field=rentme.web.models._utils.EnumIntegerField(enum=trademe.models.enums.AllowsPickups),
        ),
    ]
