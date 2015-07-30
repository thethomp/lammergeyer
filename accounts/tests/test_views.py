from unittest import TestCase

class AccountsLoginPageTest(TestCase):

	def test_login_url_resolves_to_account_login_view(self):
		found = self.client.get('/accounts/login/')
		self.assertEqual(found.func, account_login)

	def test_login_renders_login_template(self):
		response = self.client.get('/acounts/login/')
		self.assertTemplateUsed(response, 'accounts/login.html')

	def test_login_page_returns_correct_html(self):
		# Make an HttpRequest and return the account_login view response
		request = HttpRequest()
		response = account_login(request)

		expected_html = render_to_string('accounts/login.html')

		self.assertEqual(response.content.decode(), expected_html)

	def test_extended_user_model_form_is_used(self):
		pass

	def test_login_page_redirects_only_when_necessary(self):
		pass

	def test_login_page_does_not_save_user(self):
		pass

	def test_login_page_redirects_after_POST(self):
		pass

class AccountsRegisterPageTest(TestCase):
	pass