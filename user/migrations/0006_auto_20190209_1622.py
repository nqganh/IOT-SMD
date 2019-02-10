# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_user_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='uuid',
        ),
        migrations.AddField(
            model_name='user',
            name='ring_group_ext',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='ring_group_strategy',
            field=models.CharField(max_length=15, blank=True),
        ),
    ]
