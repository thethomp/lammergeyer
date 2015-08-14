import datetime
from unittest import skip
from django.test import TestCase
from django.utils import timezone

from reminders.forms import (
	ReminderForm,
	EMPTY_REMINDER_TITLE_ERROR
)
from reminders.models import Reminder
from accounts.models import CustomUser
from base import REMINDER_ONE, REMINDER_TWO
import reminders.timezone_object as tzobj

class ReminderFormTest(TestCase):

	def test_form_renders_reminder_text_input(self):
		form = ReminderForm()
		self.assertIn('placeholder="Enter a reminder"', form.as_p())
		self.assertIn('placeholder="MM/DD/YYYY"', form.as_p())
		self.assertIn('placeholder="Enter snooze"', form.as_p())
		self.assertIn('placeholder="Enter repeat"', form.as_p())

	def test_form_validation_for_blank_reminders(self):
		form = ReminderForm(data={'title': ''})
		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['title'],
			[EMPTY_REMINDER_TITLE_ERROR]
		)

	def test_form_save_handles_saving_user(self):
		user = CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		form = ReminderForm(data=REMINDER_ONE)
		new_reminder = form.save(for_user=user)

		self.assertEqual(new_reminder, Reminder.objects.first())
		self.assertEqual(new_reminder.title, 'Buy milk')
		self.assertEqual(new_reminder.user, user)

	def test_form_update_existing_reminder_values(self):
		user = CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		utc = tzobj.UTC()
		reminder = Reminder.objects.create(
			title='Buy milk',
			alarm=datetime.datetime(2015, 7, 2, 16, tzinfo=utc),
			snooze=10,
			repeat=20,
			user=user
		)
		instance = Reminder.objects.get(pk=reminder.pk)
		form = ReminderForm(data=REMINDER_TWO, instance=instance)

		self.assertIn('value="Buy beer"', form.as_p())
		self.assertIn('value="%s"' % (REMINDER_TWO['alarm'],), form.as_p())
		self.assertIn('value="15.0"', form.as_p())
		self.assertIn('value="36.0"', form.as_p())

	def test_form_saving_existing_reminder_doesnt_create_new_reminder(self):
		user = CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		utc = tzobj.UTC()
		reminder = Reminder.objects.create(
			title='Buy milk',
			alarm=datetime.datetime(2015, 7, 2, 16, tzinfo=utc),
			snooze=10,
			repeat=20,
			user=user
		)
		self.assertEqual(Reminder.objects.count(), 1)
		instance = Reminder.objects.get(pk=reminder.pk)
		form = ReminderForm(data=REMINDER_TWO, instance=instance)
		form.save(for_user=user)
		self.assertEqual(Reminder.objects.count(), 1)

	def test_form_validation_for_blank_reminders(self):
		form = ReminderForm(data={'text': ''})

		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['title'],
			[EMPTY_REMINDER_TITLE_ERROR]
		)