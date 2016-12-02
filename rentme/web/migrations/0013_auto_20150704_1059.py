# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentme_web', '0012_auto_20150704_0323'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeMeListingAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.TextField()),
                ('display_name', models.TextField()),
                ('value', models.TextField()),
                ('listing', models.ForeignKey(to='rentme_web.TradeMeListing', related_name='attributes')),
            ],
        ),
        migrations.RemoveField(
            model_name='trademelistingproperty',
            name='listing',
        ),
        migrations.DeleteModel(
            name='TradeMeListingProperty',
        ),
    ]
