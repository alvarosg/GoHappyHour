# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gohappyhourapp', '0015_auto_20150703_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationpicture',
            name='origin',
            field=models.CharField(default=b'GHH', max_length=4, choices=[(b'GHH', b'Go Happy Hour'), (b'GP', b'Google Places'), (b'LNK', b'External Link')]),
        ),
        migrations.AddField(
            model_name='locationpicture',
            name='originid',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='offerpicture',
            name='origin',
            field=models.CharField(default=b'GHH', max_length=4, choices=[(b'GHH', b'Go Happy Hour'), (b'GP', b'Google Places'), (b'LNK', b'External Link')]),
        ),
        migrations.AddField(
            model_name='offerpicture',
            name='originid',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='locationpicture',
            unique_together=set([('origin', 'originid', 'location')]),
        ),
        migrations.AlterUniqueTogether(
            name='offerpicture',
            unique_together=set([('origin', 'originid', 'offer')]),
        ),
    ]
