# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 11:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20170622_1141'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='flatmateinformation',
            unique_together=set([('current_flatmates', 'flatmates')]),
        ),
    ]