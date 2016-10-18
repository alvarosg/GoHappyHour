# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gohappyhourapp', '0005_location_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'images/offers/fullsize', blank=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to=b'images/offers/thumbnails', blank=True),
        ),
    ]
