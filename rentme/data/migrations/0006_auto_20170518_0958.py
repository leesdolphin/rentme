# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-18 09:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import rentme.data.models._utils
import trademe.models.enums

class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20170429_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListingPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dollars', models.IntegerField()),
                ('period', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='price',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.ListingPrice'),
        ),
    ]
