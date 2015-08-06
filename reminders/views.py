from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime

from .models import Reminder, List
from reminders.forms import UserForm, UserProfileForm, ReminderForm
import reminders.timezone_object as tzobj
# Create your views here.

def home_page(request):
	return render(request, 'reminders/home.html', {'form': ReminderForm()})

@login_required
def reminder_home(request):
	return render(request, 'reminders/reminder_home.html', {'form': ReminderForm()})

@login_required
def view_reminders(request, list_id):
	list_ = List.objects.get(id=list_id)
	form = ReminderForm()
	if request.method == 'POST':
		form = ReminderForm(data=request.POST)
		if form.is_valid():
			form.save(for_list=list_)
			return redirect(list_)
	# Supposedly this counts as one db hit, is cached, and later look-ups use the cached query set
	reminders = Reminder.objects.filter(list=list_)
	forms = [
		(ReminderForm(initial={
		 			'title': reminder.title,
		 			'alarm': reminder.alarm,
		 			'snooze': reminder.snooze,
		 			'repeat': reminder.repeat
		 		}), reminder.pk) for reminder in reminders
	]
	return render(request, 'reminders/reminder_list.html', {'list': list_, 'form': form, 'forms': forms})

@login_required
def new_reminder_list(request):
	form = ReminderForm(data=request.POST)
	if form.is_valid():
		list_ = List.objects.create()
		form.save(for_list=list_)
		return redirect(list_)
	else:
		return render(request, 'reminders/home.html', {'form': form})

@login_required
def edit_reminder(request, list_id, pk):
	## Two db hits
	edited_reminder = Reminder.objects.get(pk=pk)
	## Here
	form = ReminderForm(instance=edited_reminder)
	if request.method == 'POST':
		form = ReminderForm(data=request.POST, instance=edited_reminder)
		if form.is_valid():
			form.save(for_list=edited_reminder.list)
			return redirect(edited_reminder.list)
	reminders = Reminder.objects.filter(list=edited_reminder.list)
	forms = []
	## Here; Can probably optimize later
	for reminder in reminders:
		if reminder.pk == pk:
			forms.append(form)
		else:
			forms.append((ReminderForm(initial={
			 			'title': reminder.title,
			 			'alarm': reminder.alarm,
			 			'snooze': reminder.snooze,
			 			'repeat': reminder.repeat
			 		}), reminder.pk))
	form = ReminderForm()
	return render(request, 'reminders/reminder_list.html', {'list': edited_reminder.list, 'form': form, 'forms': forms})