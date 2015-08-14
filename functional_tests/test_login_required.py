import datetime

from .base import FunctionalTest, REMINDER_ONE
import reminders.timezone_object as tzobj
from reminders.models import Reminder
from accounts.models import CustomUser

class LoginRequiredTest(FunctionalTest):

	def setUp(self):
		utc = tzobj.UTC()
		date = datetime.datetime(2015, 06, 22, tzinfo=utc)
		self.user = CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		self.reminder = Reminder.objects.create(
			title='Buy milk',
			alarm=date,
			snooze=10.0,
			repeat=24.0,
			user=self.user,
		)
		super(LoginRequiredTest, self).setUp()

	def tearDown(self):
		super(LoginRequiredTest, self).tearDown()
		self.user.delete()

	def test_reminder_urls_redirect_if_not_logged_in(self):
		# Del tries to reach the reminder app without logging in by going directly
		# to the reminders home url but Del is redirected because he hasn't logged
		# in.

		self.browser.get('%s%s' % (self.server_url, '/reminders/home/',))
		self.assertRegexpMatches(self.browser.current_url, '/accounts/login.+')

		# Befuddled, Del tries to edit his reminder but is still redirected
		self.browser.get('%s%s%s%s' % 
			(self.server_url, '/reminders/', 'edit_reminder/', self.reminder.pk,)
		)
		self.assertRegexpMatches(self.browser.current_url, '/accounts/login.+')

		# Del finally logs in
		self.login_test_user()

		# Del is taken to the reminders home page where he can see his only reminder
		self.assertRegexpMatches(self.browser.current_url, '/reminders/home/')

		reminders = self.get_all_reminder_values()

		for value in REMINDER_ONE.itervalues():
			self.assertIn(value, reminders)