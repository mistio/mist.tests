import requests
import smtplib
import os

import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from tests.config import get_value_of

PRIVATE_TOKEN = os.environ.get('PRIVATE_TOKEN')

if os.environ.get('CI_BUILD_ID') is not None:
    CI_BUILD_ID = int(os.environ.get('CI_BUILD_ID')) -1
else:
    CI_BUILD_ID = ''

if os.environ.get('MIST_TEST_LOG_DIR') is not None:
    MIST_TEST_LOG_DIR = os.environ.get('MIST_TEST_LOG_DIR')
else:
    MIST_TEST_LOG_DIR = 'mayday/' + str(CI_BUILD_ID)

if os.environ.get('TRIGGER_MAYDAY_ON_FAILURES') is not None:
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
# log.info("Data returned is: %s" % data)

# this start as one because the first failed build is the current one
failures = 1
test_results = []

# Checking twice the logs as we have two stages
for i, data_dict in enumerate(data):
    if i == 0:
        continue
    log.info("looking at result %s" % data_dict)
    if data[i]['status'] == 'failed':
        failures += 1
        log.info("Found another failure. Failures so far %s" % failures)
    else:
        break


if failures >= TRIGGER_MAYDAY_ON_FAILURES:

    print str(TRIGGER_MAYDAY_ON_FAILURES) + ' last tests failed, raising mayday'

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, TO, SUBJECT, TEXT)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(FROM, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.quit()

else:
    print 'One of the ' + str(TRIGGER_MAYDAY_ON_FAILURES) + ' last tests succeeded, not raising mayday'
