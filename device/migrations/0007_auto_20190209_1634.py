# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0006_extension'),
    ]

    operations = [
        migrations.CreateModel(
            name='RingGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain_uuid', models.UUIDField(blank=True)),
                ('ring_group_uuid', models.UUIDField(blank=True)),
                ('ring_group_name', models.CharField(max_length=128, blank=True)),
                ('ring_group_extension', models.CharField(max_length=128, blank=True)),
                ('ring_group_greeting', models.CharField(max_length=128, blank=True)),
                ('ring_group_context', models.CharField(max_length=128, blank=True)),
                ('ring_group_call_timeout', models.IntegerField(blank=True)),
                ('ring_group_forward_destination', models.CharField(max_length=128, blank=True)),
                ('ring_group_forward_enabled', models.CharField(max_length=128, blank=True)),
                ('ring_group_caller_id_name', models.CharField(max_length=128, blank=True)),
                ('ring_group_caller_id_number', models.CharField(max_length=128, blank=True)),
                ('ring_group_cid_name_prefix', models.CharField(max_length=128, blank=True)),
                ('ring_group_cid_number_prefix', models.CharField(max_length=128, blank=True)),
                ('ring_group_strategy', models.CharField(max_length=128, blank=True)),
                ('ring_group_timeout_app', models.CharField(max_length=128, blank=True)),
                ('ring_group_timeout_data', models.CharField(max_length=128, blank=True)),
                ('ring_group_distinctive_ring', models.CharField(max_length=128, blank=True)),
                ('ring_group_ringback', models.CharField(max_length=128, blank=True)),
                ('ring_group_missed_call_app', models.CharField(max_length=128, blank=True)),
                ('ring_group_missed_call_data', models.CharField(max_length=128, blank=True)),
                ('ring_group_enabled', models.CharField(max_length=128, blank=True)),
                ('ring_group_description', models.CharField(max_length=128, blank=True)),
                ('dialplan_uuid', models.UUIDField(blank=True)),
                ('ring_group_forward_toll_allow', models.CharField(max_length=128, blank=True)),
            ],
            options={
                'db_table': 'v_ring_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RingGroupDestination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ring_group_destination_uuid', models.UUIDField(blank=True)),
                ('domain_uuid', models.UUIDField(blank=True)),
                ('ring_group_uuid', models.UUIDField(blank=True)),
                ('destination_number', models.CharField(max_length=128, blank=True)),
                ('destination_delay', models.IntegerField(default=0, blank=True)),
                ('destination_timeout', models.IntegerField(default=30, blank=True)),
                ('destination_prompt', models.IntegerField(default=b'', blank=True)),
            ],
            options={
                'db_table': 'v_ring_group_destinations',
                'managed': False,
            },
        ),
        migrations.RemoveField(
            model_name='device',
            name='linking',
        ),
        migrations.RemoveField(
            model_name='device',
            name='user',
        ),
        migrations.DeleteModel(
            name='Device',
        ),
    ]
