import unittest

from .base import FunctionalTest
from .base import REMINDER_ONE, REMINDER_TWO, REMINDER_THREE

from unittest import skip
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):

	""" Utility Functions"""
	def create_new_reminder(self, reminder):
		self.browser.find_element_by_id('id_new_reminder_btn').click()
		new_reminder_panel = self.browser.find_element_by_id('id_new_reminder_panel')
		inputs = new_reminder_panel.find_elements_by_tag_name('input')
		for input in inputs:
			text = input.get_attribute('name')
			if text in reminder:
				inputbox = input.send_keys(reminder[text])

	"""Functional Tests"""

	
	def test_new_user_lands_on_home_page_and_clicks_to_see_reminder_form(self):
		# Billy lands on the home page and sees the web service title.
		self.browser.get(self.server_url)
		self.assertIn(u'Your Reminders', self.browser.title.decode())

		# He then sees a button which says "Create a new reminder!"
		reminder_btn_text = self.browser.find_element_by_id('id_new_reminder_btn').text
		self.assertIn("Create a new reminder!", reminder_btn_text)

		# Billy notices no form or content without clicking the button
		panel = self.browser.find_element_by_id('id_new_reminder_panel')
		self.assertTrue(panel is not None)
		self.assertFalse(panel.is_displayed())

		# Billy clicks this button and a panel is expanded showing the reminder format
		self.browser.find_element_by_id('id_new_reminder_btn').click()
		panel = self.browser.find_element_by_id('id_new_reminder_panel')
		self.assertTrue(panel is not None)
		self.assertTrue(panel.is_displayed())

		# In the expanded content, Billy sees input fields for reminder title, reminder time, 
		# reminder snooze, and reminder repeat options
		panel = self.browser.find_element_by_id('id_new_reminder_panel')
		placeholders = [input.get_attribute('placeholder') for input in panel.find_elements_by_tag_name('input')]
		expected_placeholders = ['Enter a reminder', 'MM/DD/YYYY', 'Enter snooze', 'Enter repeat']
		for placeholder in expected_placeholders:
			self.assertIn(placeholder, placeholders)

		# Billy is not ready to add a reminder so he collapses the form
		new_reminder_btn = self.browser.find_element_by_id('id_new_reminder_btn')
		new_reminder_btn.click()
		self.assertEqual(new_reminder_btn.get_attribute('aria-expanded'), 'false')

	def test_new_user_can_create_and_display_a_new_reminder(self):
		# Billy lands on the home page
		self.browser.get(self.server_url)
		
		# Billy is ready to create a new reminder so he expands the new reminder panel.
		# Billy gives his reminder a title, a date time, a snooze duration, 
		# and finally how often the reminder repeats. He then submits the form 
		# by clicking the Create button. Upon clicking "Create" Billy is taken to a new url
		# where his reminder shows up in the table
		self.create_new_reminder(REMINDER_ONE)
		self.browser.find_element_by_id('id_create_button').click()
		billy_first_list_url = self.browser.current_url
		self.assertRegexpMatches(billy_first_list_url, '/reminders/.+')

		# After the form has been submitted, the reminder title is seen as a button in the table below
		table = self.browser.find_element_by_id('id_reminder_list')
		reminders = table.find_elements_by_tag_name('button')
		self.assertIn('1: Buy milk', [reminder.text for reminder in reminders])

		# Billy clicks the newly created reminder button in the table below. He sees that
		# the reminder expands and contains all the data entered above
		reminder_btn = self.browser.find_element_by_id('id_reminder_btn_1')
		reminder_btn.click()
		self.assertEqual(reminder_btn.get_attribute('aria-expanded'), 'true')
		
		reminders = table.find_elements_by_tag_name('input')
		for value in REMINDER_ONE.itervalues():
			self.assertIn(value, [reminder.get_attribute('value') for reminder in reminders])

		# Billy decides he wants to create another reminder so he clicks the 'Create new reminder' button
		# and creates a second reminder
		self.create_new_reminder(REMINDER_TWO)
		self.browser.find_element_by_id('id_create_button').click()

		# He then checks the table below for reminder one and confirms the contents

		table = self.browser.find_element_by_id('id_reminder_list')
		reminders = table.find_elements_by_tag_name('input')

		for value in REMINDER_ONE.itervalues():
			self.assertIn(value, [reminder.get_attribute('value') for reminder in reminders])

		# Billy now expands reminder two and confirms the contents
		reminder_btn = self.browser.find_element_by_id('id_reminder_btn_2')
		reminder_btn.click()
		self.assertEqual(reminder_btn.get_attribute('aria-expanded'), 'true')

		for value in REMINDER_TWO.itervalues():
			self.assertIn(value, [reminder.get_attribute('value') for reminder in reminders])

		# Billy wants to create another list of reminders for work related scenarios
		## Use new browser session to make sure that no information 
		## from the grocery reminder list is coming through from cookies
		self.browser.quit()
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(5)

		# Billy visits the home page and there is no trace of his previous reminders
		self.browser.get(self.live_server_url)
		table = self.browser.find_element_by_id('id_reminder_list')
		reminders = table.find_elements_by_tag_name('input')
		for value in REMINDER_ONE.itervalues():
			self.assertNotIn(value, [reminder.get_attribute('value') for reminder in reminders])
		for value in REMINDER_TWO.itervalues():
			self.assertNotIn(value, [reminder.get_attribute('value') for reminder in reminders])

		# Billy starts his second list of reminders
		self.create_new_reminder(REMINDER_THREE)
		self.browser.find_element_by_id('id_create_button').click()

		# Billy's second list is assigned a new url
		billy_second_list_url = self.browser.current_url
		
		self.assertRegexpMatches(billy_second_list_url, '/reminders/.+')
		self.assertNotEqual(billy_first_list_url, billy_second_list_url)

		# The old list is not there and the new reminder shows up on a new list
		reminder_btn = self.browser.find_element_by_id('id_reminder_btn_1')
		reminder_btn.click()
		table = self.browser.find_element_by_id('id_reminder_list')
		reminders = table.find_elements_by_tag_name('input')
		page_text = self.browser.find_element_by_tag_name('body').text
		for value in REMINDER_ONE.itervalues():
			self.assertNotIn(value, [reminder.get_attribute('value') for reminder in reminders])
		for value in REMINDER_TWO.itervalues():
			self.assertNotIn(value, [reminder.get_attribute('value') for reminder in reminders])
		for value in REMINDER_THREE.itervalues():
			self.assertIn(value, [reminder.get_attribute('value') for reminder in reminders])
		reminder_btn.click()
		#self.fail('Finish me')