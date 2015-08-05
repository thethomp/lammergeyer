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
		If errors are not raised this is probably the reason.
		I'm not sure if the 'if user.check_password(password)'
		failing causes the Except statement to execute. If it
		does not, we wont raise a ValidationError
		"""