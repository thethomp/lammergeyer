from django.test import TestCase

from accounts.forms import RegisterForm

class TestRegisterForm(TestCase):

	def test_form_has_labels(self):
		form = RegisterForm()
		self.assertIn('Email Address', form.as_p())
		self.assertIn('Password', form.as_p())
		self.assertIn('Repeat Password', form.as_p())

	def test_form_validation_for_blank_form(self):
		form = RegisterForm(
			data={
				'email':'',
				'password1': '',
				'password2': ''
			}
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

	def test_custom_form_save_works(self):
		pass

	def test_password_stored_as_hash(self):
		pass