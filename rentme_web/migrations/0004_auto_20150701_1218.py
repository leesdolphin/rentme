# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentme_web', '0003_auto_20150701_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='trademelisting',
            name='agencies',
            field=models.ManyToManyField(to='rentme_web.TradeMeAgency'),
        ),
        migrations.AlterField(
            model_name='trademelistingprice',
            name='period',
            field=models.ForeignKey(to='rentme_web.TradeMeListingPricePeriods'),
        ),
        migrations.AlterField(
            model_name='trademelistingprice',
            name='value',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        migrations.AlterUniqueTogether(
            name='trademelistinglocation',
            unique_together=set([('latitude', 'longitude', 'accuracy')]),
        ),
        migrations.AlterUniqueTogether(
            name='trademelistingprice',
            unique_together=set([('value', 'period')]),
        ),
    ]
