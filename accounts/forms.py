from django import forms
from django.utils.translation import ugettext_lazy as _

from accounts.models import CustomUser
# forms.ModelForms has their own normalize_email I believe
from accounts.utils import normalize_email as ne

class LoginForm():
	pass

class RegisterForm(forms.ModelForm):

	error_messages = {
		'password_mismatch': _('Passwords do not match'),
	}

	email = forms.EmailField(label=_("Email Address"), 
		error_messages={
		'required': 'An email address is required',
		'invalid': 'The given email address is invalid'
		}
	)
	password1 = forms.CharField(label=_("Password"),
		error_messages = {
			'required': 'Password cannot be blank'
		}
	)
	password2 = forms.CharField(label=_("Repeat Password"),
		error_messages = {
			'required': 'Password cannot be blank'
		}
	)

	class Meta:
		model = CustomUser
		fields = ('email',)

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
		return email