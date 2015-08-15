import unittest

from .base import FunctionalTest
from .base import (
	REMINDER_ONE, REMINDER_TWO, 
	REMINDER_THREE, EMPTY_REMINDER
)
from unittest import skip
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

ERRORS = {
	'id_title': 'Reminders need titles!',
	'id_alarm': 'Date and time is required!',
	'id_snooze': 'Snooze time is required!',
	'id_repeat': 'Repeat time is required!'
	
}

class ReminderValidationTest(FunctionalTest):
	
	def test_cannot_add_reminders_with_empty_fields(self):
		## In an effort to make the tests less brittle and more reliable, the 
		## use of the wait variable below on elements which need interection 
		## is going to be used throughout the following test. Inconsistency 
		## with the functional test results has been killing progress.
		wait = WebDriverWait(self.browser, 10)

		## Because of decorators, we need to login a user for these tests to past
		self.login_test_user()

		# Della Bahee lands on the user page and expands the reminder creation panel. 
		# Like a dum dum, he makes each input empty and hits Create reminder! button.
		self.browser.get('%s%s' % (self.server_url, '/reminders/home/',))
		wait.until(expected_conditions.element_to_be_clickable((By.ID, 'id_reminder_panel_'))) 
		self.create_or_edit_reminder(EMPTY_REMINDER)

		# Consequently, the Create reminder! button form is automatically expanded, showing the 
		# errors messages from his submission. Above each field is a message telling him what 
		# is wrong with the current submission
		inputs = self.gather_form_inputs()
		self.assertTrue(inputs[0].is_displayed()) 
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertIn('Reminders need titles!', error.text)

		# Del properly fills out the reminder fields and a new reminder is created.
		self.create_or_edit_reminder(REMINDER_ONE)

		# Del does not learn from his mistakes and attempts to create an empty reminder again! 
		self.create_or_edit_reminder(EMPTY_REMINDER)

		# The form remains expanded, and shows Del error messages
		inputs = self.gather_form_inputs()
		self.assertTrue(inputs[0].is_displayed())
		# An error message is shown for each field.
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertIn('Reminders need titles!', error.text)

		# To make the error messages go away, Del creates a proper reminder
		self.create_or_edit_reminder(REMINDER_TWO)
		## This should return an empty list
		self.assertFalse(self.browser.find_elements_by_css_selector('.has-error'))

		# Del then decides to edit his existing reminder. Instead of updating to a valid reminder,
		# Del tries to update a valid reminder with invalid inputs
		self.create_or_edit_reminder(EMPTY_REMINDER, 'id_reminder_panel_1')

		# When Del hits Update, the page is rendered with the edited reminder button form expanded
		edited_reminder_panel = self.browser.find_element_by_id('id_reminder_panel_1')
		inputs = edited_reminder_panel.find_elements_by_tag_name('input')
		## inputs[0] is apparently the csrf token which is always hidden
		self.assertTrue(inputs[1].is_displayed())

		# And Del is given error messages on how to correct his submission
		errors = edited_reminder_panel.find_elements_by_css_selector('.has-error')
		self.assertTrue([error.text for error in errors if 'Reminders need titles!' in error.text])

		# Del corrects and submits the edited reminder
		self.create_or_edit_reminder(REMINDER_THREE, 'id_reminder_panel_1')

		# No reminder button forms are expanded, and no error messages are present
		self.assertFalse(self.browser.find_elements_by_css_selector('.has-error'))
		reminder_panel_one = self.browser.find_element_by_id('id_reminder_panel_1')
		reminder_panel_two = self.browser.find_element_by_id('id_reminder_panel_2')
		inputs = reminder_panel_one.find_elements_by_tag_name('input')
		self.assertFalse(inputs[0].is_displayed())
		inputs = reminder_panel_two.find_elements_by_tag_name('input')
		self.assertFalse(inputs[0].is_displayed())