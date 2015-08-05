from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout

from accounts.forms import LoginForm, RegisterForm

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
			form.save()
			return redirect('account_login')
	return render(request, 'accounts/register.html', {'form': form})