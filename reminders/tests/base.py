from django.test import TestCase, TransactionTestCase

from accounts.models import CustomUser

REMINDER_ONE = {
	'title' : 'Buy milk', 
	'alarm': '2015-06-22', 
	'snooze': '10.0', 
	'repeat': '24.0'
}
REMINDER_TWO = {
	'title' : 'Buy beer', 
	'alarm': '2015-06-23', 
	'snooze': '15.0', 
	'repeat': '36.0'	
}
EMPTY_REMINDER = {
	'title' : '', 
	'alarm': '2015-06-22', 
	'snooze': '10.0', 
	'repeat': '24.0'
}

# For views testing
class UserTestCase(TransactionTestCase):
	def setUp(self):
		self.user = CustomUser.objects.create_user(email='jj@gmail.com', password='123')
		self.client.get('/accounts/login/')
		self.client.login(email=self.user.email, password='123')

	def tearDown(self):
		self.user.delete()
