# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0002_auto_20190124_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='is_master',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='device',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
