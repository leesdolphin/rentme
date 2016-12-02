# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentme_web', '0005_auto_20150702_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='trademelisting',
            name='address',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trademelisting',
            name='available_from',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trademelisting',
            name='bathrooms',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trademelisting',
            name='bedrooms',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
