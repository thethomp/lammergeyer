from django.conf.urls import url

from accounts import views

urlpatterns = [
	url(r'^login/$', views.account_login, name='account_login'),
	url(r'^register/$', views.account_register, name='account_register'),
	url(r'^logout$', views.account_logout, name='account_logout'),
]