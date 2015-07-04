# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentme_web', '0010_auto_20150704_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trademelisting',
            name='available_from',
            field=models.TextField(null=True),
        ),
    ]
