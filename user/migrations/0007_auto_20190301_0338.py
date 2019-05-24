# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20190209_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='RingGroup',
            fields=[
                ('domain_uuid', models.UUIDField(default=b'09f10c29-9f49-4209-9050-52bd09d1886a', blank=True)),
                ('ring_group_uuid', models.UUIDField(serialize=False, primary_key=True, blank=True)),
                ('ring_group_name', models.CharField(max_length=128, blank=True)),
                ('ring_group_extension', models.CharField(max_length=128, blank=True)),
                ('ring_group_greeting', models.CharField(max_length=128, blank=True)),
                ('ring_group_context', models.CharField(default=b'178.128.215.198', max_length=128, blank=True)),
                ('ring_group_call_timeout', models.IntegerField(blank=True)),
                ('ring_group_forward_destination', models.CharField(max_length=128, blank=True)),
                ('ring_group_forward_enabled', models.CharField(default=b'false', max_length=128, blank=True)),
                ('ring_group_caller_id_name', models.CharField(max_length=128, blank=True)),
                ('ring_group_caller_id_number', models.CharField(max_length=128, blank=True)),
                ('ring_group_cid_name_prefix', models.CharField(max_length=128, blank=True)),
                ('ring_group_cid_number_prefix', models.CharField(max_length=128, blank=True)),
                ('ring_group_strategy', models.CharField(default=b'simultaneous', max_length=128, blank=True)),
                ('ring_group_timeout_app', models.CharField(max_length=128, blank=True)),
                ('ring_group_timeout_data', models.CharField(max_length=128, blank=True)),
                ('ring_group_distinctive_ring', models.CharField(max_length=128, blank=True)),
                ('ring_group_ringback', models.CharField(default=b'${us-ring}', max_length=128, blank=True)),
                ('ring_group_missed_call_app', models.CharField(max_length=128, blank=True)),
                ('ring_group_missed_call_data', models.CharField(max_length=128, blank=True)),
                ('ring_group_enabled', models.CharField(default=b'true', max_length=128, blank=True)),
                ('ring_group_description', models.CharField(max_length=128, blank=True)),
                ('dialplan_uuid', models.UUIDField(blank=True)),
                ('ring_group_forward_toll_allow', models.CharField(max_length=128, blank=True)),
            ],
            options={
                'db_table': 'v_ring_groups',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='user',
            name='ring_group',
            field=models.ManyToManyField(to='user.RingGroup'),
        ),
    ]
