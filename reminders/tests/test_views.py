import datetime
from unittest import skip

from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils import timezone

from accounts.models import CustomUser
from reminders.views import reminder_home
from reminders.models import Reminder
from reminders.forms import ReminderForm, EMPTY_REMINDER_TITLE_ERROR
from base import REMINDER_ONE, REMINDER_TWO, EMPTY_REMINDER, UserTestCase
import reminders.timezone_object as tzobj

class RemindersPageTest(UserTestCase):
	maxDiff = None

	def test_reminders_home_url_resolves_to_reminder_home_view(self):
		found = resolve('/reminders/home/')
		self.assertEqual(found.func, reminder_home)

	def test_reminder_home_returns_correct_html(self):
		request = HttpRequest()
		request.user = self.user
		response = reminder_home(request)

		expected_html = render_to_string('reminders/reminder_list.html', {'form': ReminderForm()})

		self.assertMultiLineEqual(response.content.decode(), expected_html)

	def test_reminder_home_renders_reminder_list_template(self):
		response = self.client.get('/reminders/home/')
		self.assertTemplateUsed(response, 'reminders/reminder_list.html')

	def test_reminder_home_uses_reminder_form(self):
		response = self.client.get('/reminders/home/')
		self.assertIsInstance(response.context['form'], ReminderForm)

	def test_reminder_home_only_saves_reminders_when_necessary(self):
		request = HttpRequest()
		request.user = self.user
		reminder_home(request)
		self.assertEqual(Reminder.objects.count(), 0)

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/reminders/home/',
			data=REMINDER_ONE
		)

		self.assertRedirects(response, '/reminders/home/')

	def test_can_save_a_POST_request(self):
		self.client.post(
			'/reminders/home/',
			data=REMINDER_ONE
		)
		self.assertEqual(Reminder.objects.count(), 1)
		new_item = Reminder.objects.first()
		self.assertEqual(new_item.title, 'Buy milk')

class ReminderListViewTest(UserTestCase):

	def post_invalid_input(self):
		return self.client.post(
			'/reminders/home/',
			data=EMPTY_REMINDER
		)

	def test_save_a_POST_request_to_existing_reminder(self):
		utc = tzobj.UTC()
		date = datetime.datetime(2015, 06, 23, tzinfo=utc)
		saved_reminder = Reminder.objects.create(
			title='Buy milk',
			alarm=date,
			snooze=5,
			repeat=10,
			user=self.user
		)
		self.assertEqual(Reminder.objects.count(), 1)

		response = self.client.post(
			'/reminders/edit_reminder/%d' % (saved_reminder.pk,),
			data=REMINDER_TWO,
		)
		self.assertRedirects(response, '/reminders/home/')
		
		edited_reminder = Reminder.objects.get(pk=saved_reminder.pk)
		self.assertEqual(edited_reminder, saved_reminder)
		self.assertEqual(edited_reminder.title, 'Buy beer')
		self.assertEqual(edited_reminder.alarm.date(), datetime.datetime(2015, 6, 23, tzinfo=utc).date())
		self.assertEqual(edited_reminder.snooze, 15.0)
		self.assertEqual(edited_reminder.repeat, 36.0)
		self.assertEqual(edited_reminder.user, self.user)
		self.assertEqual(Reminder.objects.count(), 1)

	def test_validation_errors_are_shown_on_home_page(self):
		response = self.client.post('/reminders/home/', data=EMPTY_REMINDER)
		self.assertContains(response, EMPTY_REMINDER_TITLE_ERROR)

	def test_invalid_input_renders_list_template(self):
		response = self.client.post('/reminders/home/', data=EMPTY_REMINDER)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'reminders/reminder_list.html')

	def test_for_invalid_nothing_saved_to_db(self):
		self.post_invalid_input()
		self.assertEqual(Reminder.objects.count(), 0)

	def test_for_invalid_renders_reminder_list_template(self):
		response = self.post_invalid_input()
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'reminders/reminder_list.html')

	def test_for_invalid_input_passes_form_to_template(self):
		response = self.client.post('/reminders/home/', data=EMPTY_REMINDER)
		self.assertIsInstance(response.context['form'], ReminderForm)

	def test_for_invalid_shows_error_on_page(self):
		response = self.post_invalid_input()	
		self.assertContains(response, EMPTY_REMINDER_TITLE_ERROR)

class LoginRequiredTest(TestCase):
	# We can test GET or POST requests to test this since we just want to see if the 
	# view redirects when requested by any method
	def test_reminder_home_redirect_when_not_logged_in(self):
		response = self.client.get(reverse('reminder_home'))
		self.assertEqual(response.status_code, 302)

	def test_reminder_home_redirects_login_view_when_not_logged_in(self):
		response = self.client.get(reverse('reminder_home'))
		self.assertRegexpMatches(response['Location'], '/accounts/login/.+')

	def test_edit_reminder_redirects_when_not_logged_in(self):
		user = CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		utc = tzobj.UTC()
		date = datetime.datetime(2015, 06, 23, tzinfo=utc)
		reminder = Reminder.objects.create(
			title='Buy milk',
			alarm=date,
			snooze=5,
			repeat=10,
			user=user
		)
		response = self.client.get(reverse('edit_reminder', kwargs={'pk':reminder.pk}))
		self.assertEqual(response.status_code, 302)

	def test_edit_reminder_redirects_login_view_when_not_logged_in(self):
		user = CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		utc = tzobj.UTC()
		date = datetime.datetime(2015, 06, 23, tzinfo=utc)
		reminder = Reminder.objects.create(
			title='Buy milk',
			alarm=date,
			snooze=5,
			repeat=10,
			user=user
		)
		response = self.client.get(reverse('edit_reminder', kwargs={'pk':reminder.pk}))
		self.assertRegexpMatches(response['Location'], '/accounts/login/.+')