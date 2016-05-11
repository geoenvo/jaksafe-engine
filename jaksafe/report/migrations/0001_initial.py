# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import report.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdHocCalc',
            fields=[
                ('id', report.models.UnsignedAutoField(serialize=False, primary_key=True)),
                ('id_event', models.PositiveIntegerField(null=True)),
                ('id_user', models.IntegerField(null=True)),
                ('id_user_group', models.IntegerField(null=True)),
                ('t0', models.DateTimeField()),
                ('t1', models.DateTimeField()),
                ('damage', models.DecimalField(null=True, max_digits=17, decimal_places=2)),
                ('loss', models.DecimalField(null=True, max_digits=17, decimal_places=2)),
            ],
            options={
                'db_table': 'adhoc_calc',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdhocResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_event', models.IntegerField()),
                ('sector', models.CharField(max_length=200)),
                ('subsector', models.CharField(max_length=200)),
                ('asset', models.CharField(max_length=200)),
                ('rw', models.CharField(max_length=3)),
                ('kelurahan', models.CharField(max_length=50)),
                ('kecamatan', models.CharField(max_length=50)),
                ('kota', models.CharField(max_length=50)),
                ('kelas', models.CharField(max_length=50)),
                ('damage', models.DecimalField(max_digits=17, decimal_places=2)),
                ('loss', models.DecimalField(max_digits=17, decimal_places=2)),
            ],
            options={
                'db_table': 'adhoc_dala_result',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AutoCalc',
            fields=[
                ('id', report.models.UnsignedAutoField(serialize=False, primary_key=True)),
                ('id_event', models.PositiveIntegerField(null=True)),
                ('t0', models.DateTimeField()),
                ('t1', models.DateTimeField()),
                ('damage', models.DecimalField(null=True, max_digits=17, decimal_places=2)),
                ('loss', models.DecimalField(null=True, max_digits=17, decimal_places=2)),
            ],
            options={
                'db_table': 'auto_calc',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AutoResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_event', models.IntegerField()),
                ('sector', models.CharField(max_length=200)),
                ('subsector', models.CharField(max_length=200)),
                ('asset', models.CharField(max_length=200)),
                ('rw', models.CharField(max_length=3)),
                ('kelurahan', models.CharField(max_length=50)),
                ('kecamatan', models.CharField(max_length=50)),
                ('kota', models.CharField(max_length=50)),
                ('kelas', models.CharField(max_length=50)),
                ('damage', models.DecimalField(max_digits=17, decimal_places=2)),
                ('loss', models.DecimalField(max_digits=17, decimal_places=2)),
            ],
            options={
                'db_table': 'auto_dala_result',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AutoResultJSON',
            fields=[
                ('id', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('kelurahan_id', models.CharField(max_length=200)),
                ('kota', models.CharField(max_length=200)),
                ('kecamatan', models.CharField(max_length=200)),
                ('kelurahan', models.CharField(max_length=200)),
                ('rw', models.CharField(max_length=200)),
                ('tanggal', models.DateTimeField()),
                ('damage_infrastuktur', models.DecimalField(max_digits=17, decimal_places=2)),
                ('loss_infrastruktur', models.DecimalField(max_digits=17, decimal_places=2)),
                ('damage_lintas_sektor', models.DecimalField(max_digits=17, decimal_places=2)),
                ('loss_lintas_sektor', models.DecimalField(max_digits=17, decimal_places=2)),
                ('damage_produktif', models.DecimalField(max_digits=17, decimal_places=2)),
                ('loss_produktif', models.DecimalField(max_digits=17, decimal_places=2)),
                ('damage_sosial_perumahan', models.DecimalField(max_digits=17, decimal_places=2)),
                ('loss_sosial_perumahan', models.DecimalField(max_digits=17, decimal_places=2)),
                ('damage_total', models.DecimalField(max_digits=17, decimal_places=2)),
                ('loss_total', models.DecimalField(max_digits=17, decimal_places=2)),
                ('sumber', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FloodEvent',
            fields=[
                ('id', report.models.UnsignedAutoField(serialize=False, primary_key=True)),
                ('unit', models.CharField(max_length=255)),
                ('village', models.CharField(max_length=255, null=True)),
                ('district', models.CharField(max_length=255, null=True)),
                ('rt', models.CharField(max_length=255, null=True)),
                ('rw', models.CharField(max_length=255, null=True)),
                ('depth', models.PositiveIntegerField()),
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
                ('id', report.models.UnsignedAutoField(serialize=False, primary_key=True)),
                ('unit', models.CharField(max_length=255)),
                ('village', models.CharField(max_length=255, null=True)),
                ('district', models.CharField(max_length=255, null=True)),
                ('rt', models.CharField(max_length=255, null=True)),
                ('rw', models.CharField(max_length=255, null=True)),
                ('depth', models.PositiveIntegerField()),
                ('report_time', models.DateTimeField()),
                ('request_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'fl_event_raw',
            },
            bases=(models.Model,),
        ),
    ]
