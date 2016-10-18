# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('postcode', models.CharField(max_length=200, null=True)),
                ('country', models.CharField(max_length=200, null=True)),
                ('phonenumber', models.CharField(max_length=200, null=True)),
                ('timezoneid', models.CharField(max_length=50, null=True)),
                ('picture', models.CharField(max_length=200, null=True)),
                ('thumbnail', models.CharField(max_length=200, null=True)),
                ('origin', models.CharField(default=b'GHH', max_length=4, choices=[(b'GHH', b'Go Happy Hour'), (b'GP', b'Google Places')])),
                ('originid', models.CharField(max_length=100, null=True)),
                ('owner', models.ForeignKey(related_name='locations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_published',),
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500, null=True)),
                ('score', models.IntegerField(default=0)),
                ('votes', models.IntegerField(default=0)),
                ('date_expire', models.DateField(null=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('location', models.ForeignKey(related_name='offers', to='gohappyhourapp.Location')),
                ('owner', models.ForeignKey(related_name='offers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_published',),
            },
        ),
        migrations.CreateModel(
            name='OfferTimeRange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weekdays', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(regex=b'^[01]{7}$')])),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('offer', models.ForeignKey(related_name='offertimeranges', to='gohappyhourapp.Offer')),
                ('owner', models.ForeignKey(related_name='offertimeranges', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_published',),
            },
        ),
        migrations.CreateModel(
            name='OfferUserVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=500, null=True)),
                ('value', models.IntegerField()),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('offer', models.ForeignKey(related_name='offeruservotes', to='gohappyhourapp.Offer')),
                ('owner', models.ForeignKey(related_name='offeruservotes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_published',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='offeruservote',
            unique_together=set([('offer', 'owner')]),
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([('origin', 'originid')]),
        ),
    ]
