from .base import FunctionalTest

from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

class NewVisitorTest(FunctionalTest):

	def test_new_user_lands_on_home_page_and_sees_correct_title(self):
		# Billy lands on the home page and sees the web service title.
		self.browser.get(self.server_url)
		self.assertIn(u'Your Reminders', self.browser.title.decode())

		# He then sees a button which says "Create a new reminder!"
		#self.browser.find_element_by_id()

		# Billy clicks this button and a form window pops up

		# In the form window, Billy sees fields for reminder title, reminder time, 
		# reminder snooze, and reminder repeat options

		#Finish the test
		self.fail("Finish me")