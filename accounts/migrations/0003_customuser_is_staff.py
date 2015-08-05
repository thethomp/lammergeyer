# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether this user can log into this admin site.', verbose_name='staff status'),
        ),
    ]
