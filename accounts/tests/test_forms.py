from django.test import TestCase
from django.core.exceptions import ValidationError

from registration.models import RegistrationProfile

from accounts.forms import RegisterForm, LoginForm
from accounts.models import CustomUser
from .base import VALID_USER, INVALID_USER

class TestRegisterForm(TestCase):

	def test_form_has_labels(self):
		form = RegisterForm()
		self.assertIn('Email Address', form.as_p())
		self.assertIn('Password', form.as_p())
		self.assertIn('Repeat Password', form.as_p())

	def test_form_validation_for_blank_form(self):
		form = RegisterForm(
			data=INVALID_USER
		)
		self.assertFalse(form.is_valid())
		self.assertIn("An email address is required" , form.errors['email'])
		self.assertIn("Password cannot be blank", form.errors['password1'])
		self.assertIn("Password cannot be blank", form.errors['password2'])

	def test_form_validation_for_blank_email(self):
		form = RegisterForm(
			data={
				'email':'',
				'password1': '123',
				'password2': '1234'
			}
		)
		self.assertFalse(form.is_valid())
		self.assertIn("An email address is required" , form.errors['email'])

	def test_form_validation_for_invalid_email(self):
		form = RegisterForm(
			data={
				'email':'invalid',
				'password1': '123',
				'password2': '1234'
			}
		)
		self.assertFalse(form.is_valid())
		self.assertIn("The given email address is invalid" , form.errors['email'])

	def test_clean_email_converts_to_lower_case(self):
		form = RegisterForm(
			data={
				'email':'Jj@example.com',
				'password1': '123',
				'password2': '1234'
			}
		)
		self.assertFalse(form.is_valid())
		self.assertEqual(form.cleaned_data['email'], 'jj@example.com')

	def test_form_validation_for_blank_password1(self):
		form = RegisterForm(
			data={
				'email':'jj@example.com',
				'password1': '',
				'password2': '1234'
			}
		)
		self.assertFalse(form.is_valid())
		self.assertIn("Password cannot be blank", form.errors['password1'])

	def test_form_validation_for_blank_password2(self):
		form = RegisterForm(
			data={
				'email':'jj@example.com',
				'password1': '123',
				'password2': ''
			}
		)
		self.assertFalse(form.is_valid())
		self.assertIn("Password cannot be blank", form.errors['password2'])

	def test_form_validation_for_mismatched_passwords(self):
		form = RegisterForm(
			data={
				'email':'jj@example.com',
				'password1': '123',
				'password2': '1234'
			}
		)
		self.assertFalse(form.is_valid())
		self.assertIn("Passwords do not match", form.errors['password2'])

	def test_custom_form_save_updates_db(self):
		form = RegisterForm(
			data=VALID_USER
		)
		self.assertTrue(form.is_valid())
		form.save()
		self.assertEqual(CustomUser.objects.count(), 1)
		saved_user = CustomUser.objects.first()
		self.assertEqual(saved_user.email, 'jj@gmail.com')
		self.assertNotEqual(saved_user.password, '123')

	def test_password_stored_as_hash(self):
		form = RegisterForm(
			data=VALID_USER
		)
		form.save()
		saved_user = CustomUser.objects.first()
		self.assertNotEqual(saved_user.password, '123')

	def test_form_displays_existing_email_error(self):
		CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		form = RegisterForm(
			data=VALID_USER
		)
		self.assertFalse(form.is_valid())
		self.assertIn('Email already in use', form.as_p())

	def test_form_creates_active_user(self):
		form = RegisterForm(
			data=VALID_USER
		)
		form.save()
		user = CustomUser.objects.first()
		self.assertTrue(user.is_active)

	def test_form_returns_same_user(self):
		form = RegisterForm(
			data=VALID_USER
		)
		user = form.save()
		saved_user = CustomUser.objects.first()
		self.assertEqual(user, saved_user)

class LoginFormTest(TestCase):

	def test_form_is_labeled(self):
		form = LoginForm()
		self.assertIn('Email Address', form.as_p())
		self.assertIn('Password', form.as_p())

	def test_form_accepts_valid_credentials(self):
		CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		form = LoginForm(data={'email': 'jj@gmail.com', 'password': '123'})
		self.assertTrue(form.is_valid())

	def test_form_raises_error_on_invalid_password(self):
		# "That password is incorrect"
		CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		form = LoginForm(data={'email': 'jj@gmail.com', 'password': '1234'})
		self.assertFalse(form.is_valid())
		self.assertIn('Incorrect email or password', form.errors['__all__'])

	def test_form_raises_error_on_invalid_email(self):
		# "Email does not exist"
		CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		form = LoginForm(data={'email': 'j@gmail.com', 'password': '1234'})
		self.assertFalse(form.is_valid())
		self.assertIn('Incorrect email or password', form.errors['__all__'])

	def test_form_raises_error_on_blank_email(self):
		pass

	def test_form_raises_error_on_blank_password(self):
		pass

	def test_authenticate_returns_a_user_if_user_exists(self):
		CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		from accounts.backends import EmailAuthBackend
		backend = EmailAuthBackend()
		user = backend.authenticate(email='jj@gmail.com', password='123')
		self.assertTrue(user)

	def test_authenticate_returns_None_if_user_does_not_exist(self):
		from accounts.backends import EmailAuthBackend
		backend = EmailAuthBackend()
		user = backend.authenticate(email='jj@gmail.com', password='123')
		self.assertFalse(user)

	def test_authenticate_returns_None_if_password_is_wrong(self):
		CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		from accounts.backends import EmailAuthBackend
		backend = EmailAuthBackend()
		user = backend.authenticate(email='jj@gmail.com', password='1234')
		self.assertFalse(user)