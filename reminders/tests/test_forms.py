import datetime
from django.test import TestCase
from django.utils import timezone

from reminders.forms import (
	ReminderForm, ExistingReminderForm,
	EMPTY_REMINDER_TITLE_ERROR
)
from reminders.models import List, Reminder
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

	def test_form_save_handles_saving_to_a_list(self):
		list_ = List.objects.create()
		form = ReminderForm(data=REMINDER_ONE)
		new_reminder = form.save(for_list=list_)

		self.assertEqual(new_reminder, Reminder.objects.first())
		self.assertEqual(new_reminder.title, 'Buy milk')
		self.assertEqual(new_reminder.list, list_)

	def test_form_update_existing_reminder_values(self):
		list_ = List.objects.create()
		utc = tzobj.UTC()
		reminder = Reminder.objects.create(
			title='Buy milk',
			alarm=datetime.datetime(2015, 7, 2, 16, tzinfo=utc),
			snooze=10,
			repeat=20,
			list=list_
		)
		instance = Reminder.objects.get(pk=reminder.pk)
		form = ReminderForm(data=REMINDER_TWO, instance=instance)

		self.assertIn('value="Buy beer"', form.as_p())
		self.assertIn('value="%s"' % (REMINDER_TWO['alarm'],), form.as_p())
		self.assertIn('value="15.0"', form.as_p())
		self.assertIn('value="36.0"', form.as_p())

	def test_form_validation_for_blank_reminders(self):
		form = ReminderForm(data={'text': ''})

		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['title'],
			[EMPTY_REMINDER_TITLE_ERROR]
		)