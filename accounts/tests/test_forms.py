from django.test import TestCase
from django.core.exceptions import ValidationError

from accounts.forms import RegisterForm
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
		self.assertIn('Email already already in use', form.as_p())