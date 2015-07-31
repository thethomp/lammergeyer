from django.db import models
from django.contrib.auth import models as auth_models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class CustomUserManager(auth_models.BaseUserManager):

	def create_user(self, email, password, **extra_arguments):
		
		if not email:
			raise ValueError('Email cannot be empty!')

		user = self.model(
			email=email, password=password,
		)
		user.save(using=self._db)
		return user
		
class CustomUser(auth_models.AbstractBaseUser,
				   auth_models.PermissionsMixin):
	# https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser

	"""
	More or less copied from django-oscar and django AbstractBaseUser implementations. Check GitHub
	https://github.com/django-oscar/blob/master/src/apps/customer/abstract_models.py
	https://github.com/django/django/blob/master/django/contrib/auth/models.py 
	"""

	email = models.EmailField(max_length=254, default='', unique=True)
	is_staff = models.BooleanField(
		_('Staff status'),
		default=False,
		help_text=_(
			'Designates whether this user can log into this admin site.'
		),
	)
	

	USERNAME_FIELD = 'email'

	objects = CustomUserManager()