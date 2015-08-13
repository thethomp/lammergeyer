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

	def test_new_user_can_create_and_display_a_new_reminder(self):
		## Because of decorators, we need to login a user for these tests to past
		self.login_test_user()

		# Billy lands on the home page
		self.browser.get('%s%s' % (self.server_url, '/reminders/home/',))
		
		# Billy is ready to create a new reminder so he expands the new reminder panel.
		# Billy gives his reminder a title, a date time, a snooze duration, 
		# and finally how often the reminder repeats. He then submits the form 
		# by clicking the Create button. Upon clicking "Create" Billy stays on the same page
		# but a reminder now appears below the create reminder form.
		self.create_or_edit_reminder(REMINDER_ONE)
		
		billy_first_list_url = self.browser.current_url
		self.assertRegexpMatches(billy_first_list_url, '/reminders/home/')

		# After the form has been submitted, the reminder title is seen as a button in the table below
		wait = WebDriverWait(self.browser, 10)
		table = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'id_reminder_list')))
		reminders = table.find_elements_by_tag_name('button')
		self.assertIn('1: Buy milk', [reminder.text for reminder in reminders])

		# Billy clicks the newly created reminder button in the table below. He sees that
		# the reminder expands and contains all the data entered above
		## Testing attributes is not a great thing to do, seems wildly inconsistent
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

		# Billy cannot think of anything else to put down so he closes the browser.
		self.browser.quit()

		# Later something comes up for which Billy needs a new reminder. So he opens
		# the reminders app and logs back in. He sees his first two reminders.
		self.browser = webdriver.Firefox()
		self.login_test_user()
		self.browser.get('%s%s' % (self.server_url, '/reminders/home/',))

		reminders = self.get_all_reminder_values()
		for value in REMINDER_ONE.itervalues():
			self.assertIn(value, reminders)
		for value in REMINDER_TWO.itervalues():
			self.assertIn(value, reminders)

		# Then creates his third and final? reminder.
		self.create_or_edit_reminder(REMINDER_THREE)
		
		# All three reminders show up below the create reminder form
		reminders = self.get_all_reminder_values()

		for value in REMINDER_ONE.itervalues():
			self.assertIn(value, reminders)
		for value in REMINDER_TWO.itervalues():
			self.assertIn(value, reminders)
		for value in REMINDER_THREE.itervalues():
			self.assertIn(value, reminders)