# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TraceMeAgencyAgent',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('full_name', models.TextField()),
                ('position', models.TextField()),
                ('mobile_number', models.CharField(max_length=20)),
                ('office_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('fax_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TradeMeAgency',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.TextField()),
                ('phone_number', models.CharField(max_length=20)),
                ('website', models.URLField()),
                ('logo', models.URLField()),
                ('is_real_estate_agency', models.BooleanField()),
                ('is_licensed_property_agency', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='TradeMeDistrict',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TradeMeListing',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('title', models.TextField()),
                ('category', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('generated_at', models.DateTimeField()),
                ('stored_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TradeMeListingLocation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('latitude', models.DecimalField(max_digits=11, decimal_places=8)),
                ('longitude', models.DecimalField(max_digits=11, decimal_places=8)),
                ('accuracy', models.IntegerField(choices=[(0, 'None'), (1, 'Address'), (3, 'Street'), (2, 'Suburb')])),
            ],
        ),
        migrations.CreateModel(
            name='TradeMeListingPhoto',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('thumbnail', models.URLField()),
                ('list', models.URLField()),
                ('medium', models.URLField()),
                ('gallery', models.URLField()),
                ('large', models.URLField()),
                ('full_size', models.URLField()),
                ('original_width', models.IntegerField()),
                ('original_height', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TradeMeListingPrice',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('value', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='TradeMeListingPricePeriods',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TradeMeListingProperty',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.TextField()),
                ('display_name', models.TextField()),
                ('value', models.TextField()),
                ('listing', models.ForeignKey(to='rentme_web.TradeMeListing', related_name='properties')),
            ],
        ),
        migrations.CreateModel(
            name='TradeMeLocality',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TradeMeMember',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('nickname', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('suburb', models.TextField()),
                ('region', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TradeMeSuburb',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.TextField(unique=True)),
                ('adjacent_suburbs', models.ManyToManyField(related_name='adjacent_suburbs_rel_+', to='rentme_web.TradeMeSuburb')),
                ('district', models.ForeignKey(to='rentme_web.TradeMeDistrict')),
            ],
        ),
        migrations.AddField(
            model_name='trademelistingprice',
            name='period',
            field=models.ForeignKey(to='rentme_web.TradeMeListingPricePeriods'),
        ),
        migrations.AddField(
            model_name='trademelisting',
            name='location',
            field=models.ForeignKey(to='rentme_web.TradeMeListingLocation'),
        ),
        migrations.AddField(
            model_name='trademelisting',
            name='member',
            field=models.ForeignKey(to='rentme_web.TradeMeMember'),
        ),
        migrations.AddField(
            model_name='trademelisting',
            name='photos',
            field=models.ManyToManyField(to='rentme_web.TradeMeListingPhoto'),
        ),
        migrations.AddField(
            model_name='trademelisting',
            name='price',
            field=models.ForeignKey(to='rentme_web.TradeMeListingPrice'),
        ),
        migrations.AddField(
            model_name='trademedistrict',
            name='locality',
            field=models.ForeignKey(to='rentme_web.TradeMeLocality'),
        ),
        migrations.AddField(
            model_name='tracemeagencyagent',
            name='agency',
            field=models.ForeignKey(to='rentme_web.TradeMeAgency', related_name='agents'),
        ),
    ]
