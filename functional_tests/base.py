from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
REMINDER_ONE = {
	'reminder_title' : 'Buy milk', 
	'reminder_alarm': '06/23/2015', 
	'reminder_snooze': '10', 
	'reminder_repeat': 'T'
}
REMINDER_TWO = {
	'reminder_title' : 'Buy beer', 
	'reminder_alarm': '06/23/2015', 
	'reminder_snooze': '15', 
	'reminder_repeat': 'TWF'	
}

class FunctionalTest(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		super(FunctionalTest, cls).setUpClass()
		cls.server_url = cls.live_server_url

	@classmethod
	def teadDownClass(cls):
		super(FunctionalTest, cls).tearDownClass()

	def setUp(self):
		self.browser = webdriver.Firefox() #we start the browser here
		self.browser.implicitly_wait(3) #this makes sure we wait after the browser has been started and ensures the page has loaded

	#Similarly, tearDown is inherited from TestCase and overriden with our own functionality here
	def tearDown(self):
		self.browser.quit()