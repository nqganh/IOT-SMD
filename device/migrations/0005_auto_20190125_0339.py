# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0004_auto_20190125_0330'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='imei',
            new_name='uuid',
        ),
    ]
