# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gohappyhourapp', '0008_auto_20150625_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(null=True, upload_to=b'images/locations/fullsize', blank=True)),
                ('thumbnail', models.ImageField(null=True, upload_to=b'images/locations/thumbnails', blank=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('date_published',),
            },
        ),
        migrations.AlterModelOptions(
            name='offerusercomment',
            options={'ordering': ('-date_edited',)},
        ),
        migrations.RemoveField(
            model_name='location',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='location',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='location',
            name='thumbnail',
        ),
        migrations.AddField(
            model_name='locationpicture',
            name='location',
            field=models.ForeignKey(related_name='pictures', to='gohappyhourapp.Location', unique=True),
        ),
        migrations.AddField(
            model_name='locationpicture',
            name='owner',
            field=models.ForeignKey(related_name='pictures', to=settings.AUTH_USER_MODEL),
        ),
    ]
