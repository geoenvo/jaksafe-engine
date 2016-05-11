# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import report.models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoCalcDaily',
            fields=[
                ('id', report.models.UnsignedAutoField(serialize=False, primary_key=True)),
                ('id_event', models.PositiveIntegerField(null=True)),
                ('from_date', models.DateTimeField()),
                ('to_date', models.DateTimeField()),
                ('day', models.PositiveIntegerField(null=True)),
                ('loss', models.DecimalField(null=True, max_digits=17, decimal_places=2)),
            ],
            options={
                'db_table': 'auto_calc_daily',
            },
            bases=(models.Model,),
        ),
    ]
