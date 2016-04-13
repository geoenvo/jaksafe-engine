# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdHocCalc',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('t0', models.DateTimeField()),
                ('t1', models.DateTimeField()),
                ('damage', models.DecimalField(max_digits=17, decimal_places=2)),
                ('loss', models.DecimalField(max_digits=17, decimal_places=2)),
                ('id_event', models.IntegerField()),
                ('id_user', models.IntegerField()),
                ('id_user_group', models.IntegerField()),
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
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('id_event', models.IntegerField()),
                ('t0', models.DateTimeField()),
                ('t1', models.DateTimeField()),
                ('damage', models.DecimalField(max_digits=17, decimal_places=2)),
                ('loss', models.DecimalField(max_digits=17, decimal_places=2)),
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
    ]
