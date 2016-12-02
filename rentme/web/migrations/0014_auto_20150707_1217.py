# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentme_web', '0013_auto_20150704_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyrating',
            name='property',
            field=models.OneToOneField(related_name='rating', to='rentme_web.TradeMeListing'),
        ),
        migrations.AlterUniqueTogether(
            name='trademelistingattribute',
            unique_together=set([('listing', 'name')]),
        ),
    ]
