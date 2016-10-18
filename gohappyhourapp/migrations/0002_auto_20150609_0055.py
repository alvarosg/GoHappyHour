# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gohappyhourapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='originid',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
