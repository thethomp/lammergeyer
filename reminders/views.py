from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime

from .models import Reminder
from reminders.forms import ReminderForm
import reminders.timezone_object as tzobj

@login_required
def reminder_home(request):
	form = ReminderForm()
	if request.method == 'POST':
		form = ReminderForm(data=request.POST)
		if form.is_valid():
			form.save(for_user=request.user)
			return redirect('reminder_home')
	# Supposedly this counts as one db hit, is cached, and later look-ups use the cached query set
	reminders = Reminder.objects.filter(user=request.user)
	forms = [(
		ReminderForm(
			initial={
		 			'title': reminder.title,
		 			'alarm': reminder.alarm,
		 			'snooze': reminder.snooze,
		 			'repeat': reminder.repeat
		 	}), 
		reminder.pk) 
	for reminder in reminders
	]
	return render(request, 'reminders/reminder_list.html', {'form': form, 'forms': forms})

@login_required
def edit_reminder(request, pk):
	## Two db hits
	edited_reminder = Reminder.objects.get(pk=pk)
	## Here
	if request.method == 'POST':
		form = ReminderForm(data=request.POST, instance=edited_reminder)
		if form.is_valid():
			form.save(for_user=request.user)
			return redirect('reminder_home')
	reminders = Reminder.objects.filter(user=request.user)
	forms = []
	## Here; Can probably optimize later
	for reminder in reminders:
		if reminder.pk == int(pk):
			# Append form that failed validation
			forms.append((form, reminder.pk))
		else:
			forms.append(
				(ReminderForm(
					initial={
			 			'title': reminder.title,
			 			'alarm': reminder.alarm,
			 			'snooze': reminder.snooze,
			 			'repeat': reminder.repeat
			 		}), reminder.pk)
			)
	return render(request, 'reminders/reminder_list.html', {'form': ReminderForm(), 'forms': forms})