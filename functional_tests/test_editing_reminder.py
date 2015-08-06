import unittest

from .base import FunctionalTest
from .base import REMINDER_ONE, REMINDER_TWO, REMINDER_THREE

from unittest import skip

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ReturningVisitorTest(FunctionalTest):

	""" Utility Functions"""

	def get_all_reminder_values(self):
		wait = WebDriverWait(self.browser, 10)
		element = wait.until(
			expected_conditions.element_to_be_clickable((By.ID, 'id_reminder_list'))
		)
		table = self.browser.find_element_by_id('id_reminder_list')
		reminders = table.find_elements_by_tag_name('input')
		reminders = [reminder.get_attribute('value') for reminder in reminders]
		return reminders

	"""Functional Test"""
	
	def test_user_can_create_reminder_and_then_edit_it_later(self):
		## For consistency
		wait = WebDriverWait(self.browser, 10)
		## Because of decorators, we need to login a user for these tests to past
		self.login_test_user()

		# Billy lands on the home page and creates a reminder
		self.browser.get('%s%s' % (self.server_url, '/reminders/home/',))
		panel = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'id_reminder_panel_')))
		self.create_or_edit_reminder(REMINDER_ONE)

		# He thinks the reminder is perfect and continues doing whatever he is doing 
		# knowing that he won't forget. He closes the browser.
		billy_url = self.browser.current_url
		self.browser.quit()

		# A little while later Billy realizes he is fallible and must change his reminder.
		# So he opens up the browser, and goes to his reminder list
		self.browser = webdriver.Firefox()
		## Log back in
		self.login_test_user()
		self.browser.get(billy_url)
		wait = WebDriverWait(self.browser, 10)
		wait.until(expected_conditions.element_to_be_clickable((By.ID, 'id_reminder_panel_')))

		# Billy sees his original reminder
		reminders = self.get_all_reminder_values()
		for value in REMINDER_ONE.itervalues():
			self.assertIn(value, reminders)

		# and then changes the reminder to reflect his schedule
		## Wait for input elements to be visible

		self.create_or_edit_reminder(REMINDER_TWO, panel='id_reminder_panel_1')
		
		self.assertRegexpMatches(billy_url, '/reminders/.+')

		reminders = self.get_all_reminder_values()
		for value in REMINDER_ONE.itervalues():
			self.assertNotIn(value, reminders)
		for value in REMINDER_TWO.itervalues():
			self.assertIn(value, reminders)