from django.conf.urls import patterns, url

from reminders import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logged-in/$', views.user_logged_in, name='logged-in'),
	#url(r'^home/$', views.home, name='home'),
	url(r'^account/$', views.account, name='account'),
	url(r'^about/$', views.about, name='about'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', name="logout"),
	url(r'^new$', views.new_reminder_list, name='new_reminder_list'),
	url(r'^(\d+)/$', views.view_reminders, name='view_reminders'),
	url(r'^(?P<list_id>\d+)/edit_reminder/(?P<pk>\d+)$', views.edit_reminder, name='edit_reminder'),
	url(r'^home/$', views.reminder_home, name='reminder_home'),
]
# If you use a named capture group, then keyword arguments are used;
# otherwise, positional arguments are used. One or the other apparently.
# So if you use a capture group for one variable, but pass several in the
# url headers, you will only have access to the kwarg in the view of the 
# variable defined by a capture group.