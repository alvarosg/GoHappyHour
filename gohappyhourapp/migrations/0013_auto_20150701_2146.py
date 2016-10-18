# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gohappyhourapp', '0012_auto_20150701_2051'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(null=True, upload_to=b'images/offers/fullsize', blank=True)),
                ('thumbnail', models.ImageField(null=True, upload_to=b'images/offers/thumbnails', blank=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('offer', models.ForeignKey(related_name='offerpictures', to='gohappyhourapp.Location')),
                ('owner', models.ForeignKey(related_name='offerpictures', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_published',),
            },
        ),
        migrations.RemoveField(
            model_name='offer',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='thumbnail',
        ),
    ]
