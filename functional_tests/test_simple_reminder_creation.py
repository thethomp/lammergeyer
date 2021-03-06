import unittest

from .base import FunctionalTest
from .base import REMINDER_ONE, REMINDER_TWO, REMINDER_THREE

from unittest import skip

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):

	""" Utility Functions"""
	def get_all_reminder_values(self):
		table = self.browser.find_element_by_id('id_reminder_list')
		reminders = table.find_elements_by_tag_name('input')
		reminders = [reminder.get_attribute('value') for reminder in reminders]
		return reminders

	"""Functional Test"""

	def test_new_user_can_create_and_display_a_new_reminder(self):
		# Billy lands on the home page
		self.browser.get('%s%s' % (self.server_url, '/reminders/home/',))
		
		# Billy is ready to create a new reminder so he expands the new reminder panel.
		# Billy gives his reminder a title, a date time, a snooze duration, 
		# and finally how often the reminder repeats. He then submits the form 
		# by clicking the Create button. Upon clicking "Create" Billy is taken to a new url
		# where his reminder shows up in the table
		self.create_or_edit_reminder(REMINDER_ONE)
		
		billy_first_list_url = self.browser.current_url
		self.assertRegexpMatches(billy_first_list_url, '/reminders/.+')

		# After the form has been submitted, the reminder title is seen as a button in the table below
		wait = WebDriverWait(self.browser, 10)
		table = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'id_reminder_list')))
		reminders = table.find_elements_by_tag_name('button')
		self.assertIn('1: Buy milk', [reminder.text for reminder in reminders])

		# Billy clicks the newly created reminder button in the table below. He sees that
		# the reminder expands and contains all the data entered above
		panel = self.browser.find_element_by_id('id_reminder_panel_1')
		buttons = panel.find_elements_by_tag_name('button')
		buttons[0].click()
		self.assertEqual(buttons[0].get_attribute('aria-expanded'), 'true')
		
		reminders = self.get_all_reminder_values()
		for value in REMINDER_ONE.itervalues():
			self.assertIn(value, reminders)

		# Billy decides he wants to create another reminder so he clicks the 'Create new reminder' button
		# and creates a second reminder
		self.create_or_edit_reminder(REMINDER_TWO)

		# He then checks the table below for reminder one and confirms the contents
		reminders = self.get_all_reminder_values()

		for value in REMINDER_ONE.itervalues():
			self.assertIn(value, reminders)

		# Billy now expands reminder two and confirms the contents
		panel = self.browser.find_element_by_id('id_reminder_panel_2')
		buttons = panel.find_elements_by_tag_name('button')
		buttons[0].click()
		self.assertEqual(buttons[0].get_attribute('aria-expanded'), 'true')

		for value in REMINDER_TWO.itervalues():
			self.assertIn(value, reminders)

		# Billy wants to create another list of reminders for work related scenarios
		## Use new browser session to make sure that no information 
		## from the grocery reminder list is coming through from cookies
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# Billy visits the home page and there is no trace of his previous reminders
		self.browser.get('%s%s' % (self.server_url, '/reminders/home/',))
		reminders = []
		with self.assertRaises(NoSuchElementException):
			reminders = self.get_all_reminder_values()

		for value in REMINDER_ONE.itervalues():
			self.assertNotIn(value, reminders)
		for value in REMINDER_TWO.itervalues():
			self.assertNotIn(value, reminders)

		# Billy starts his second list of reminders
		self.create_or_edit_reminder(REMINDER_THREE)

		# Billy's second list is assigned a new url
		billy_second_list_url = self.browser.current_url
		
		self.assertRegexpMatches(billy_second_list_url, '/reminders/.+')
		self.assertNotEqual(billy_first_list_url, billy_second_list_url)

		# The old list is not there and the new reminder shows up on a new list
		panel = self.browser.find_element_by_id('id_reminder_panel_1')
		buttons = panel.find_elements_by_tag_name('button')
		buttons[0].click()
		reminders = self.get_all_reminder_values()

		for value in REMINDER_ONE.itervalues():
			self.assertNotIn(value, reminders)
		for value in REMINDER_TWO.itervalues():
			self.assertNotIn(value, reminders)
		for value in REMINDER_THREE.itervalues():
			self.assertIn(value, reminders)