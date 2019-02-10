# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190124_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='doorbell',
            field=models.BooleanField(default=False),
        ),
    ]
