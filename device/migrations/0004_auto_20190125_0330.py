# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0003_auto_20190124_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='can_receive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='device',
            name='can_send',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='device',
            name='is_doorbell',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='device',
            name='linking',
            field=models.ManyToManyField(related_name='linking_rel_+', null=True, to='device.Device', blank=True),
        ),
    ]
