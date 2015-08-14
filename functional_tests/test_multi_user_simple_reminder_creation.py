import unittest

from .base import FunctionalTest
from .base import REMINDER_ONE, REMINDER_TWO, REMINDER_THREE
from accounts.models import CustomUser

from unittest import skip

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):

	def setUp(self):
		CustomUser.objects.create_user(email='delbah@gmail.com', password='123')
		super(NewVisitorTest, self).setUp()

	def test_multiple_users_can_create_and_display_their_own_reminders(self):
		# Billy logs in, is redirected to the home page, and creates a few reminders
		self.login_test_user()
		home_url = self.browser.get(self.browser.current_url)

		self.assertRegexpMatches(home_url, '/reminders/home/')
		self.create_or_edit_reminder(REMINDER_ONE)
		self.create_or_edit_reminder(REMINDER_TWO)

		reminders = self.get_all_reminder_values()
		
		for value in REMINDER_ONE.itervalues():
			self.assertIn(value, reminders)
		for value in REMINDER_TWO.itervalues():
			self.assertIn(value, reminders)
		for value in REMINDER_THREE.itervalues():
			self.assertNotIn(value, reminders)

		# Billy finishes his reminders and logs out.
		logout_button = self.browser.find_element_by_id('id_logout')
		logout_button.click()

		# Del logs in, sees no trace of Billy's reminders, and creates a few of his
		# own reminders.
		self.browser.get('%s%s' % (self.server_url, '/accounts/login/',))
		inputs = self.gather_form_inputs()
		inputs[0].send_keys('delbah@gmail.com')
		inputs[1].send_keys('123')
		submit_button = self.browser.find_element_by_id('id_login')
		submit_button.click()

		reminders = self.get_all_reminder_values()

		for value in REMINDER_ONE.itervalues():
			self.assertNotIn(value, reminders)
		for value in REMINDER_TWO.itervalues():
			self.assertNotIn(value, reminders)

		self.create_or_edit_reminder(REMINDER_THREE)

		reminders = self.get_all_reminder_values()

		for value in REMINDER_ONE.itervalues():
			self.assertNotIn(value, reminders)
		for value in REMINDER_TWO.itervalues():
			self.assertNotIn(value, reminders)
		for value in REMINDER_THREE.itervalues():
			self.assertIn(value, reminders)

		# Satisfied, Del logs out.
		logout_button = self.browser.find_element_by_id('id_logout')
		logout_button.click()

		# Billy logs in again, sees only his reminders, and then logs out
		self.browser.login_test_user()
		for value in REMINDER_ONE.itervalues():
			self.assertIn(value, reminders)
		for value in REMINDER_TWO.itervalues():
			self.assertIn(value, reminders)
		for value in REMINDER_THREE.itervalues():
			self.assertNotIn(value, reminders)

		logout_button = self.browser.find_element_by_id('id_logout')
		logout_button.click()