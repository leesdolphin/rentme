# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 23:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('web', '0025_auto_20170211_0611'),
        ('data', '0002_auto_20170401_1004')
    ]

    operations = [
        migrations.RemoveField(
            model_name='agencyagent',
            name='agency',
        ),
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='district',
            name='locality',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='agency',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='attributes',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='broadband_technologies',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='category',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='geographic_location',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='member',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photos',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='suburb',
        ),
        migrations.RemoveField(
            model_name='membershipdistrict',
            name='locality',
        ),
        migrations.RemoveField(
            model_name='suburb',
            name='adjacent_suburbs',
        ),
        migrations.RemoveField(
            model_name='suburb',
            name='district',
        ),
        migrations.DeleteModel(
            name='Agency',
        ),
        migrations.DeleteModel(
            name='AgencyAgent',
        ),
        migrations.DeleteModel(
            name='Attributes',
        ),
        migrations.DeleteModel(
            name='BroadbandTechnology',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='District',
        ),
        migrations.DeleteModel(
            name='GeographicLocation',
        ),
        migrations.DeleteModel(
            name='Listing',
        ),
        migrations.DeleteModel(
            name='Locality',
        ),
        migrations.DeleteModel(
            name='Member',
        ),
        migrations.DeleteModel(
            name='MembershipDistrict',
        ),
        migrations.DeleteModel(
            name='MembershipLocality',
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
        migrations.DeleteModel(
            name='Suburb',
        ),
    ]
