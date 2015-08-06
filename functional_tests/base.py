from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

import sys

from accounts.models import CustomUser

REMINDER_ONE = {
	'id_title': 'Buy milk', 
	'id_alarm': '2015-06-22', 
	'id_snooze': '10.0', 
	'id_repeat': '24.0'
}
REMINDER_TWO = {
	'id_title': 'Buy beer', 
	'id_alarm': '2015-06-23', 
	'id_snooze': '15.0', 
	'id_repeat': '36.0'	
}
REMINDER_THREE = {
	'id_title': 'Meeting at 8 am', 
	'id_alarm': '2015-06-25', 
	'id_snooze': '20.0', 
	'id_repeat': '48.0'	
}
EMPTY_REMINDER = {
	'id_title': '', 
	'id_alarm': '', 
	'id_snooze': '', 
	'id_repeat': ''	
}

class FunctionalTest(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		super(FunctionalTest, cls).setUpClass()
		cls.server_url = cls.live_server_url

	@classmethod
	def tearDownClass(cls):
		super(FunctionalTest, cls).tearDownClass()

	def setUp(self):
		self.browser = webdriver.Firefox() 
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def create_or_edit_reminder(self, reminder, panel=None):
		"""
		The arguments reminder_button and submit_button are the html id's for expanding the
		reminder and submitting the reminder, respectively. The reminder_button either corresponds
		to the collapsible form for a new reminder, or the collapsible form of an existing reminder.
		The submit_button mirrors usage explained above but for submitting forms data in cases above.
		"""
		wait = WebDriverWait(self.browser, 10)
		panel_id = 'id_reminder_panel_'
		if panel:
			panel_id = panel
		reminder_panel = wait.until(expected_conditions.element_to_be_clickable((By.ID, panel_id)))

		buttons = reminder_panel.find_elements_by_tag_name('button')
		buttons[0].click()
		wait.until(expected_conditions.element_to_be_clickable((By.ID, buttons[1].get_attribute('id'))))

		inputs = reminder_panel.find_elements_by_tag_name('input')
		for input in inputs:
			text = input.get_attribute('id')
			if text in reminder:
				wait.until(expected_conditions.visibility_of(input))
				input.clear()
				inputbox = input.send_keys(reminder[text])
		
		wait.until(expected_conditions.element_to_be_clickable((By.ID, buttons[1].get_attribute('id'))))
		buttons[1].click()

	def safe_close_panel(self):
		wait = WebDriverWait(self.browser, 10)
		panel = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'id_reminder_panel_')))
		buttons = panel.find_elements_by_tag_name('button')
		buttons[0].click()
		wait.until(expected_conditions.invisibility_of_element_located((By.ID, buttons[1].get_attribute('id'))))

	def gather_form_inputs(self):
		form = self.browser.find_element_by_tag_name('form')
		inputs = form.find_elements_by_tag_name('input')
		inputs = [input for input in inputs if 'hidden' not in input.get_attribute('type')]
		return inputs

	def login_test_user(self):
		if not CustomUser.objects.filter(email='jj@gmail.com').exists():
			CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		self.browser.get('%s%s' % (self.server_url, '/accounts/login/',))
		inputs = self.gather_form_inputs()
		inputs[0].send_keys('jj@gmail.com')
		inputs[1].send_keys('123')
		submit_button = self.browser.find_element_by_id('id_login')
		submit_button.click()