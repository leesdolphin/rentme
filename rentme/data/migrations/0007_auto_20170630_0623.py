# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 06:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20170625_1028'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='flatmate_info',
            new_name='flatmate_information',
        ),
    ]
