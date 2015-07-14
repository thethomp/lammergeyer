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
	def create_new_reminder(self, reminder):
		self.browser.find_element_by_id('id_new_reminder_btn').click()
		new_reminder_panel = self.browser.find_element_by_id('id_new_reminder_panel')
		inputs = new_reminder_panel.find_elements_by_tag_name('input')
		for input in inputs:
			text = input.get_attribute('name')
			if text in reminder:
				inputbox = input.send_keys(reminder[text])
		self.browser.find_element_by_id('id_create_button').click()

	def get_all_reminder_values(self):
		table = self.browser.find_element_by_id('id_reminder_list')
		reminders = table.find_elements_by_tag_name('input')
		reminders = [reminder.get_attribute('value') for reminder in reminders]
		return reminders

	"""Functional Test"""
	
	def test_user_can_create_reminder_and_then_edit_it_later(self):
		# Billy lands on the home page and creates a reminder
		self.browser.get(self.live_server_url)
		self.create_new_reminder(REMINDER_ONE)

		# He thinks the reminder is perfect and continues doing whatever he is doing 
		# knowing that he won't forget. He closes the browser.
		billy_url = self.browser.current_url
		self.browser.quit()

		# A little while later Billy realizes he is fallible and must change his reminder.
		# So he opens up the browser, and goes to his reminder list
		self.browser = webdriver.Firefox()
		self.browser.get(billy_url)

		# Billy sees his original reminder 
		reminders = self.get_all_reminder_values()
		for value in REMINDER_ONE.itervalues():
			self.assertIn(value, reminders)

		# and then changes the reminder to reflect his schedule
		self.browser.find_element_by_id('id_reminder_btn_1').click()

		## Wait for input elements to be visible
		wait = WebDriverWait(self.browser, 10)
		element = wait.until(
			expected_conditions.element_to_be_clickable((By.ID, 'id_title'))
		)

		edited_reminder = {}
		for key, value in REMINDER_TWO.iteritems():
			edited_reminder['%s_%d' % (key, 1)] = value

		reminder_panel = self.browser.find_element_by_id('id_reminder_panel')
		inputs = reminder_panel.find_elements_by_tag_name('input')
		for input in inputs:
			text = input.get_attribute('name')
			if text in edited_reminder:
				input.clear()
				input.send_keys(edited_reminder[text])

		# He updates the reminder, and sees that the reminder has indeed changed, 
		# and that there is no trace of his previous reminder
		self.browser.find_element_by_id('id_update_button').click()
		self.assertRegexpMatches(billy_url, '/reminders/.+')
		element = wait.until(
			expected_conditions.element_to_be_clickable((By.ID, 'id_reminder_list'))
		)
		reminders = self.get_all_reminder_values()
		for value in REMINDER_ONE.itervalues():
			self.assertNotIn(value, reminders)
		for value in REMINDER_TWO.itervalues():
			self.assertIn(value, reminders)