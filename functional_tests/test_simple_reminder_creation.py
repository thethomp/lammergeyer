from .base import FunctionalTest

from unittest import skip
from selenium import webdriver
from selenium.webdriver.support import expected_conditions

class NewVisitorTest(FunctionalTest):

	def test_new_user_lands_on_home_page_and_sees_correct_title(self):
		# Billy lands on the home page and sees the web service title.
		self.browser.get(self.server_url)
		self.assertIn(u'Your Reminders', self.browser.title.decode())

		# He then sees a button which says "Create a new reminder!"
		reminder_btn_text = self.browser.find_element_by_id('id_new_reminder_btn').text
		self.assertIn("Create a new reminder!", reminder_btn_text)

		# Billy clicks this button and a form window pops up
		self.browser.find_element_by_id('id_new_reminder_btn').click()
		self.assertTrue(expected_conditions.alert_is_present())

		# In the form window, Billy sees fields for reminder title, reminder time, 
		# reminder snooze, and reminder repeat options
		modal = self.browser.switch_to.alert.text
		self.assertIn('Reminder Title', modal)
		self.assertIn('Reminder Time', modal)
		self.assertIn('Reminder Snooze', modal)
		self.assertIn('Reminder Repeat', modal)

		#Finish the test
		self.fail("Finish me")