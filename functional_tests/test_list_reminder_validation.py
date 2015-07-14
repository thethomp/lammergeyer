from .base import FunctionalTest
from unittest import skip

class ReminderValidationTest(FunctionalTest):

	@skip('skipped')
	def test_cannot_add_reminders_with_empty_fields(self):
		# Della Bahee lands on the user page and expands the reminder creation panel. 
		# Like a dum dum, he neglects each input field and simply hits Create reminder! button.
		self.browser.get(live_server_url)
		self.browser.find_element_by_id('id_new_reminder_btn').click()

		# Consequently, he is redirected to the reminder-list page and sees error messages appear 
		# above each field telling him they are required for reminder creation.
		self.assertRegExpMatches(self.browser.get(current_url), '/reminders/+\d')

		# Del properly fills out the reminder fields and a new reminder is created.
		self.browser.create_new_reminder(REMINDER_ONE)

		# Del does not learn from his mistakes and attempts to create an empty reminder again!

		# An error message is shown for each field.

		# Del now only fills out the reminder title field, hits create but only to see error messages 
		# for the other three fields

		# Del tries fills in each field, one by one, getting a corresponding error message each time.

		# Del is learning, he realizes at least one field must be filled in. Thus he tries each combination 
		# of dual fields

		# Del is convinced at least two fields must be used. So he tries all triplet combinations.

		# Del now tries all triplet combinations.

		# Del has decided that every field must have an input. He creates a proper reminder.