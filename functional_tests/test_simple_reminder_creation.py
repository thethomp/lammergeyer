from .base import FunctionalTest

from unittest import skip
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys

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
		expected_placeholders = ['Enter a reminder', 'MM/DD/YYYY', 'Enter snooze', 'Enter repeat']
		self.assertEqual(placeholders, expected_placeholders)

		# Billy is not ready to add a reminder so he collapses the form
		reminder_btn_text = self.browser.find_element_by_id('id_new_reminder_btn')
		reminder_btn_text.click()
		self.assertEqual(reminder_btn_text.get_attribute('aria-expanded'), 'false')

	def test_new_user_can_create_and_display_a_new_reminder(self):
		# Billy is ready to create a new reminder so he expands the new reminder panel
		self.browser.get(self.server_url)
		self.browser.find_element_by_id('id_new_reminder_btn').click()

		# Four fields are necessary for a reminder
		form = self.browser.find_element_by_tag_name('form')
		fields = [input for input in form.find_elements_by_tag_name('input')]
		self.assertEqual(len(fields), 5)

		# A new reminder is created to "Buy milk"
		reminder_title = self.browser.find_element_by_id('id_new_reminder_title')
		reminder_title.send_keys('Buy milk\n')

		# The reminder is set for 06/23/2015
		reminder_alarm = self.browser.find_element_by_id('id_new_reminder_alarm')
		reminder_alarm.send_keys('06/23/2015\n')

		# The reminder is given a snooze of '10'
		reminder_snooze = self.browser.find_element_by_id('id_new_reminder_snooze')
		reminder_snooze.send_keys('10\n')

		# Finally, the reminder is given a repeat of 'T' meaning that the reminder is only valid for today
		# versus multi-day reminders
		reminder_repeat = self.browser.find_element_by_id('id_new_reminder_repeat')
		reminder_repeat.send_keys('T')
		reminder_repeat.send_keys(Keys.ENTER)

		# He then clicks "Save" and the page is updated to display the new reminder as a button.
		# The button reads the reminder title "Buy milk"
		#import time; time.sleep(10)
		reminder_btn = self.browser.find_element_by_id('id_reminder_btn')
		self.assertEqual('Buy milk', reminder_btn.text)

		# Clicking on the button expands the reminder that was created above
		reminder_btn.click()
		reminder_section = self.browser.find_element_by_id('id_reminder_section')
		reminders = [reminder.text for reminder in reminder_section.find_elements_by_tag_name('input')]
		self.assertIn('Buy milk', reminders)
		self.assertIn('06/23/2015', reminders)
		self.assertIn('10', reminders)
		self.assertIn('T', reminders)
