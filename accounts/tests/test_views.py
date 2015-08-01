from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.core.urlresolvers import resolve

from accounts.views import account_login, account_register
from accounts.forms import LoginForm, RegisterForm
from accounts.models import CustomUser
from .base import VALID_USER, INVALID_USER

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
	maxDiff = None

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

		expected_html = render_to_string('accounts/register.html', {'form': RegisterForm()})

		self.assertMultiLineEqual(response.content.decode(), expected_html)

	def test_register_page_only_does_not_save(self):
		request = HttpRequest()
		account_register(request)
		self.assertEqual(CustomUser.objects.count(), 0)

	def test_register_form_is_used(self):
		response = self.client.get(
			'/accounts/register/'
		)
		self.assertIsInstance(response.context['form'], RegisterForm)

	def test_can_save_a_POST_request(self):
		response = self.client.post(
			'/accounts/register/',
			data=VALID_USER
		)
		self.assertEqual(CustomUser.objects.count(), 1)
		saved_user = CustomUser.objects.first()
		self.assertEqual(saved_user.email, 'jj@gmail.com')
		self.assertNotEqual(saved_user.password, '123')

	def test_POST_request_redirects_to_login(self):
		response = self.client.post(
			'/accounts/register/',
			data=VALID_USER
		)
		self.assertRedirects(response, '/accounts/login/')

	def test_invalid_POST_renders_register_form(self):
		response = self.client.post(
			'/accounts/register/',
			data=INVALID_USER
		)
		self.assertIsInstance(response.context['form'], RegisterForm)

	def test_invalid_POST_displays_errors(self):
		response = self.client.post(
			'/accounts/register/',
			data=INVALID_USER
		)
		self.assertIn('An email address is required', response.content.decode())
		self.assertIn('Password cannot be blank', response.content.decode())