# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentme_web', '0009_auto_20150702_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyRating',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('rating', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='trademelisting',
            name='agency',
            field=models.ManyToManyField(to='rentme_web.TradeMeAgency'),
        ),
        migrations.AddField(
            model_name='propertyrating',
            name='property',
            field=models.OneToOneField(to='rentme_web.TradeMeListing'),
        ),
    ]
