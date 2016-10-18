# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gohappyhourapp', '0002_auto_20150609_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='originid',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='picture',
            field=models.ImageField(null=True, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='location',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to=b''),
        ),
    ]
