from django.conf.urls import url

from accounts import views

urlpatterns = [
	url(r'^login/$', views.account_login, name='account_login'),
]