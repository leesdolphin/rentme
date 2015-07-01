# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentme_web', '0002_auto_20150630_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='trademelisting',
            name='thumbnail_href',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='trademelisting',
            name='member',
            field=models.ForeignKey(null=True, to='rentme_web.TradeMeMember'),
        ),
        migrations.AlterField(
            model_name='trademelistinglocation',
            name='accuracy',
            field=models.IntegerField(unique=True, choices=[(0, 'None'), (1, 'Address'), (3, 'Street'), (2, 'Suburb')]),
        ),
        migrations.AlterField(
            model_name='trademelistinglocation',
            name='latitude',
            field=models.DecimalField(unique=True, max_digits=11, decimal_places=8),
        ),
        migrations.AlterField(
            model_name='trademelistinglocation',
            name='longitude',
            field=models.DecimalField(unique=True, max_digits=11, decimal_places=8),
        ),
        migrations.AlterField(
            model_name='trademelistingprice',
            name='period',
            field=models.ForeignKey(unique=True, to='rentme_web.TradeMeListingPricePeriods'),
        ),
        migrations.AlterField(
            model_name='trademelistingprice',
            name='value',
            field=models.DecimalField(unique=True, max_digits=10, decimal_places=2),
        ),
    ]
