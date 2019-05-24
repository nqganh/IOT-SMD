# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0005_auto_20190125_0339'),
    ]

    operations = [
        migrations.CreateModel(
            name='DialPlan',
            fields=[
                ('domain_uuid', models.UUIDField(default=b'09f10c29-9f49-4209-9050-52bd09d1886a', blank=True)),
                ('dialplan_uuid', models.UUIDField(serialize=False, primary_key=True, blank=True)),
                ('app_uuid', models.UUIDField(blank=True)),
                ('hostname', models.CharField(default=None, max_length=128, blank=True)),
                ('dialplan_context', models.CharField(default=b'178.128.215.198', max_length=128, blank=True)),
                ('dialplan_name', models.CharField(max_length=128, blank=True)),
                ('dialplan_number', models.CharField(max_length=128, blank=True)),
                ('dialplan_continue', models.CharField(default=b'false', max_length=128, blank=True)),
                ('dialplan_xml', models.TextField(blank=True)),
                ('dialplan_order', models.IntegerField(default=101, blank=True)),
                ('dialplan_enabled', models.CharField(default=b'true', max_length=128, blank=True)),
                ('dialplan_description', models.CharField(max_length=128, blank=True)),
            ],
            options={
                'db_table': 'v_dialplans',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Extension',
            fields=[
                ('extension_uuid', models.CharField(max_length=256, serialize=False, primary_key=True)),
                ('domain_uuid', models.CharField(default=b'09f10c29-9f49-4209-9050-52bd09d1886a', max_length=256, blank=True)),
                ('extension', models.CharField(unique=True, max_length=10, blank=True)),
                ('number_alias', models.CharField(max_length=10, blank=True)),
                ('password', models.CharField(max_length=32, blank=True)),
                ('effective_caller_id_name', models.CharField(max_length=128, blank=True)),
                ('effective_caller_id_number', models.CharField(max_length=16, blank=True)),
                ('outbound_caller_id_name', models.CharField(max_length=16, blank=True)),
                ('outbound_caller_id_number', models.CharField(max_length=128, blank=True)),
                ('emergency_caller_id_name', models.CharField(max_length=128, blank=True)),
                ('emergency_caller_id_number', models.CharField(max_length=16, blank=True)),
                ('directory_first_name', models.CharField(max_length=64, blank=True)),
                ('directory_last_name', models.CharField(max_length=64, blank=True)),
                ('directory_visible', models.CharField(default=b'true', max_length=8, blank=True)),
                ('directory_exten_visible', models.CharField(default=b'true', max_length=8, blank=True)),
                ('limit_max', models.CharField(default=5, max_length=8, blank=True)),
                ('limit_destination', models.CharField(default=b'error/user_busy', max_length=64, blank=True)),
                ('missed_call_app', models.CharField(max_length=16, blank=True)),
                ('missed_call_data', models.CharField(max_length=128, blank=True)),
                ('user_context', models.CharField(default=b'178.128.215.198', max_length=16, blank=True)),
                ('toll_allow', models.CharField(max_length=8, blank=True)),
                ('call_timeout', models.IntegerField(default=30, blank=True)),
                ('call_group', models.CharField(max_length=32, blank=True)),
                ('call_screen_enabled', models.CharField(default=b'false', max_length=8, blank=True)),
                ('user_record', models.CharField(max_length=8, blank=True)),
                ('hold_music', models.CharField(max_length=32, blank=True)),
                ('auth_acl', models.CharField(max_length=8, blank=True)),
                ('cidr', models.CharField(max_length=32, blank=True)),
                ('sip_force_contact', models.CharField(max_length=32, blank=True)),
                ('nibble_account', models.IntegerField(blank=True)),
                ('sip_force_expires', models.IntegerField(blank=True)),
                ('mwi_account', models.CharField(max_length=32, blank=True)),
                ('sip_bypass_media', models.CharField(max_length=8, blank=True)),
                ('unique_id', models.IntegerField(blank=True)),
                ('dial_string', models.CharField(max_length=128, blank=True)),
                ('dial_user', models.CharField(max_length=32, blank=True)),
                ('dial_domain', models.CharField(max_length=32, blank=True)),
                ('do_not_disturb', models.CharField(max_length=8, blank=True)),
                ('forward_all_destination', models.CharField(max_length=8, blank=True)),
                ('forward_all_enabled', models.CharField(max_length=8, blank=True)),
                ('forward_busy_destination', models.CharField(max_length=8, blank=True)),
                ('forward_busy_enabled', models.CharField(max_length=8, blank=True)),
                ('forward_no_answer_destination', models.CharField(max_length=8, blank=True)),
                ('forward_no_answer_enabled', models.CharField(max_length=8, blank=True)),
                ('forward_user_not_registered_destination', models.CharField(max_length=8, blank=True)),
                ('forward_user_not_registered_enabled', models.CharField(max_length=8, blank=True)),
                ('follow_me_uuid', models.UUIDField(blank=True)),
                ('enabled', models.CharField(default=b'true', max_length=8, blank=True)),
                ('description', models.CharField(max_length=128, blank=True)),
                ('forward_caller_id_uuid', models.UUIDField(blank=True)),
                ('absolute_codec_string', models.CharField(max_length=128, blank=True)),
                ('force_ping', models.CharField(max_length=8, blank=True)),
            ],
            options={
                'db_table': 'v_extensions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RingGroupDestination',
            fields=[
                ('ring_group_destination_uuid', models.UUIDField(serialize=False, primary_key=True, blank=True)),
                ('domain_uuid', models.UUIDField(default=b'09f10c29-9f49-4209-9050-52bd09d1886a', blank=True)),
                ('destination_delay', models.IntegerField(default=0, blank=True)),
                ('destination_timeout', models.IntegerField(default=30, blank=True)),
                ('destination_prompt', models.IntegerField(default=None, blank=True)),
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
