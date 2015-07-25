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
		fields = ('title','alarm','snooze','repeat',)
		widgets = {
			'title': forms.fields.TextInput(attrs={
				'placeholder': 'Enter a reminder',
			}),
			'alarm': forms.fields.DateTimeInput(attrs={
				'placeholder': 'MM/DD/YYYY'
			}, format=('%Y-%m-%d')),
			'snooze': forms.fields.TextInput(attrs={
				'placeholder': 'Enter snooze'
			}),
			'repeat': forms.fields.TextInput(attrs={
				'placeholder': 'Enter repeat'
			})
		}
		error_messages = {
			'title': {'required': EMPTY_REMINDER_TITLE_ERROR}
		}

	def save(self, for_list):
		self.instance.list = for_list
		return super(ReminderForm, self).save()
	
class ExistingReminderForm(ReminderForm):

	def __init__(self, for_reminder, *args, **kwargs):
		super(ExistingReminderForm, self).__init__(*args, **kwargs)
		self.instance.reminder = for_reminder