from reminders.models import Reminder
import reminders.timezone_object as tzobj
import datetime

def return_proper_reminder(post_dictionary):
	date = [int(i) for i in request.POST.get('reminder_alarm', '').split('-')]
	utc = tzobj.UTC()

	