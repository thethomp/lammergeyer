# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0009_remove_reminder_list'),
    ]

    operations = [
        migrations.DeleteModel(
            name='List',
        ),
    ]
