# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-10 09:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import rentme.data.models._utils
import trademe.models.enums


class Migration(migrations.Migration):

    dependencies = [
        ('raw', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('area_of_business', rentme.data.models._utils.EnumIntegerField(enum=trademe.models.enums.AreaOfBusiness, help_text='Area of business this category is related to', null=True)),
                ('can_be_second_category', models.NullBooleanField(help_text='Indicates whether this category can be selected as a second category.')),
                ('can_have_second_category', models.NullBooleanField(help_text='Indicates whether this category can be paired with a second category.')),
                ('count', models.IntegerField(help_text='The number of items for sale in this category.', null=True)),
                ('has_classifieds', models.NullBooleanField(help_text='Indicates whether classifieds are allowed in this category.')),
                ('has_legal_notice', models.NullBooleanField(help_text='Indicates whether the category has legal requirements. You should ask the user to accept the legal notice before listing in this category. There is an API to get the text of the legal notice.')),
                ('is_restricted', models.NullBooleanField(help_text='Indicates whether the category is restricted to adults only (i.e. the category is R18).')),
                ('name', models.TextField(help_text='The name of the category.', null=True)),
                ('number', models.TextField(help_text='A unique identifier for the category e.g. “0004-0369-6076-“. We plan to change this to a numeric identifier (e.g. “6076”) so you should ensure you can cope with both formats.', primary_key=True, serialize=False)),
                ('path', models.TextField(help_text='The full URL path of this category e.g. “/Home-living/Beds-bedroom-furniture/Bedside-tables”.', null=True)),
                ('parent', models.ForeignKey(help_text='The list of subcategories belonging to this category.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='raw.Category')),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('district_id', models.IntegerField(help_text='The ID of the district.', primary_key=True, serialize=False)),
                ('name', models.TextField(help_text='The name of the district.', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('locality_id', models.IntegerField(help_text='The ID of the region.', primary_key=True, serialize=False)),
                ('name', models.TextField(help_text='The name of the region.', null=True)),
                ('districts', models.ManyToManyField(help_text='The list of districts that belong to this region.', related_name='localities', to='raw.District')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MembershipDistrict',
            fields=[
                ('district_id', models.IntegerField(help_text='The ID of the district.', primary_key=True, serialize=False)),
                ('name', models.TextField(help_text='The name of the district.', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MembershipLocality',
            fields=[
                ('locality_id', models.IntegerField(help_text='The ID of the region.', primary_key=True, serialize=False)),
                ('name', models.TextField(help_text='The name of the region.', null=True)),
                ('districts', models.ManyToManyField(help_text='The list of districts that belong to this region.', related_name='localities', to='raw.MembershipDistrict')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Suburb',
            fields=[
                ('name', models.TextField(help_text='The name of the suburb.', null=True)),
                ('suburb_id', models.IntegerField(help_text='The ID of the suburb.', primary_key=True, serialize=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SuburbAdjacentSuburbs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='suburbadjacentsuburbs',
            unique_together=set([('value',)]),
        ),
        migrations.AddField(
            model_name='suburb',
            name='adjacent_suburbs',
            field=models.ManyToManyField(help_text='A list containing the IDs of the suburbs adjacent to this suburb.', related_name='suburb_reverse_adjacent_suburbs', to='raw.SuburbAdjacentSuburbs'),
        ),
        migrations.AddField(
            model_name='district',
            name='suburbs',
            field=models.ManyToManyField(help_text='The list of suburbs that belong to this district.', related_name='district_reverse_suburbs', to='raw.Suburb'),
        ),
    ]
