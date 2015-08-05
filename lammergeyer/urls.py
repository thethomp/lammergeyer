from django.conf.urls import include, url
from django.contrib import admin
from reminders import urls as reminders_urls
from accounts import urls as accounts_urls

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
	url(r'^reminders/', include(reminders_urls)),
	url(r'^accounts/', include(accounts_urls)),
]