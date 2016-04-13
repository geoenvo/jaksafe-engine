# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FloodEvent',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('unit', models.CharField(max_length=255)),
                ('village', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('rt', models.CharField(max_length=255)),
                ('rw', models.CharField(max_length=255)),
                ('depth', models.IntegerField()),
                ('report_time', models.DateTimeField()),
                ('request_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'fl_event',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FloodEventRaw',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('unit', models.CharField(max_length=255)),
                ('village', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('rt', models.CharField(max_length=255)),
                ('rw', models.CharField(max_length=255)),
                ('depth', models.IntegerField()),
                ('report_time', models.DateTimeField()),
                ('request_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'fl_event_raw',
            },
            bases=(models.Model,),
        ),
    ]
