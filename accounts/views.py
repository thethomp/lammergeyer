from django.shortcuts import render

# Create your views here.

def account_login(request):
	return render(request, 'accounts/login.html')