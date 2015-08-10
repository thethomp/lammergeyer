from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from unittest import skip

from .base import FunctionalTest

class NewUserTest(FunctionalTest):

	def test_new_visitor_can_create_account(self):
		# Della Bahee happens to find himself on the accounts page.
		## Url should be 'thethomp.info/accounts/login/'
		self.browser.get('%s%s' % (self.server_url, '/accounts/login/',))
		self.assertRegexpMatches(self.browser.current_url, '/accounts/login.+')

		# He is given the option to login with an email address and password, 
		# or register for a new reminders account.
		inputs = self.gather_form_inputs()
		input_names = [input.get_attribute('name') for input in inputs]
		self.assertIn('email', input_names)
		self.assertIn('password', input_names)

		a_tags = self.browser.find_elements_by_tag_name('a')
		a_text = [a.text for a in a_tags]
		self.assertIn('Register', a_text)
		a_tags[0].click()

		# Surprisingly, Del knows that he does not have an account yet. So he clicks on the
		# hyperlink 'Sign Up' and is redirected to a registration page
		## Should redirect to 'thethomp.info/accounts/register/'
		register_url = self.browser.current_url
		self.assertRegexpMatches(register_url, '/accounts/register.+')

		# The registration page is similar to login page except for an additional field
		# password field with label 'Re-enter Password'
		inputs = self.gather_form_inputs()
		input_names = [input.get_attribute('name') for input in inputs]
		self.assertIn('email', input_names)
		self.assertIn('password1', input_names)
		self.assertIn('password2', input_names)

		# Del enters his email address into the appropriate field, then his password, and finally
		# confirms his password in the second password field.
		wait = WebDriverWait(self.browser, 10)
		wait.until(expected_conditions.visibility_of(inputs[0]))
		inputs[0].send_keys('jj@gmail.com')
		inputs[1].send_keys('123')
		inputs[2].send_keys('123')

		# Del clicks 'Register' button. He is redirected to the login page where he can enter his credentials
		submit_button = self.browser.find_element_by_id('id_register')
		submit_button.click()

		self.assertRegexpMatches(self.browser.current_url, '/accounts/login.+')

		# Della Bahee is eager to test the reminder functionality so he quickly logs in with the values from
		# the registration page
		self.login_test_user()

		# No errors show up, and Del is redirected to the reminders app urls
		errors = self.browser.find_elements_by_css_selector('has-error')
		self.assertEqual(len(errors), 0)
		reminders_url = self.browser.current_url
		self.assertRegexpMatches(reminders_url, '/reminders/home.+')