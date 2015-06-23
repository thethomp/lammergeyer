from .base import FunctionalTest

from unittest import skip
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException

class NewVisitorTest(FunctionalTest):

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
		expected_placeholders = ['Enter a reminder', 'Enter alarm', 'Enter snooze', 'Enter repeat']
		self.assertEqual(placeholders, expected_placeholders)

		# Billy is not ready to add a reminder so he collapses the form
		reminder_btn_text = self.browser.find_element_by_id('id_new_reminder_btn')
		reminder_btn_text.click()
		self.assertEqual(reminder_btn_text.get_attribute('aria-expanded'), 'false')

		#Finish the test
		self.fail("Finish me")