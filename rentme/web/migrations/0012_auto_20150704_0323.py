# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentme_web', '0011_auto_20150704_0302'),
    ]

    operations = [
        migrations.AddField(
            model_name='trademelistingphoto',
            name='plus_size',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='trademelistingphoto',
            name='full_size',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='trademelistingphoto',
            name='gallery',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='trademelistingphoto',
            name='large',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='trademelistingphoto',
            name='list',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='trademelistingphoto',
            name='medium',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='trademelistingphoto',
            name='thumbnail',
            field=models.URLField(null=True),
        ),
    ]
