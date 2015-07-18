from django.test import TestCase

from reminders.forms import ReminderForm, EMPTY_REMINDER_TITLE_ERROR

class ReminderFormTest(TestCase):

	def test_form_renders_reminder_text_input(self):
		form = ReminderForm()
		self.assertIn('placeholder="Enter a reminder"', form.as_p())

	def test_form_validation_for_blank_reminders(self):
		form = ReminderForm(data={'text': ''})
		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['title'],
			[EMPTY_REMINDER_TITLE_ERROR]
		)