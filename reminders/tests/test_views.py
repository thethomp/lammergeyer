import datetime

from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils import timezone

from reminders.views import home_page, reminder_home
from reminders.models import Reminder, List
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

		expected_html = render_to_string('reminders/reminder_home.html', {'form': ReminderForm()})

		self.assertMultiLineEqual(response.content.decode(), expected_html)

	def test_reminder_home_renders_reminder_home_template(self):
		response = self.client.get('/reminders/home/')
		self.assertTemplateUsed(response, 'reminders/reminder_home.html')

	def test_reminder_home_uses_item_form(self):
		response = self.client.get('/reminders/home/')
		self.assertIsInstance(response.context['form'], ReminderForm)

	def test_reminder_home_only_saves_reminders_when_necessary(self):
		request = HttpRequest()
		request.user = self.user
		reminder_home(request)
		self.assertEqual(Reminder.objects.count(), 0)

	# The tests below might make more sense being in a different class
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

class ReminderListViewTest(UserTestCase):

	def post_invalid_input(self):
		list_ = List.objects.create()
		return self.client.post(
			'/reminders/%d/' % (list_.id,),
			data=EMPTY_REMINDER
		)

	def test_uses_reminder_list_template(self):
		list_  = List.objects.create()
		response = self.client.get('/reminders/%d/' % (list_.id,))
		self.assertTemplateUsed(response, 'reminders/reminder_list.html')

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

		response = self.client.post(
			'/reminders/%d/edit_reminder/%d' % (list_.id, saved_reminder.pk,),
			data=REMINDER_TWO,
		)
		self.assertRedirects(response, '/reminders/%d/' % (list_.id,))
		
		edited_reminder = Reminder.objects.get(pk=saved_reminder.pk)
		self.assertEqual(edited_reminder, saved_reminder)
		self.assertEqual(edited_reminder.title, 'Buy beer')
		self.assertEqual(edited_reminder.alarm.date(), datetime.datetime(2015, 6, 23, tzinfo=utc).date())
		self.assertEqual(edited_reminder.snooze, 15.0)
		self.assertEqual(edited_reminder.repeat, 36.0)
		self.assertEqual(Reminder.objects.count(), 1)

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

	def test_validation_errors_are_shown_on_home_page(self):
		response = self.client.post('/reminders/new', data=EMPTY_REMINDER)
		self.assertContains(response, EMPTY_REMINDER_TITLE_ERROR)

	def test_invalid_input_renders_home_template(self):
		response = self.client.post('/reminders/new', data=EMPTY_REMINDER)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'reminders/home.html')

	def test_for_invalid_nothing_saved_to_db(self):
		self.post_invalid_input()
		self.assertEqual(Reminder.objects.count(), 0)

	def test_for_invalid_renders_reminder_list_template(self):
		response = self.post_invalid_input()
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'reminders/reminder_list.html')

	def test_for_invalid_input_passes_form_to_template(self):
		response = self.client.post('/reminders/new', data=EMPTY_REMINDER)
		self.assertIsInstance(response.context['form'], ReminderForm)

	def test_for_invalid_shows_error_on_page(self):
		response = self.post_invalid_input()	
		self.assertContains(response, EMPTY_REMINDER_TITLE_ERROR)

	def test_displays_reminder_form(self):
		list_ = List.objects.create()
		response = self.client.get('/reminders/%d/' % (list_.id,))
		self.client.login(email=self.user.email, password='123')
		response = self.client.get('/reminders/%d/' % (list_.id,))

		self.assertIsInstance(response.context['form'], ReminderForm)
		self.assertContains(response, 'name="title"')

class LoginRequiredTest(TestCase):
	# We can test GET or POST requests to test this since we just want to see if the 
	# view redirects when requested by any method
	def test_reminder_home_redirect_when_not_logged_in(self):
		response = self.client.get(reverse('reminder_home'))
		self.assertEqual(response.status_code, 302)

	def test_reminder_home_redirects_login_view_when_not_logged_in(self):
		response = self.client.get(reverse('reminder_home'))
		self.assertRegexpMatches(response['Location'], '/accounts/login/.+')

	def test_view_reminder_redirects_when_not_logged_in(self):
		list_ = List.objects.create()
		response = self.client.get(reverse('view_reminders', args=[list_.id]))
		self.assertEqual(response.status_code, 302)

	def test_view_reminder_redirects_login_view_when_not_logged_in(self):
		response = self.client.get(reverse('view_reminders', args=[1]))
		self.assertRegexpMatches(response['Location'], '/accounts/login/.+')

	def test_edit_reminder_redirects_when_not_logged_in(self):
		utc = tzobj.UTC()
		date = datetime.datetime(2015, 06, 23, tzinfo=utc)
		list_ = List.objects.create()
		reminder = Reminder.objects.create(
			title='Buy milk',
			alarm=date,
			snooze=5,
			repeat=10,
			list=list_
		)
		response = self.client.get(reverse('edit_reminder', kwargs={'list_id':list_.id, 'pk':reminder.pk}))
		self.assertEqual(response.status_code, 302)

	def test_edit_reminder_redirects_login_view_when_not_logged_in(self):
		utc = tzobj.UTC()
		date = datetime.datetime(2015, 06, 23, tzinfo=utc)
		list_ = List.objects.create()
		reminder = Reminder.objects.create(
			title='Buy milk',
			alarm=date,
			snooze=5,
			repeat=10,
			list=list_
		)
		response = self.client.get(reverse('edit_reminder', kwargs={'list_id':list_.id, 'pk':reminder.pk}))
		self.assertRegexpMatches(response['Location'], '/accounts/login/.+')

	def test_new_reminder_list_view_redirects_when_not_logged_in(self):
		response = self.client.get(reverse('new_reminder_list'))
		self.assertEqual(response.status_code, 302)

	def test_new_reminder_list_view_redirects_login_view_when_not_logged_in(self):
		response = self.client.get(reverse('new_reminder_list'))
		self.assertRegexpMatches(response['Location'], '/accounts/login/.+')