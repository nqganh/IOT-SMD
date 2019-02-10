# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0005_auto_20190125_0339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extension_uuid', models.CharField(max_length=256)),
                ('domain_uuid', models.CharField(max_length=256, blank=True)),
                ('extension', models.CharField(max_length=10, blank=True)),
                ('number_alias', models.CharField(max_length=10, blank=True)),
                ('password', models.CharField(max_length=32, blank=True)),
                ('accountcode', models.CharField(max_length=32, blank=True)),
                ('effective_caller_id_name', models.CharField(max_length=128, blank=True)),
                ('effective_caller_id_number', models.CharField(max_length=16, blank=True)),
                ('outbound_caller_id_name', models.CharField(max_length=16, blank=True)),
                ('outbound_caller_id_number', models.CharField(max_length=128, blank=True)),
                ('emergency_caller_id_name', models.CharField(max_length=128, blank=True)),
                ('emergency_caller_id_number', models.CharField(max_length=16, blank=True)),
                ('directory_first_name', models.CharField(max_length=64, blank=True)),
                ('directory_last_name', models.CharField(max_length=64, blank=True)),
                ('directory_visible', models.CharField(max_length=8, blank=True)),
                ('directory_exten_visible', models.CharField(max_length=8, blank=True)),
                ('limit_max', models.CharField(max_length=8, blank=True)),
                ('limit_destination', models.CharField(max_length=8, blank=True)),
                ('missed_call_app', models.CharField(max_length=16, blank=True)),
                ('missed_call_data', models.CharField(max_length=128, blank=True)),
                ('user_context', models.CharField(max_length=16, blank=True)),
                ('toll_allow', models.CharField(max_length=8, blank=True)),
                ('call_timeout', models.IntegerField(blank=True)),
                ('call_group', models.CharField(max_length=32, blank=True)),
                ('call_screen_enabled', models.CharField(max_length=8, blank=True)),
                ('user_record', models.CharField(max_length=8, blank=True)),
                ('hold_music', models.CharField(max_length=32, blank=True)),
                ('auth_acl', models.CharField(max_length=8, blank=True)),
                ('cidr', models.CharField(max_length=32, blank=True)),
                ('sip_force_contact', models.CharField(max_length=32, blank=True)),
                ('nibble_account', models.CharField(max_length=64, blank=True)),
                ('sip_force_expires', models.IntegerField(blank=True)),
                ('mwi_account', models.CharField(max_length=32, blank=True)),
                ('sip_bypass_media', models.CharField(max_length=8, blank=True)),
                ('unique_id', models.CharField(max_length=128, blank=True)),
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
                ('follow_me_uuid', models.CharField(max_length=256, blank=True)),
                ('enabled', models.CharField(max_length=8, blank=True)),
                ('description', models.CharField(max_length=128, blank=True)),
                ('forward_caller_id_uuid', models.CharField(max_length=256, blank=True)),
                ('absolute_codec_string', models.CharField(max_length=128, blank=True)),
                ('force_ping', models.CharField(max_length=8, blank=True)),
            ],
            options={
                'db_table': 'v_extensions',
                'managed': False,
            },
        ),
    ]
