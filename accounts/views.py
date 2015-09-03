from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout

from accounts.forms import LoginForm, RegisterForm

from registration.models import RegistrationProfile
from registration.views import ActivationView

# Create your views here.

def account_login(request):
	if request.method == 'POST':
		form = LoginForm(data=request.POST)
		if form.is_valid():
			user = form.email_cache
			if user.is_active:
				django_login(request, user)
				return redirect('reminder_home')
	return render(request, 'accounts/login.html', {'form': LoginForm()})

def account_register(request):
	form = RegisterForm()
	if request.method == 'POST':
		form = RegisterForm(data=request.POST)
		if form.is_valid():
			user = form.save()
			inactive_user = RegistrationProfile.objects.create_inactive_user(
				site=None,
				new_user=user,
				send_email=False,
			)
			return redirect('account_login')
	return render(request, 'accounts/register.html', {'form': form})

def account_logout(request):
	django_logout(request)
	return redirect('account_login')

class AccountActivationView(ActivationView):

	def activate(self, request, *args, **kwargs):
		try:
			user = RegistrationProfile.objects.activate_user(
				kwargs['activation_key']
			)
			return user
		except RegistrationProfile.DoesNotExist:
			raise NotImplementedError

	def get_success_url(self, request, user):
		return 'account_login'