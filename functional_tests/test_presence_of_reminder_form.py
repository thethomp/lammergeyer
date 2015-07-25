import unittest

from .base import FunctionalTest
from .base import REMINDER_ONE, REMINDER_TWO, REMINDER_THREE

from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys

class NewPageTest(FunctionalTest):

	"""Functional Tests"""
	
	def test_new_user_lands_on_home_page_and_clicks_to_see_reminder_form(self):
		## To help with stability
		wait = WebDriverWait(self.browser, 10)

		# Billy lands on the home page and sees the web service title.
		self.browser.get(self.server_url)
		self.assertIn(u'Your Reminders', self.browser.title.decode())
		element = wait.until(
			expected_conditions.element_to_be_clickable((By.ID, 'id_reminder_panel_'))
		)

		# He then sees a button which says "Create a new reminder!"
		panel = self.browser.find_element_by_id('id_reminder_panel_')
		buttons = panel.find_elements_by_tag_name('button')
		self.assertIn("Create a new reminder!", buttons[0].text)

		# Billy notices no form or content without clicking the button
		self.assertTrue(panel is not None)
		self.assertFalse(buttons[1].is_displayed())

		# Billy clicks this button and a panel is expanded showing the reminder format
		buttons[0].click()

		element = wait.until(
			expected_conditions.element_to_be_clickable((By.ID, buttons[1].get_attribute('id')))
		)

		self.assertTrue(panel is not None)
		self.assertTrue(panel.is_displayed())

		# In the expanded content, Billy sees input fields for reminder title, reminder time, 
		# reminder snooze, and reminder repeat options
		inputs = panel.find_elements_by_tag_name('input')
		placeholders = [input.get_attribute('placeholder') for input in inputs]
		expected_placeholders = ['Enter a reminder', 'MM/DD/YYYY', 'Enter snooze', 'Enter repeat']
		for placeholder in expected_placeholders:
			self.assertIn(placeholder, placeholders)

		# Billy is not ready to add a reminder so he collapses the form
		buttons[0].click()
		self.assertEqual(buttons[0].get_attribute('aria-expanded'), 'false')