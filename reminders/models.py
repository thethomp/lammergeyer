from django.db import models
from django.forms import ModelForm, RegexField
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	phone = models.CharField(max_length=10, blank=True)
	def __unicode__(self):
		return self.user.username

#class User(models.Model):
#	email = models.CharField(max_length=100)
#	password = models.CharField(max_length=100)
#	phone_number = RegexField(regex=r'^\+?1?\d{9,15}$', error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
#	def __str__(self):
#		return self.email

class Reminder(models.Model):
	user = models.ForeignKey(UserProfile)
	active = models.BooleanField(default=True)
	title = models.CharField(max_length=100)
	reminder_time = models.DateTimeField('reminder time')
	snooze_duration = models.DateTimeField('snooze')
	repeat_time = models.DateTimeField('repeat')
	def __str__(self):
		return self.title
    
#class PhoneModel(ModelForm):
#	class Meta:
	#	model = User
	#	fields = ['phone_number']
	#user = models.ForeignKey(User)
	#phone_number = RegexField(regex=r'^\+?1?\d{9,15}$', error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
	#phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	#phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=10) # validators should be a list
	#def __str__(self):
	#	return self.phone_number
