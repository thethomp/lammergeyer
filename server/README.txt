Pre-requisites:
1. Set up gmail account and make sure that EMAIL* settings are correct
in lammergeyer/settings.py

To Run test_send_reminders.py:
Use the Django shell.
1. Go to base project directory
2. Execute script like so:
	python manage.py shell < server/test_send_reminders.py

To set up cron to send out reminders every 10 seconds:
1. Copy/paste the contents of cron_job.sh to the crontab of the server
2. Do this by using the 'crontab -e' command
3. Ensure all paths are correct before enabling 
