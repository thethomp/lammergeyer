from django.conf.urls import patterns, include, url
from django.contrib import admin
from reminders import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url(r'^reminders/', include('reminders.urls')),
	url(r'^$', views.home_page, name='home')
]
