# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='imei',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='parent',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='sip_password',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='sip_username',
            field=models.CharField(max_length=16, blank=True),
        ),
    ]
