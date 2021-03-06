import datetime

from django.db import models
from django.forms import ModelForm, RegexField
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import reminders.timezone_object as tzobj

# Create your models here.

def now_minus_1():
	utc = tzobj.UTC()
	return datetime.datetime.now(utc)-datetime.timedelta(days=1)

class List(models.Model):

	def get_absolute_url(self):
		return reverse('view_reminders', args=[self.id])

class Reminder(models.Model):

	title = models.CharField(max_length=255, default='')
	alarm = models.DateTimeField(default=now_minus_1)
	snooze = models.FloatField(default=8)
	repeat = models.FloatField(default=300)
	list = models.ForeignKey(List, default=None)

	def __unicode__(self):
		return self.title