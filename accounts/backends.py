from django.conf import settings
from django.contrib.auth.models import check_password
from accounts.models import CustomUser

class EmailAuthBackend(object):
	"""
	Custom authentication backend for email-based users
	"""

	def authenticate(self, email=None, password=None):
		"""
		Check if the email exists then check_password
		"""
		try:
			user = CustomUser.objects.get(email=email)
			if user.check_password(password):
				return user
		except CustomUser.DoesNotExist:
			return None
		"""
		If the user exists but the password does not check out,
		we still return None. That is, all modules return None 
		if we don't explicitly tell them to return something
		"""

	def get_user(self, user_id):
		"""
		We need to implement this method so we can use django's
		login
		"""
		try:
			user = CustomUser.objects.get(pk=user_id)
			if user.is_active:
				return user
			return None
		except CustomUser.DoesNotExist:
			return None