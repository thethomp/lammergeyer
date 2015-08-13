# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reminders', '0007_reminder_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='user',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL),
        ),
    ]
