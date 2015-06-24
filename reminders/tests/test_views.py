from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from reminders.views import home_page

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)

		expected_html = render_to_string('reminders/home.html')

		self.assertEqual(response.content, expected_html)

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['reminder_title'] = 'Buy milk'
		request.POST['reminder_alarm'] = '6/23/2015'
		request.POST['reminder_snooze'] = '10'
		request.POST['reminder_repeat'] = 'T'

		response = home_page(request)
		
		self.assertIn('Buy milk', response.content)
		self.assertIn('6/23/2015', response.content)
		self.assertIn('10', response.content)
		self.assertIn('T', response.content)