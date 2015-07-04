# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentme_web', '0004_auto_20150701_1218'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='trademelistingprice',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='trademelistingprice',
            name='period',
        ),
        migrations.RenameField(
            model_name='trademelisting',
            old_name='agencies',
            new_name='agency',
        ),
        migrations.RemoveField(
            model_name='trademelisting',
            name='price',
        ),
        migrations.AddField(
            model_name='trademelisting',
            name='rent_per_week',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tracemeagencyagent',
            name='email',
            field=models.EmailField(null=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='tracemeagencyagent',
            name='fax_number',
            field=models.CharField(null=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='tracemeagencyagent',
            name='mobile_number',
            field=models.CharField(null=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='tracemeagencyagent',
            name='office_number',
            field=models.CharField(null=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='tracemeagencyagent',
            name='position',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='trademeagency',
            name='logo',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='trademeagency',
            name='phone_number',
            field=models.CharField(null=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='trademeagency',
            name='website',
            field=models.URLField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name='tracemeagencyagent',
            unique_together=set([('agency', 'full_name')]),
        ),
        migrations.DeleteModel(
            name='TradeMeListingPrice',
        ),
        migrations.DeleteModel(
            name='TradeMeListingPricePeriods',
        ),
    ]
