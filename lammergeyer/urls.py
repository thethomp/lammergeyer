from django.conf.urls import patterns, include, url
from django.contrib import admin
from reminders import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	#url(r'^reminders/', include('reminders.urls')),
	url(r'^$', views.home_page, name='home'),
	url(r'^reminders/the-only-reminder-list-in-the-world/$', views.view_reminders, name='view_reminders'),
]
