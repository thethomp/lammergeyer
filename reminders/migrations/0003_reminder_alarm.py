# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import reminders.models


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0002_reminder_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='alarm',
            field=models.DateTimeField(default=reminders.models.now_minus_1),
        ),
    ]
