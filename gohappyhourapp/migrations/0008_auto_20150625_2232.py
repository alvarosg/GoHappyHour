# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gohappyhourapp', '0007_auto_20150625_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='address',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='country',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='postcode',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
