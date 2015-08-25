from django.conf.urls import url

from accounts import views

urlpatterns = [
	url(r'^login/$', views.account_login, name='account_login'),
	url(r'^register/$', views.account_register, name='account_register'),
	url(r'^logout$', views.account_logout, name='account_logout'),
	url(r'^activate/(?P<activation_key>\w+)/$', views.account_activation, name='registration_activate'),
]