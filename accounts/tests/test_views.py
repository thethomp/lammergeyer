import random
from unittest import skip
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.core.urlresolvers import resolve, reverse

from registration.models import RegistrationProfile

from accounts.views import (
	account_login, account_register, 
	account_logout, AccountActivationView
)
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

		expected_html = render_to_string('accounts/login.html', {'form': LoginForm})

		self.assertMultiLineEqual(response.content.decode(), expected_html)

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
		CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		response = self.client.post(
			'/accounts/login/',
			data={
				'email': 'jj@gmail.com',
				'password': '123'
			}
		)
		self.assertRedirects(response, '/reminders/home/')

	def test_logged_in_session_dict_has_user_id(self):
		user = CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		with self.assertRaises(KeyError):
			session = self.client.session
			session['_auth_user_id']
		self.client.login(email=user.email, password='123')
		session = self.client.session
		self.assertEqual(str(user.id), session['_auth_user_id'])

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

	def test_register_existing_email_displays_error(self):
		CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		response = self.client.post(
			'/accounts/register/',
			data=VALID_USER
		)
		self.assertIn('Email already in use', response.content.decode())

	def test_registration_profile_is_created_in_view(self):
		self.client.post(
			'/accounts/register/',
			data=VALID_USER
		)
		self.assertTrue(RegistrationProfile.objects.count(), 1)

	def test_register_view_assigns_registration_profile_to_user(self):
		self.client.post(
			'/accounts/register/',
			data=VALID_USER,
		)
		user = CustomUser.objects.first()
		profile = RegistrationProfile.objects.first()
		self.assertEqual(user, profile.user)

	def test_register_view_deactivates_user(self):
		self.client.post(
			'/accounts/register/',
			data=VALID_USER,
		)
		user = CustomUser.objects.first()
		self.assertFalse(user.is_active)

class AccountsLogoutTest(TestCase):
	maxDiff = None

	def test_logout_url_resolves_to_accounts_logout_view(self):
		found = resolve('/accounts/logout')
		self.assertEqual(found.func, account_logout)

	def test_logout_redirects(self):
		response = self.client.get('/accounts/logout')
		self.assertEqual(response.status_code, 302)

	def test_logout_redirects_to_login_page(self):
		response = self.client.get('/accounts/logout')
		self.assertRedirects(response, reverse('account_login'))

	def test_logout_view_logs_out_user(self):
		CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		self.client.post(
			'/accounts/login/',
			data={
				'email': 'jj@gmail.com',
				'password': '123'
			}
		)
		self.assertTrue(self.client.session['_auth_user_id'])
		self.client.get('/accounts/logout')
		self.assertFalse(self.client.session.get('_auth_user_id', None))

class AccountActivationViewTest(TestCase):

	@skip('skip for now')
	def test_activation_url_resolves_to_view(self):
		atof = 'abcdef'
		digits = '0123456789'
		random_string = ''.join(random.choice(atof + digits) for _ in range(40))
		found = resolve('/accounts/activate/%s/' % (random_string,))
		self.assertEqual(found.func, AccountActivationView.activate)

	def test_view_activates_user(self):
		user = CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		RegistrationProfile.objects.create_inactive_user(site=None, new_user=user, send_email=False)
		profile = RegistrationProfile.objects.first()
		self.client.get(
			'/accounts/activate/%s/' % (profile.activation_key,)
		)
		user.refresh_from_db()
		self.assertTrue(user.is_active)

	def test_view_redirects_on_successful_activation(self):
		user = CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		RegistrationProfile.objects.create_inactive_user(site=None, new_user=user, send_email=False)
		profile = RegistrationProfile.objects.first()
		response = self.client.get(
			'/accounts/activate/%s/' % (profile.activation_key,)
		)
		self.assertRedirects(response, reverse('account_login'))

	def test_view_displays_error_for_expired_keys(self):
		pass

	def test_view_displays_sensible_error_for_incorrect_key(self):
		pass

