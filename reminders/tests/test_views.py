import datetime

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils import timezone

from reminders.views import home_page
from reminders.models import Reminder
from functional_tests.base import REMINDER_ONE
import reminders.timezone_object as tzobj

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)

		expected_html = render_to_string('reminders/home.html')

		self.assertEqual(response.content, expected_html)

	def test_home_page_only_saves_reminders_when_necessary(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Reminder.objects.count(), 0)

class NewReminderListTest( TestCase):

	def test_home_page_redirects_after_POST(self):
		response = self.client.post(
			'/reminders/new',
			data=REMINDER_ONE
		)
		self.assertRedirects(response, '/reminders/the-only-reminder-list-in-the-world/')
		#self.assertEqual(response.status_code, 302)
		#self.assertEqual(response['location'], '/reminders/the-only-reminder-list-in-the-world/')

	def test_home_page_can_save_a_POST_request(self):
		self.client.post(
			'/reminders/new',
			data=REMINDER_ONE
		)
		self.assertEqual(Reminder.objects.count(), 1)
		new_item = Reminder.objects.first()
		self.assertEqual(new_item.title, 'Buy milk')

class ReminderViewTest(TestCase):

	def test_displays_multiple_reminders(self):
		utc = tzobj.UTC()
		date = datetime.datetime(2015, 06, 23, tzinfo=utc)
		Reminder.objects.create(
			title='Buy milk',
			alarm=date,
			snooze=5,
			repeat=10
		)
		Reminder.objects.create(
			title='Buy beer',
			alarm=date,
			snooze=5,
			repeat=10
		)

		response = self.client.get('/reminders/the-only-reminder-list-in-the-world/')

		self.assertContains(response, 'Buy milk')
		self.assertContains(response, 'Buy beer')

	def test_uses_reminder_list_template(self):
		response = self.client.get('/reminders/the-only-reminder-list-in-the-world/')
		self.assertTemplateUsed(response, 'reminders/reminder_list.html')