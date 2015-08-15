#from django.shortcuts import render
#from django.http import HttpResponse, HttpResponseRedirect
#from reminders.forms import UserForm, UserProfileForm
#from django.template import RequestContext, loader
#from django.shortcuts import render_to_response
#from django.contrib.auth import authenticate, login
#from django.contrib.auth.decorators import login_required
#from .reminders.models import Reminder, UserProfile
from reminders.models import Reminder, UserProfile
#from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
import os, django


class ReminderSender():

	def __init__(self):
		os.environ['DJANGO_SETTINGS_MODULE'] = 'lammergeyer.settings'
		django.setup()
	
	def get_reminder_list(self):
		reminder_upper_limit = timezone.now() + timedelta(hours=1)
		reminder_lower_limit = timezone.now() - timedelta(hours=1)
		print 'UL: ' + str(reminder_upper_limit)
		print 'LL: ' + str(reminder_lower_limit)
		reminder_list = Reminder.objects.filter(reminder_time__lt=reminder_upper_limit).filter(reminder_time__gt=reminder_lower_limit)

		print reminder_list
