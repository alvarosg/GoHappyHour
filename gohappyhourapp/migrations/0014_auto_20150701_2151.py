# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gohappyhourapp', '0013_auto_20150701_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerpicture',
            name='offer',
            field=models.ForeignKey(related_name='offerpictures', to='gohappyhourapp.Offer'),
        ),
    ]
