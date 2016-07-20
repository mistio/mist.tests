import requests
import smtplib
import os

import logging

from datetime import date, timedelta, datetime

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

#Add a private token here when deployed
PRIVATE_TOKEN = ''

#Google credentials to send the email
GOOGLE_TEST_PASSWORD = ''
GOOGLE_TEST_EMAIL = 'tester.mist.io@gmail.com'

#Change this to alter after how many consecutive failures the mayday is raised
TRIGGER_MAYDAY_ON_FAILURES = 2

TO = 'mayday@mistio.pagerduty.com'
SUBJECT = 'Production mayday alert'

gl_url = "https://gitlab.ops.mist.io/api/v3/projects/2/builds"
headers = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

TEXT = 'Build has failed, check the logs at https://gitlab.ops.mist.io/mistio/mist.test.logs/tree/master/mayday'

request = requests.get(gl_url, headers=headers)
data = request.json()
# log.info("Data returned is: %s" % data)

failures = 0
successes = 0

def raise_mayday():
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (GOOGLE_TEST_EMAIL, TO, SUBJECT, TEXT)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(GOOGLE_TEST_EMAIL, GOOGLE_TEST_PASSWORD)
    server.sendmail(GOOGLE_TEST_EMAIL, TO, message)
    server.quit()

#Initialize the last succesful test date to 1 day ago
last_succesful_test = date.today() - timedelta(days=1)

#Check for the time of the last succesful test
for i in range(0,len(data) -1):
    if data[i]['status'] == 'success':
        last_succesful_test = datetime.strptime(str(data[i]['finished_at']), "%Y-%m-%dT%H:%M:%S.%fZ")
        break

#if the last succesfult tests was more than 30 minutes ago, raise mayday
if last_succesful_test < datetime.now() - timedelta(minutes=30):
    raise_mayday()

# Checking the logs for failures if we find success first, everything is ok
for i, data_dict in enumerate(data):
    log.info("looking at result %s" % data_dict)
    if data[i]['status'] == 'pending' or data[i]['status'] == 'canceled' or data[i]['status'] == 'running':
        pass
    elif data[i]['status'] == 'failed':
        failures += 1
        log.info("Found another failure. Failures so far %s" % failures)
        if failures >= TRIGGER_MAYDAY_ON_FAILURES:
            raise_mayday()
    elif data[i]['status'] == 'success':
        break
