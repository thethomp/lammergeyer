from django import forms

from reminders.models import Reminder

EMPTY_REMINDER_TITLE_ERROR = 'Reminders need titles!'

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