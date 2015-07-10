import unittest

from .base import FunctionalTest
from .base import REMINDER_ONE, REMINDER_TWO, REMINDER_THREE

from unittest import skip
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys

class NewPageTest(FunctionalTest):

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

	"""Functional Tests"""
	
	def test_new_user_lands_on_home_page_and_clicks_to_see_reminder_form(self):
		# Billy lands on the home page and sees the web service title.
		self.browser.get(self.live_server_url)
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