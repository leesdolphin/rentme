# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 10:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_auto_20170630_0633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='photo',
            field=models.ForeignKey(help_text='A collection of photos for the listing.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='data.Photo'),
        ),
    ]
