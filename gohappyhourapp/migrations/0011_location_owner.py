# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gohappyhourapp', '0010_auto_20150701_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='owner',
            field=models.ForeignKey(related_name='locations', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
