from unittest import skip
from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from accounts.models import CustomUser

from registration.models import RegistrationProfile

class UserModelTests(TestCase):

	def test_default_values(self):
		user = CustomUser()
		self.assertEqual(user.email, '')
		self.assertEqual(user.password, '')
		self.assertFalse(user.is_staff)
		self.assertFalse(user.is_superuser)

	def test_string_representation(self):
		user = CustomUser(email='jj@gmail.com', password='1234')
		self.assertEqual(str(user), 'jj@gmail.com')
		self.assertEqual(user.password, '1234')

	@skip('skipped')
	def test_email_is_primary_key(self):
		user = CustomUser()
		self.assertFalse(hasattr(user, 'id'))

	def test_custom_user_is_authenticated(self):
		user = CustomUser()
		self.assertTrue(user.is_authenticated())

class UserManagerTests(TransactionTestCase):

	def test_user_manager_creates_user(self):
		user = CustomUser.objects.create_user(email='jj@gmail.com', password='1234')
		self.assertEqual(CustomUser.objects.count(), 1)

	def test_user_manager_create_user_values_and_default_values(self):
		CustomUser.objects.create_user(email='jj@gmail.com', password='1234')
		first_user = CustomUser.objects.first()
		self.assertEqual(first_user.email, 'jj@gmail.com')
		# In CustomUserManager we are using set_password to store passwords
		# as a hash. So the assert below should be a NotEqual
		self.assertNotEqual(first_user.password, '1234')
		self.assertFalse(first_user.is_staff)
		self.assertFalse(first_user.is_superuser)

	def test_user_manager_forbids_empty_email_or_empty_password(self):
		# Remember that 'blank=False' by default for django char fields
		user = CustomUser(email='', password='')
		with self.assertRaises(ValidationError):
			user.save()
			user.full_clean()

	def test_password_is_not_stored_as_plain_text(self):
		CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		saved_user = CustomUser.objects.first()
		self.assertNotEqual(saved_user.password, '123')

	def test_duplicate_email_accounts_not_allowed(self):
		CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		with self.assertRaises(IntegrityError):
			CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		self.assertEqual(CustomUser.objects.count(), 1)

class UserRegistrationProfileTest(TestCase):

	def test_registration_profile_deactivates_user(self):
		user = CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		inactive_user = RegistrationProfile.objects.create_inactive_user(site=None, new_user=user)

		user = CustomUser.objects.first()
		self.assertFalse(user.is_active)

	def test_registration_profile_user_equals_custom_user(self):
		user = CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		profile = RegistrationProfile.objects.create_inactive_user(site=None, new_user=user)
		self.assertEqual(user, profile)