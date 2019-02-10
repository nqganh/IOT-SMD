# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0007_auto_20190209_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='DialPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain_uuid', models.UUIDField(blank=True)),
                ('dialplan_uuid', models.UUIDField(blank=True)),
                ('app_uuid', models.UUIDField(blank=True)),
                ('hostname', models.CharField(max_length=128, blank=True)),
                ('dialplan_context', models.CharField(max_length=128, blank=True)),
                ('dialplan_name', models.CharField(max_length=128, blank=True)),
                ('dialplan_number', models.CharField(max_length=128, blank=True)),
                ('dialplan_continue', models.CharField(max_length=128, blank=True)),
                ('dialplan_xml', models.TextField(blank=True)),
                ('dialplan_order', models.IntegerField(default=0, blank=True)),
                ('dialplan_enabled', models.CharField(max_length=128, blank=True)),
                ('dialplan_description', models.CharField(max_length=128, blank=True)),
            ],
            options={
                'db_table': 'v_dialplans',
                'managed': False,
            },
        ),
    ]
