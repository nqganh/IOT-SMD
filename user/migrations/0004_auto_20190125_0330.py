# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_doorbell'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='doorbell',
        ),
        migrations.RemoveField(
            model_name='user',
            name='imei',
        ),
        migrations.RemoveField(
            model_name='user',
            name='sip_password',
        ),
        migrations.RemoveField(
            model_name='user',
            name='sip_username',
        ),
    ]
