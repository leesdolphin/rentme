# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentme_web', '0006_auto_20150702_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trademelisting',
            name='agency',
            field=models.ManyToManyField(to='rentme_web.TradeMeAgency', null=True),
        ),
    ]
