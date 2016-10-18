# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gohappyhourapp', '0006_auto_20150623_2215'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferUserComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=500, null=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('date_published',),
            },
        ),
        migrations.RemoveField(
            model_name='offeruservote',
            name='comment',
        ),
        migrations.AlterField(
            model_name='offer',
            name='date_expire',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='description',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='offerusercomment',
            name='offer',
            field=models.ForeignKey(related_name='offerusercomments', to='gohappyhourapp.Offer'),
        ),
        migrations.AddField(
            model_name='offerusercomment',
            name='owner',
            field=models.ForeignKey(related_name='offerusercomments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='offerusercomment',
            unique_together=set([('offer', 'owner')]),
        ),
    ]
