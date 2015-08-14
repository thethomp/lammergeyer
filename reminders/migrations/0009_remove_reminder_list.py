# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0008_reminder_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reminder',
            name='list',
        ),
    ]
