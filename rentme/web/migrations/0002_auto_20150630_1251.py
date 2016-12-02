# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentme_web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trademedistrict',
            name='locality',
            field=models.ForeignKey(to='rentme_web.TradeMeLocality', related_name='districts'),
        ),
        migrations.AlterField(
            model_name='trademedistrict',
            name='name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='trademelocality',
            name='name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='trademesuburb',
            name='district',
            field=models.ForeignKey(to='rentme_web.TradeMeDistrict', related_name='suburbs'),
        ),
        migrations.AlterField(
            model_name='trademesuburb',
            name='name',
            field=models.TextField(),
        ),
    ]
