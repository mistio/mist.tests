import requests
import smtplib
import os

from email.mime.text import MIMEText
from config import get_value_of

PRIVATE_TOKEN = os.environ.get('PRIVATE_TOKEN')

if os.environ.get('CI_BUILD_ID') is not None:
    CI_BUILD_ID = int(os.environ.get('CI_BUILD_ID')) -1
else:
    CI_BUILD_ID = ''

if os.environ.get('MIST_TEST_LOG_DIR') is not None:
    MIST_TEST_LOG_DIR = os.environ.get('MIST_TEST_LOG_DIR')
else:
    MIST_TEST_LOG_DIR = 'mayday/' + str(CI_BUILD_ID)

if os.environ.get('TRIGGER_MAYDAY_ON_FAILURES')is not None:
    TRIGGER_MAYDAY_ON_FAILURES = int(os.environ.get('TRIGGER_MAYDAY_ON_FAILURES'))
else:
    TRIGGER_MAYDAY_ON_FAILURES = 2

gl_url = "https://gitlab.ops.mist.io/api/v3/projects/2/builds"
headers = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

gmail_pwd = get_value_of('GOOGLE_TEST_PASSWORD', '')
FROM = get_value_of('GOOGLE_TEST_EMAIL', '')
TO = 'mayday@mistio.pagerduty.com'
SUBJECT = 'Production mayday alert'

TEXT = 'Build has failed, check the logs at https://gitlab.ops.mist.io/mistio/mist.test.logs/tree/master/' + MIST_TEST_LOG_DIR

print 'https://gitlab.ops.mist.io/mistio/mist.test.logs/tree/master/' + MIST_TEST_LOG_DIR

request = requests.get(gl_url, headers=headers)
data = request.json()

failures = 0
test_results = []

#Checking twice the logs as we have two stages
for i in range(TRIGGER_MAYDAY_ON_FAILURES * 2):
    if data[i]['name'] == 'run_mayday_test':
        test_results.append(data[i]['status'])
#checking only the last mayday tests for consecutive failures
for j in range(TRIGGER_MAYDAY_ON_FAILURES):
    if test_results[j] == 'failed':
        failures +=1

if failures >= TRIGGER_MAYDAY_ON_FAILURES:

    print str(TRIGGER_MAYDAY_ON_FAILURES) + ' last tests failed, raising mayday'

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, TO, SUBJECT, TEXT)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(FROM,gmail_pwd)
#    server.sendmail(FROM, TO, message)
    server.quit()

else:
    print 'One of the ' + str(TRIGGER_MAYDAY_ON_FAILURES) + ' last tests succeeded, not raising mayday'
