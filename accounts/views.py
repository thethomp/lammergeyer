from django.shortcuts import render, redirect

from accounts.forms import LoginForm, RegisterForm

# Create your views here.

def account_login(request):
	return render(request, 'accounts/login.html', {'form': LoginForm()})

def account_register(request):
	form = RegisterForm()
	if request.method == 'POST':
		form = RegisterForm(data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('account_login')
	return render(request, 'accounts/register.html', {'form': form})