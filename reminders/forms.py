from reminders.models import Reminder
from django.contrib.auth.models import User
from django import forms

EMPTY_REMINDER_TITLE_ERROR = 'Reminders need titles!'

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		#model = UserProfile
		fields = ('phone',)

class ReminderForm(forms.ModelForm):
	
	class Meta:
		model = Reminder
		fields = ('title',)
		widgets = {
			'title': forms.fields.TextInput(attrs={
				'placeholder': 'Enter a reminder',
			}),
		}
		error_messages = {
			'title': {'required': EMPTY_REMINDER_TITLE_ERROR}
		}
	
