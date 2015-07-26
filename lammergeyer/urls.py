from django.conf.urls import include, url
from django.contrib import admin
from reminders import views as reminders_views
from reminders import urls as reminders_urls

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
	#url(r'^$', reminders_views.home_page, name='home'),
	url(r'^reminders/', include(reminders_urls)),
]