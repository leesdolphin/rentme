# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentme_web', '0014_auto_20150707_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyReview',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('rating', models.PositiveSmallIntegerField()),
                ('property', models.OneToOneField(related_name='review', to='rentme_web.TradeMeListing')),
            ],
        ),
        migrations.RemoveField(
            model_name='propertyrating',
            name='property',
        ),
        migrations.DeleteModel(
            name='PropertyRating',
        ),
    ]
