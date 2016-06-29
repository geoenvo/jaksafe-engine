# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_autoresult_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autoresult',
            name='damage',
            field=models.DecimalField(default=0.0, max_digits=17, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='autoresult',
            name='loss',
            field=models.DecimalField(default=0.0, max_digits=17, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='autoresult',
            name='total',
            field=models.DecimalField(default=0.0, max_digits=17, decimal_places=2),
            preserve_default=True,
        ),
    ]
