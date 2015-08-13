from django import forms
from django.utils.translation import ugettext_lazy as _

from accounts.models import CustomUser
from django.contrib.auth import authenticate
# forms.ModelForms has their own normalize_email I believe
from accounts.utils import normalize_email as ne

class LoginForm(forms.Form):
	"""
	Could quite possbile inherit from django's AuthenticationForm
	and then override the form with what we need (custom backend with
	authenticate method, and a few other odds and ends) but I'm not 
	sure it is even worth it at this point. Further research required
	"""

	email = forms.EmailField(label=_("Email Address"))
	password = forms.CharField(label=_("Password"),
		widget=forms.PasswordInput
	)

	error_messages = {
		'invalid_login': _('Incorrect email or password'),
		'inactive': _('This email has not been activated')
	}

	class Meta:
		fields = ('email', 'password',)

	def __init__(self, request=None, *args, **kwargs):
		"""
		Very simple overriding of Form init to get rid of the labels
		nonsense, and customize more towards our model
		"""
		self.request = request
		self.email_cache = None
		super(LoginForm, self).__init__(*args, **kwargs)

	def clean(self):
		"""
		Override clean method and insert our custom authentication backend 
		-- Otherwise heavily borrowed from django AuthenticationForm
		"""
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')

		if email and password:
			self.email_cache = authenticate(email=email, password=password)
			# Authenticate calls check_password(...) which returns a boolean.
			# In authenticate(...) try block, if if-statement fails, we skip
			# Except and that is the end of the method... so we return None
			if self.email_cache is None:
				raise forms.ValidationError(
					self.error_messages['invalid_login'],
					code='invalid_login'
				)
			else:
				# If the email is inactive, we will raise a validation error
				# and this will cause form.is_valid() to fail presumably
				self.confirm_login_allowed(self.email_cache)
		return self.cleaned_data

	def confirm_login_allowed(self, email):
		"""
		From django src -- 
		Controls whether the given User may log in. This is a policy setting, 
		independent of end-user authentication. This default behavior is to 
		allow login by active users, and reject login by inactive users.

		**Note**
		This is the exact policy setting we desire if we are going to use 
		email confirmation to verify ownership of an email account. We can 
		set is_active to True once the cofirmation email situation is resolved
		**Endnote**

		If the given user cannot log in, the method should raise a 
		''forms.ValidationError''.

		If the given user may log in, the method should return None
		"""
		if not email.is_active:
			raise forms.ValidationError(
				self.error_messages['inactive'],
				code='inactive'
			)
	def get_user(self):
		return self.email_cache


class RegisterForm(forms.ModelForm):

	error_messages = {
		'password_mismatch': _('Passwords do not match'),
		'email_exists':_('Email already in use'),
	}

	email = forms.EmailField(label=_("Email Address"),
		error_messages={
		'required': 'An email address is required',
		'invalid': 'The given email address is invalid'
		},
	)
	password1 = forms.CharField(label=_("Password"),
		widget=forms.PasswordInput,
		error_messages = {
			'required': 'Password cannot be blank'
		},
	)
	password2 = forms.CharField(label=_("Repeat Password"),
		widget=forms.PasswordInput,
		error_messages = {
			'required': 'Password cannot be blank'
		},
	)

	class Meta:
		model = CustomUser
		fields = ('email', 'password1', 'password2',)

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code='password_mismatch',
			)
		return password2

	def clean_email(self):
		"""
		Normalize email. They check for existing emails in django-oscar
		at this point. However, validation at the database level should
		kick in when we try to save it??? If not, we can do it manually
		with a query set.
		"""
		email = ne(self.cleaned_data['email'])
		if CustomUser.objects.filter(email=email).exists():
			raise forms.ValidationError(
				self.error_messages['email_exists'],
				code='email_exists'
			)
		return email

	def save(self, commit=True):
		"""
		Save the form -- copy of django's save() in UserCreationForm
		"""
		user = super(RegisterForm, self).save(commit=False)
		# We don't commit here because we want to modify the password.
		# In fact, any time we want to change some of the data before 
		# we save it, we can override the save with commit=False. SO 
		# has the use case as populating null fields at this point. Also
		# can be used in the views for setting foreign keys.
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user