from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from reminders.views import home_page
from functional_tests.base import REMINDER_ONE

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
		request.POST = REMINDER_ONE

		response = home_page(request)
		
		self.assertIn('Buy milk', response.content)
		expected_html = render_to_string(
			'reminders/home.html',
			REMINDER_ONE
		)

		self.assertEqual(expected_html, response.content.decode())