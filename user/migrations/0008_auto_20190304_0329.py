# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20190301_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ring_group',
            field=models.ManyToManyField(related_name='user', to='user.RingGroup'),
        ),
    ]
