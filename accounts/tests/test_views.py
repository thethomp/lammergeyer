from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.core.urlresolvers import resolve

from accounts.views import account_login, account_register
from accounts.forms import LoginForm, RegisterForm
from accounts.models import CustomUser

class AccountsLoginPageTest(TestCase):

	def test_login_url_resolves_to_account_login_view(self):
		found = resolve('/accounts/login/')
		self.assertEqual(found.func, account_login)

	def test_login_renders_login_template(self):
		response = self.client.get('/accounts/login/')
		self.assertTemplateUsed(response, 'accounts/login.html')

	def test_login_page_returns_correct_html(self):
		# Make an HttpRequest and return the account_login view response
		request = HttpRequest()
		response = account_login(request)

		expected_html = render_to_string('accounts/login.html')

		self.assertEqual(response.content.decode(), expected_html)

	def test_login_form_is_used(self):
		response = self.client.get(
			'/accounts/login/'
		)
		self.assertIsInstance(response.context['form'], LoginForm)

	def test_login_page_redirects_only_when_necessary(self):
		# Here the idea will be to check redirection when submitting a post
		# request that is invalid. Should stay on /accounts/login/ and display errors
		pass

	def test_login_page_does_not_save_user(self):
		self.client.get(
			'/accounts/login/',
		)
		self.assertEqual(CustomUser.objects.count(), 0)

	def test_login_page_redirects_after_POST(self):
		# Test if successful credentials redirect to /reminders/reminder_home for now
		pass

class AccountsRegisterPageTest(TestCase):
	
	def test_register_url_resolves_to_account_register_view(self):
		found = resolve('/accounts/register/')
		self.assertEqual(found.func, account_register)

	def test_register_renders_register_template(self):
		response = self.client.get('/accounts/register/')
		self.assertTemplateUsed(response, 'accounts/register.html')

	def test_register_page_returns_correct_html(self):
		# Make an HttpRequest and return the account_login view response
		request = HttpRequest()
		response = account_register(request)

		expected_html = render_to_string('accounts/register.html')

		self.assertEqual(response.content.decode(), expected_html)

	def test_register_form_is_used(self):
		response = self.client.get(
			'/accounts/register/'
		)
		self.assertIsInstance(response.context['form'], RegisterForm)