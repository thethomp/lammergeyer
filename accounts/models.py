from django.db import models
from django.contrib.auth import models as auth_models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# Create your models here.

class CustomUserManager(auth_models.BaseUserManager):

	def create_user(self, email, password, **extra_arguments):
		"""
		Creates custom user that is based off the supplied email.
		"""
		
		if not email:
			raise ValueError('Email cannot be empty!')

		user = self.model(email=email)
		user.set_password(password)
		user.save(using=self._db)
		return user
		
class CustomUser(auth_models.AbstractBaseUser,
				   auth_models.PermissionsMixin):
	"""
	More or less copied from django-oscar and django AbstractBaseUser implementations. Check GitHub and Docs.
	https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser
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
	# Override AbstractBaseUser is_active class attribute with a field so the database can track this value
	# on a per user basis.
	is_active = models.BooleanField(
		_('active'),
		default=True,
		help_text=_(
			'Designates whether this user should be treated as active.'
			'Unselect this instead of deleting accounts'
		),
	)
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
	USERNAME_FIELD = 'email'

	objects = CustomUserManager()

	def __unicode__(self):
		return self.email