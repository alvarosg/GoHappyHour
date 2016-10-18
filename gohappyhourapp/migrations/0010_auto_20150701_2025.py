# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gohappyhourapp', '0009_auto_20150701_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationpicture',
            name='location',
            field=models.ForeignKey(related_name='pictures', to='gohappyhourapp.Location'),
        ),
    ]
