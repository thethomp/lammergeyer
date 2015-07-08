# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0006_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='list',
            field=models.ForeignKey(default=None, to='reminders.List'),
        ),
    ]
