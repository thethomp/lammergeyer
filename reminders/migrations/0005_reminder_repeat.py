# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0004_reminder_snooze'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='repeat',
            field=models.FloatField(default=300),
        ),
    ]
