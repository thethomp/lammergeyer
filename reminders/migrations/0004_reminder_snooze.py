# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0003_reminder_alarm'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='snooze',
            field=models.FloatField(default=8),
        ),
    ]
