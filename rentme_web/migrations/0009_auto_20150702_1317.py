# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentme_web', '0008_auto_20150702_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trademelisting',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='trademelisting',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
