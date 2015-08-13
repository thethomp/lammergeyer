import datetime

from django.db import models
from django.core.urlresolvers import reverse

import reminders.timezone_object as tzobj
from lammergeyer import settings

# Create your models here.

def now_minus_1():
	utc = tzobj.UTC()
	return datetime.datetime.now(utc)-datetime.timedelta(days=1)

class Reminder(models.Model):

	title = models.CharField(max_length=255, default='')
	alarm = models.DateTimeField(default=now_minus_1)
	snooze = models.FloatField(default=8)
	repeat = models.FloatField(default=300)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None)

	"""
	https://docs.djangoproject.com/en/1.8/topics/auth/customizing/
	'When you define a foreign key or many-to-many relations to the 
	User model, you should specify the custom model using the 
	AUTH_USER_MODEL setting. For example: 
	user = models.ForeignKey(settings.AUTH_USER_MODEL)'
	"""

	def __unicode__(self):
		return self.title