# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gohappyhourapp', '0004_auto_20150609_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='website',
            field=models.URLField(null=True, blank=True),
        ),
    ]
