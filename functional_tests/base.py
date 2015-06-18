from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdrive

class FunctionalTest(StaticLiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox() #we start the browser here
		self.browser.implicitly_wait(3) #this makes sure we wait after the browser has been started and ensures the page has loaded

	#Similarly, tearDown is inherited from TestCase and overriden with our own functionality here
	def tearDown(self):
		self.browser.quit()