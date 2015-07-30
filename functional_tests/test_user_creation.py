from .base import FunctionalTest

from unittest import skip

class NewUserTest(FunctionalTest):

	def test_new_visitor_can_create_account(self):
		# Della Bahee happens to find himself on the accounts page.
		## Url should be 'thethomp.info/accounts/login/'
		self.browser.get('%s%s' % (self.server_url, '/accounts/login/',))
		self.assertRegexpMatches(self.browser.current_url, '/accounts/login.+')

		# He is given the option to login with an email address and password, 
		# or register for a new reminders account.
		form = self.browser.find_element_by_tag_name('form')
		inputs = form.find_elements_by_tag_name('input')
		input_names = [input.get_attribute('name') for input in inputs]
		self.assertIn('email', input_names)
		self.assertIn('password', input_names)

		# Surprisingly, Del knows that he does not have an account yet. So he clicks on the
		# hyperlink 'Sign Up' and is redirected to a registration page
		## Should redirect to 'thethomp.info/accounts/register/'
		registration_url = self.browser.current_url
		self.assertRegexpMatches(registration, '/accounts/register.+')
		self.fail('Finish me!')

		# The registration page is similar to login page except for an additional field
		# password field with label 'Re-enter Password'

		# Del creates enters his email address into the appropriate field, then his password, and finally
		# confirms his password in the second password field.

		# Del clicks 'Register' button. He is redirected to an email confirmation page where he is prompted
		# to enter a validation code which verifies access to the email associated with the registration.

		# Del recieved the activation email and enters the code into the input box asking for it.
		# Again he is redirected but this time to a page which exclaiming 'Registration Successful!'

		# There is a hyperlink on this page called 'Log In' which takes Del back to the beginning, to the login
		# page
		self.browser.get('%s%s' % (self.server_url, '/accounts/login/',))
		self.assertRegexpMatches(self.browser.current_url, '/accounts/login.+')