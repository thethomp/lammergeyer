from django.db import models

# Create your models here.

class User(models.Model):
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	

class Reminder(models.Model):
	user = models.ForeignKey(User)
	active = models.BooleanField(default=True)
	title = models.CharField(max_length=100)
	reminder_time = models.DateTimeField('reminder time')
	snooze_duration = models.DateTimeField('snooze')
	repeat_time = models.DateTimeField('repeat')
