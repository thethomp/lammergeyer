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

@login_required
def account(request):
	return HttpResponse("This will be the Account page some day!")

@login_required
def home(request):
	r_user = request.user
	#print r_user
	#print User.objects.get(username='hi').id
	#print UserProfile.objects.get(id=8)
	reminder_list = Reminder.objects.filter(user=UserProfile.objects.get(user_id=User.objects.get(username=r_user).id))
	#reminder_list = Reminder.objects.filter(user=r_user)
	print reminder_list
	template = loader.get_template('reminders/home.html')
	context = RequestContext(request, {'reminder_list' : reminder_list,})
	return HttpResponse(template.render(context))	
#	return HttpResponse("This will be the Reminders home page some day!")

@login_required
def user_logged_in(request):
	template = loader.get_template('reminders/logged-in.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context)) #'reminders/logged-in.html')


def register(request):

	if request.user.is_authenticated():
		return HttpResponseRedirect('/reminders/logged-in/')

	context = RequestContext(request)
	registered = False
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			
			profile = profile_form.save(commit=False)
			profile.user = user

			profile.save()
			registered = True
		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render_to_response(
			'reminders/register.html',
			{'user_form': user_form, 'profile_form' : profile_form, 'registered' : registered},
			context)	

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/reminders/logout/')


def user_login(request):
	context = RequestContext(request)

	if request.method == 'POST':
		#email = request.POST['email']
		username = request.POST['username']
		#email = request.POST.get('email', False)
		password = request.POST['password']
		
		user = authenticate(username=username, password=password)
		#user = authenticate(email=email, password=password)

		if user: #successful login
			if user.is_active:
				login(request, user)
				return render_to_response('reminders/logged-in.html', {}, context)
				#return HttpResponse("You're successfully logged in to remind.me! Neat stuff is on it's way, stay tuned!")
				#return HttpResponseRedirect('/reminders/perrty-login/')
			else:
				return HttpResponse("You're reminder.me account is currently disabled")
		else: # bad login info
			print "Invalid login info: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login credentials")

	else: #not a post, probably a get, show login page
		return render_to_response('reminders/login.html', {}, context)


def about(request):
	return HttpResponse("ABOUT page placeholder")

def index( request ):
	#return render_to_response
	return HttpResponse("You're at the Reminders index!<br /><a href=""/reminders/register/"">Register Here</a><br /><a href=""/reminders/login/"">Log In</a>")

def home_page(request):
	return render(request, 'reminders/home.html', {'form': ReminderForm()})

def reminder_home(request):
	return render(request, 'reminders/reminder_home.html', {'form': ReminderForm()})

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

def new_reminder_list(request):
	form = ReminderForm(data=request.POST)
	if form.is_valid():
		list_ = List.objects.create()
		form.save(for_list=list_)
		return redirect(list_)
	else:
		return render(request, 'reminders/home.html', {'form': form})

def edit_reminder(request, pk):
	instance = Reminder.objects.get(pk=pk)
	if request.method == 'POST':
		form = ReminderForm(data=request.POST, instance=instance)
		if form.is_valid():
			form.save(for_list=instance.list)
			return redirect(instance.list)
	reminders = Reminder.objects.filter(list=instance.list)
	forms = []
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
	return render(request, 'reminders/reminder_list.html', {'list': instance.list, 'form': form, 'forms': forms})