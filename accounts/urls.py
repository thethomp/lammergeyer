from django.conf.urls import url

from accounts import views
from accounts.views import AccountActivationView

urlpatterns = [
	url(r'^login/$', views.account_login, name='account_login'),
	url(r'^register/$', views.account_register, name='account_register'),
	url(r'^logout$', views.account_logout, name='account_logout'),
	url(r'^activate/(?P<activation_key>\w+)/$', AccountActivationView.as_view(), name='registration_activate'),
]