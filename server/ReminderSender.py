#from django.shortcuts import render
#from django.http import HttpResponse, HttpResponseRedirect
#from reminders.forms import UserForm, UserProfileForm
#from django.template import RequestContext, loader
#from django.shortcuts import render_to_response
#from django.contrib.auth import authenticate, login
#from django.contrib.auth.decorators import login_required
#from .reminders.models import Reminder, UserProfile
from reminders.models import Reminder
from accounts.models import CustomUser, CustomUserManager
#from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
import os, django
from django.core.mail import send_mail



class ReminderSender():

	def __init__(self):
		os.environ['DJANGO_SETTINGS_MODULE'] = 'lammergeyer.settings'
		django.setup()
	
	def get_reminder_list(self):
		## Establish upper and lower limits for reminder filter times
		now = timezone.now()
		reminder_upper_limit = now + timedelta(seconds=10)
		reminder_lower_limit = now# - timedelta(minutes=1)
		print 'now: ' + str(now)
		print 'UL: ' + str(reminder_upper_limit)
		print 'LL: ' + str(reminder_lower_limit)
		reminder_list = Reminder.objects.filter(alarm__lt=reminder_upper_limit).filter(alarm__gt=reminder_lower_limit)
		for r in reminder_list:
			email = r.user.email
			title = r.title
			extra_text ='\n (your reminder was set for {0} and the time right now is {1})'.format(r.alarm, str(now))
			to_string = 'Reminder will be sent to {0} with the message\'{1}\''.format(email, title)
			print to_string
			send_mail('Reminder from thomp.info!', title+extra_text, 'GoodGirlsAreGREAT@ThompIsABadass.com',[email], fail_silently=False)
				

	def extract_reminder_data(reminder):
		out = {}
		out['email'] = reminder.user.email
		out['title'] = reminder.title
		return out





