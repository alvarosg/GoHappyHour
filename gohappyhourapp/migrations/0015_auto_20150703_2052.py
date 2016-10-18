# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('gohappyhourapp', '0014_auto_20150701_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offertimerange',
            name='weekdays',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(regex=b'^(?=.*[1])[01]{7}$')]),
        ),
    ]
