from django.shortcuts import render

from accounts.forms import LoginForm, RegisterForm

# Create your views here.

def account_login(request):
	return render(request, 'accounts/login.html', {'form': LoginForm()})

def account_register(request):
	return render(request, 'accounts/register.html', {'form': RegisterForm()})