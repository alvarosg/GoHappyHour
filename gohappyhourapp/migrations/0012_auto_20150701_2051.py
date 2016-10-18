# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('gohappyhourapp', '0011_location_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationpicture',
            name='location',
            field=models.ForeignKey(related_name='locationpictures', to='gohappyhourapp.Location'),
        ),
        migrations.AlterField(
            model_name='locationpicture',
            name='owner',
            field=models.ForeignKey(related_name='locationpictures', to=settings.AUTH_USER_MODEL),
        ),
    ]
