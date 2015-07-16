import unittest

from .base import FunctionalTest
from .base import REMINDER_ONE, EMPTY_REMINDER
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
POSSIBLE_INPUT_COMBINATIONS = [
	# 0
	[''],
	# 1, 2, 3, 4
	['id_title'],['id_alarm'],['id_snooze'],['id_repeat'], 
	# 5, 6, 7, 8, 9, 10
	['id_title', 'id_alarm'],['id_title', 'id_snooze'],['id_title', 'id_repeat'],['id_alarm', 'id_snooze'],['id_alarm', 'id_repeat'],['id_snooze', 'id_repeat'], 
	# 11, 12, 13, 14
	['id_title', 'id_alarm', 'id_snooze'],['id_title', 'id_alarm', 'id_repeat'],['id_title', 'id_snooze', 'id_repeat'],['id_alarm', 'id_snooze', 'id_repeat'], 
	# 15
	['id_title', 'id_alarm', 'id_snooze', 'id_repeat']
]

class ReminderValidationTest(FunctionalTest):
	
	def return_errors_on_empty_inputs(self, reminder, *args):
		element = wait.until(
			expected_conditions.element_to_be_clickable((By.ID, 'id_new_reminder_btn'))
		)
		self.browser.find_element_by_id('id_new_reminder_btn').click()
		new_reminder_panel = self.browser.find_element_by_id('id_new_reminder_panel')
		for arg in args:
			input = new_reminder_panel.find_element_by_id(arg)
			input.send_keys(reminder[arg])
		self.browser.find_element_by_id('id_create_button').click()
		errors = self.browser.find_elements_by_css_selector('.has-error')
		return errors

	def test_cannot_add_reminders_with_empty_title_fields(self):
		## In an effort to make the tests less brittle and more reliable, the use of the 
		## wait variable below on elements which need interection is going to be used throughout
		## the following test. Inconsistency with the functional test results has been killing 
		## progress.
		wait = WebDriverWait(self.browser, 10)

		# Della Bahee lands on the user page and expands the reminder creation panel. 
		# Like a dum dum, he neglects each input field and simply hits Create reminder! button.
		self.browser.get(self.server_url)
		element = wait.until(
			expected_conditions.element_to_be_clickable((By.ID, 'id_new_reminder_btn'))
		) 
		self.create_or_edit_reminder(EMPTY_REMINDER, 'id_new_reminder_btn', 'id_create_button')

		# Consequently, he is redirected to the home page and sees error messages appear 
		# above each field telling him they are required for reminder creation.
		element = wait.until(
			expected_conditions.element_to_be_clickable((By.ID, 'id_new_reminder_btn'))
		)
		self.browser.find_element_by_id('id_new_reminder_btn').click()
		element = wait.until(
			expected_conditions.element_to_be_clickable((By.ID, 'id_create_button'))
		) 
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, 'Reminders need titles!')
		#self.browser.find_element_by_id('id_new_reminder_btn').click()
		#self.assertEqual(self.browser.find_element_by_id('id_new_reminder_btn').get_attribute('aria-expanded'), 
		#	'false'
		#)
		self.safe_close_panel()

		# Del properly fills out the reminder fields and a new reminder is created.
		self.create_or_edit_reminder(REMINDER_ONE, 'id_new_reminder_btn', 'id_create_button')

		# Del does not learn from his mistakes and attempts to create an empty reminder again!
		self.browser.find_element_by_id('id_new_reminder_btn').click()
		create_button = self.browser.find_element_by_id('id_create_button').click()

		# An error message is shown for each field.
		errors = self.find_elements_by_css_selector('.has-error')
		for error in errors:
			self.assertIn(error, ERRORS.itervalues())

		# Del now only fills in singular fields and hits create. He sees input error messages for each field
		# he left blank
		## The number of possible ways someone can incorrectly fill out a form can be represented by the power
		## set of the inputs. A form with 4 fields has exactly 1 way to fill none of them, 4 ways to fill out one
		## of them, (1, 4, 6, 4, 1)..., and exactly 1 way, the correct way, to fill out all of them. Below we test
		## that when a single form field is completed, the error corresponding that that field is not in the error 
		## list. And that the list has the proper number of errors
		for inputs in POSSIBLE_INPUT_COMBINATIONS[1:5]:
			errors = self.return_errors_on_empty_inputs(REMINDER_ONE, inputs)
			for input in inputs:
				self.assertNotIn(ERRORS[input], errors)
			self.assertEqual(len(errors), 3)

		# Del is learning, he realizes at least one field must be filled in. Thus he tries each combination 
		# of dual fields
		for inputs in POSSIBLE_INPUT_COMBINATIONS[5:11]:
			errors = self.return_errors_on_empty_inputs(REMINDER_ONE, inputs)
			for input in inputs:
				self.assertNotIn(ERRORS[input], errors)
			self.assertEqual(len(errors), 2)

		# Del is convinced at least two fields must be used. So he tries all triplet combinations.
		for inputs in POSSIBLE_INPUT_COMBINATIONS[11:15]:
			errors = self.return_errors_on_empty_inputs(REMINDER_ONE, inputs)
			for input in inputs:
				self.assertNotIn(ERRORS[input], errors)
			self.assertEqual(len(errors), 1)

		# Del has decided that every field must have an input. He creates a proper reminder.
		for inputs in POSSIBLE_INPUT_COMBINATIONS[15]:
			errors = self.return_errors_on_empty_inputs(REMINDER_ONE, inputs)
			for input in inputs:
				self.assertNotIn(ERRORS[input], errors)
			self.assertEqual(len(errors), 0)