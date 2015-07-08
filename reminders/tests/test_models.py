import datetime

from django.test import TestCase
from reminders.models import Reminder, List
import reminders.timezone_object as tzobj

class ListAndReminderModelTest(TestCase):

	def test_saving_and_retrieving_reminders(self):
		utc = tzobj.UTC()
		list_ = List()
		list_.save()

		first_reminder = Reminder()
		first_reminder.title = 'Our very first reminder'
		first_reminder.alarm = datetime.datetime(2015, 7, 2, 16, tzinfo=utc)
		first_reminder.snooze = 10
		first_reminder.repeat = 240 # lets assume the repeat is in minutes... 240 -> repeat every 4 hrs.
		first_reminder.list = list_
		first_reminder.save()

		second_reminder = Reminder()
		second_reminder.title = 'The second reminder'
		second_reminder.alarm = datetime.datetime(2015, 7, 2, 16, tzinfo=utc)
		second_reminder.snooze = 10
		second_reminder.repeat = 240
		second_reminder.list = list_
		second_reminder.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_reminders = Reminder.objects.all()
		self.assertEqual(saved_reminders.count(), 2)

		first_saved_reminder = saved_reminders[0]
		second_saved_reminder = saved_reminders[1]

		self.assertEqual(first_saved_reminder.title, 'Our very first reminder')
		self.assertEqual(first_saved_reminder.alarm, datetime.datetime(2015, 7, 2, 16, tzinfo=utc))
		self.assertEqual(first_saved_reminder.snooze, 10)
		self.assertEqual(first_saved_reminder.repeat, 240)
		self.assertEqual(first_saved_reminder.list, list_)

		self.assertEqual(second_saved_reminder.title, 'The second reminder')
		self.assertEqual(second_saved_reminder.alarm, datetime.datetime(2015, 7, 2, 16, tzinfo=utc))
		self.assertEqual(second_saved_reminder.snooze, 10)
		self.assertEqual(second_saved_reminder.repeat, 240)
		self.assertEqual(second_saved_reminder.list, list_)