from django.conf.urls import patterns, include, url
from django.contrib import admin
from reminders import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	#url(r'^reminders/', include('reminders.urls')),
	url(r'^$', views.home_page, name='home'),
	url(r'^reminders/(\d+)/$', views.view_reminders, name='view_reminders'),
	url(r'^reminders/(\d+)/add_reminder$', views.add_reminder, name='add_reminder'),
	url(r'^reminders/new$', views.new_reminder_list, name='new_reminder_list'),
]