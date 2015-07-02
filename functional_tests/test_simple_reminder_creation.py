import unittest

from .base import FunctionalTest
from .base import TESTDATA

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

	@unittest.skip('skip for now')
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
		form = self.browser.find_element_by_id('id_new_reminder_form')
		placeholders = [input.get_attribute('placeholder') for input in form.find_elements_by_tag_name('input')]
		expected_placeholders = ['Enter a reminder', 'MM/DD/YYYY', 'Enter snooze', 'Enter repeat']
		self.assertEqual(placeholders, expected_placeholders)

		# Billy is not ready to add a reminder so he collapses the form
		reminder_btn_text = self.browser.find_element_by_id('id_new_reminder_btn')
		reminder_btn_text.click()
		self.assertEqual(reminder_btn_text.get_attribute('aria-expanded'), 'false')

	def test_new_user_can_create_and_display_a_new_reminder(self):
		# Billy is ready to create a new reminder so he expands the new reminder panel
		self.browser.get(self.server_url)
		#self.browser.find_element_by_id('id_new_reminder_btn').click()
		self.create_new_reminder(TESTDATA)
		# Billy gives his reminder a title,
		#inputbox = self.browser.find_element_by_id('id_new_title')
		#inputbox.send_keys('Our very first reminder!')
		# a date time,
		#inputbox = self.browser.find_element_by_id('id_new_alarm')
		#inputbox.send_keys('Remind me in 1 hour')
		# a snooze duration, 
		#inputbox = self.browser.find_element_by_id('id_new_snooze')
		#inputbox.send_keys('10 more minutes!')
		# and finally how often the reminder repeats
		#inputbox = self.browser.find_element_by_id('id_new_repeat')
		#inputbox.send_keys('T')
		# He then submits the form by clicking the Create button
		self.browser.find_element_by_id('id_new_button').click()

		# After the form has been submitted, the reminder title is seen as a button in the table below
		table = self.browser.find_element_by_id('id_reminder_list')
		reminders = table.find_elements_by_tag_name('button')
		self.assertIn('1: Buy milk', [reminder.text for reminder in reminders])

		# Billy clicks the newly created reminder button in the table below. He sees that
		# the reminder expands and contains all the data entered above
		reminder_btn = self.browser.find_element_by_id('id_reminder_btn')
		reminder_btn.click()
		self.assertEqual(reminder_btn.get_attribute('aria-expanded'), 'true')

		
		reminders = table.find_elements_by_tag_name('input')
		for value in TESTDATA.itervalues():
			self.assertIn(value, [reminder.get_attribute('value') for reminder in reminders])

		self.fail('Finish me')

		# Billy decides he wants to create another reminder so he clicks the 'Create new reminder' button
