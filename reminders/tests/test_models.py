import datetime
import sys

from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from reminders.models import Reminder
from accounts.models import CustomUser
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

class UserReminderModelTest(TransactionTestCase):

	def setUp(self):
		self.user = CustomUser.objects.create_user(email='jj@gmail.com', password='123')

	def tearDown(self):
		self.user.delete()

	def test_reminder_is_related_to_user(self):
		reminder = Reminder()
		reminder.user = self.user
		reminder.save()
		self.assertIn(reminder, self.user.reminder_set.all())

	def test_editing_existing_reminders(self):
		utc = tzobj.UTC()
		reminder_one = Reminder.objects.create(
			title='Buy milk',
			alarm=datetime.datetime(2015, 7, 2, 16, tzinfo=utc),
			snooze=10,
			repeat=20,
			user=self.user
		)
		reminder_two = Reminder.objects.create(
			title='Buy beer',
			alarm=datetime.datetime(2015, 8, 3, 16, tzinfo=utc),
			snooze=11,
			repeat=21,
			user=self.user
		)
		saved_reminder = Reminder.objects.get(pk=reminder_two.pk)
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
		self.assertEqual(saved_reminder.user, self.user)
		self.assertEqual(saved_reminder.pk, reminder_two.pk)

	def test_cannot_save_empty_reminders(self):
		reminder = Reminder(title='', user=self.user)
		with self.assertRaises(ValidationError):
			reminder.save()
			reminder.full_clean()

	def test_foreign_key_object_instance(self):
		reminder = Reminder()
		reminder.user = self.user
		self.assertTrue(isinstance(reminder.user, CustomUser))