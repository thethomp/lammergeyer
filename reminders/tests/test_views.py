import datetime

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils import timezone

from reminders.views import home_page
from reminders.models import Reminder, List
from base import REMINDER_ONE, REMINDER_TWO, EMPTY_REMINDER
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

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/reminders/new',
			data=REMINDER_ONE
		)
		new_list  = List.objects.first()
		self.assertRedirects(response, '/reminders/%d/' % (new_list.id,))

	def test_can_save_a_POST_request(self):
		self.client.post(
			'/reminders/new',
			data=REMINDER_ONE
		)
		self.assertEqual(Reminder.objects.count(), 1)
		new_item = Reminder.objects.first()
		self.assertEqual(new_item.title, 'Buy milk')

class ReminderViewTest(TestCase):

	def test_can_save_a_POST_request_to_an_existing_list(self):
		correct_list = List.objects.create()
		other_list = List.objects.create()

		self.client.post(
			'/reminders/%d/' % (correct_list.id,),
			data=REMINDER_ONE
		)

		self.assertEqual(Reminder.objects.count(), 1)
		new_item = Reminder.objects.first()
		self.assertEqual(new_item.title, 'Buy milk')
		self.assertEqual(new_item.list, correct_list)

	def test_POST_redirects_to_list_view(self):
		correct_list = List.objects.create()
		other_list = List.objects.create()

		response = self.client.post(
			'/reminders/%d/' % (correct_list.id,),
			data=REMINDER_ONE
		)

		self.assertRedirects(response, '/reminders/%d/' % (correct_list.id,))

	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get('/reminders/%d/' % (correct_list.id,))
		self.assertEqual(response.context['list'], correct_list)

	def test_save_a_POST_request_to_existing_reminder(self):
		list_ = List.objects.create()
		utc = tzobj.UTC()
		date = datetime.datetime(2015, 06, 23, tzinfo=utc)
		saved_reminder = Reminder.objects.create(
			title='Buy milk',
			alarm=date,
			snooze=5,
			repeat=10,
			list=list_
		)
		self.assertEqual(Reminder.objects.count(), 1)

		edited_reminder = {}
		for key, value in REMINDER_TWO.iteritems():
			edited_reminder['%s_%d' % (key, saved_reminder.pk,)] = value

		response = self.client.post(
			'/reminders/%d/edit_reminder/%d' % (list_.id, saved_reminder.pk,),
			data=edited_reminder,
		)
		self.assertRedirects(response, '/reminders/%d/' % (list_.id,))

		edited_reminder = Reminder.objects.get(pk=saved_reminder.pk)
		self.assertEqual(edited_reminder, saved_reminder)
		self.assertEqual(edited_reminder.title, 'Buy beer')
		self.assertEqual(edited_reminder.alarm, datetime.datetime(2015, 6, 23, tzinfo=utc))
		self.assertEqual(edited_reminder.snooze, 15.0)
		self.assertEqual(edited_reminder.repeat, 36.0)
		self.assertEqual(Reminder.objects.count(), 1)

	def test_validation_errors_are_sent_back_to_home_page_template(self):
		response = self.client.post('/reminders/new', data=EMPTY_REMINDER)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'reminders/home.html')
		expected_error = "Reminders need titles!"
		self.assertContains(response, expected_error)

	def test_empty_reminders_are_not_saved(self):
		response = self.client.post('/reminders/new', data=EMPTY_REMINDER)
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Reminder.objects.count(), 0)

	def test_displays_only_reminders_for_that_list(self):
		utc = tzobj.UTC()
		date = datetime.datetime(2015, 06, 23, tzinfo=utc)
		correct_list = List.objects.create()
		Reminder.objects.create(
			title='Buy milk',
			alarm=date,
			snooze=5,
			repeat=10,
			list=correct_list
		)
		Reminder.objects.create(
			title='Buy beer',
			alarm=date,
			snooze=5,
			repeat=10,
			list=correct_list
		)
		other_list = List.objects.create()
		Reminder.objects.create(
			title='Buy milkshakes',
			alarm=date,
			snooze=5,
			repeat=10,
			list=other_list
		)
		Reminder.objects.create(
			title='Buy beerfloats',
			alarm=date,
			snooze=5,
			repeat=10,
			list=other_list
		)
		response = self.client.get('/reminders/%d/' % (correct_list.id,))

		self.assertContains(response, 'Buy milk')
		self.assertContains(response, 'Buy beer')
		self.assertNotContains(response, 'Buy milkshakes')
		self.assertNotContains(response, 'Buy beerfloats')

	def test_uses_reminder_list_template(self):
		list_  = List.objects.create()
		response = self.client.get('/reminders/%d/' % (list_.id,))
		self.assertTemplateUsed(response, 'reminders/reminder_list.html')