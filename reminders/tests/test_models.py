import datetime
import sys

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from reminders.models import Reminder, List
import reminders.timezone_object as tzobj


class ReminderModelTest(TestCase):

	def test_default_values(self):
		reminder = Reminder()
		self.assertEqual(reminder.title, '')
		self.assertEqual(
			reminder.alarm.strftime('%Y-%m-%d'), 
			(timezone.now() + datetime.timedelta(days=-1,hours=-8)).strftime('%Y-%m-%d')
		)
		self.assertEqual(reminder.snooze, 8)
		self.assertEqual(reminder.repeat, 300)

	def test_string_representation(self):
		reminder = Reminder(title='Buy something, anything')
		self.assertEqual(str(reminder), 'Buy something, anything')

class ListModelTest(TestCase):

	def test_get_absolute_url(self):
		list_ = List.objects.create()
		self.assertEqual(list_.get_absolute_url(), '/reminders/%d/' % (list_.id,))

class ListAndReminderModelTest(TestCase):

	def test_reminder_is_related_to_list(self):
		reminder = Reminder()
		list_ = List.objects.create()
		reminder.list = list_
		reminder.save()
		self.assertIn(reminder, list_.reminder_set.all())

	def test_editing_existing_reminders(self):
		list_ = List.objects.create()
		utc = tzobj.UTC()
		reminder_one = Reminder.objects.create(
			title='Buy milk',
			alarm=datetime.datetime(2015, 7, 2, 16, tzinfo=utc),
			snooze=10,
			repeat=20,
			list=list_
		)
		reminder_two = Reminder.objects.create(
			title='Buy beer',
			alarm=datetime.datetime(2015, 8, 3, 16, tzinfo=utc),
			snooze=11,
			repeat=21,
			list=list_
		)
		reminder_pk = reminder_two.pk
		saved_reminder = Reminder.objects.get(pk=reminder_pk)
		saved_reminder.title = 'Buy milk'
		saved_reminder.alarm = datetime.datetime(2015, 7, 2, 16, tzinfo=utc)
		saved_reminder.snooze = 10
		saved_reminder.repeat = 240
		saved_reminder.save()

		self.assertEqual(saved_reminder, reminder_two)
		self.assertEqual(Reminder.objects.count(), 2)
		self.assertEqual(saved_reminder.title, 'Buy milk')
		self.assertEqual(saved_reminder.alarm, datetime.datetime(2015, 7, 2, 16, tzinfo=utc))
		self.assertEqual(saved_reminder.snooze, 10)
		self.assertEqual(saved_reminder.repeat, 240)
		self.assertEqual(saved_reminder.list, list_)
		self.assertEqual(saved_reminder.pk, reminder_pk)

	def test_cannot_save_empty_reminders(self):
		list_ = List.objects.create()
		reminder = Reminder(title='', list=list_)
		with self.assertRaises(ValidationError):
			reminder.save()
			reminder.full_clean()