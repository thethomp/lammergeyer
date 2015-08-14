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

class ReminderValidationTest(FunctionalTest):
	
	def test_cannot_add_reminders_with_empty_title_fields(self):
		## In an effort to make the tests less brittle and more reliable, the use of the 
		## wait variable below on elements which need interection is going to be used throughout
		## the following test. Inconsistency with the functional test results has been killing 
		## progress.
		wait = WebDriverWait(self.browser, 10)
		## Because of decorators, we need to login a user for these tests to past
		self.login_test_user()

		# Della Bahee lands on the user page and expands the reminder creation panel. 
		# Like a dum dum, he neglects each input field and simply hits Create reminder! button.
		self.browser.get('%s%s' % (self.server_url, '/reminders/home/',))
		wait.until(expected_conditions.element_to_be_clickable((By.ID, 'id_reminder_panel_'))) 
		self.create_or_edit_reminder(EMPTY_REMINDER)

		# Consequently, he is redirected to the home page and sees error messages appear 
		# above each field telling him they are required for reminder creation.
		panel = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'id_reminder_panel_')))
		buttons = panel.find_elements_by_tag_name('button')
		buttons[0].click()
		wait.until(expected_conditions.element_to_be_clickable((By.ID, buttons[1].get_attribute('id')))) 
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertIn('Reminders need titles!', error.text)


		self.safe_close_panel()

		# Del properly fills out the reminder fields and a new reminder is created.
		self.create_or_edit_reminder(REMINDER_ONE)

		# Del does not learn from his mistakes and attempts to create an empty reminder again!
		wait.until(expected_conditions.element_to_be_clickable((By.ID, 'id_reminder_panel_'))) 
		self.create_or_edit_reminder(EMPTY_REMINDER)
		panel = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'id_reminder_panel_')))
		buttons = panel.find_elements_by_tag_name('button')
		buttons[0].click()
		wait.until(expected_conditions.element_to_be_clickable((By.ID, buttons[1].get_attribute('id')))) 

		# An error message is shown for each field.
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertIn('Reminders need titles!', error.text)