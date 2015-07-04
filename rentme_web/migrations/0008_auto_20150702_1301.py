# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentme_web', '0007_auto_20150702_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trademelistinglocation',
            name='accuracy',
            field=models.IntegerField(choices=[(0, 'None'), (1, 'Address'), (3, 'Street'), (2, 'Suburb')]),
        ),
        migrations.AlterField(
            model_name='trademelistinglocation',
            name='latitude',
            field=models.DecimalField(decimal_places=8, max_digits=11),
        ),
        migrations.AlterField(
            model_name='trademelistinglocation',
            name='longitude',
            field=models.DecimalField(decimal_places=8, max_digits=11),
        ),
    ]
