# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gohappyhourapp', '0003_auto_20150609_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'images/locations/fullsize', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to=b'images/locations/thumbnails', blank=True),
        ),
    ]
