from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from reminders.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
# Create your views here.

def register(request):
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

def user_login(request):
	context = RequestContext(request)

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		
		user = authenticate(username=username, password=password)

		if user: #successful login
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/reminders/')
			else:
				return HttpResponse("You're reminder.me account is currently disabled")
		else: # bad login info
			print "Invalid login info: {0}, {1}".format(email, password)
			return HttpResponse("Invalid login credentials")

	else: #not a post, probably a get, show login page
		return render_to_response('reminders/login.html', {}, context)


def index( request ):
	#return render_to_response
	return HttpResponse("hello world. You're at the Reminders index!<br /><a href=""/reminders/register/"">Register Here</a><br /><a href=""/reminders/login/"">Log In</a>")
