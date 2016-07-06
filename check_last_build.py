import requests
import smtplib
import os

from email.mime.text import MIMEText
from config import get_value_of

PRIVATE_TOKEN = os.environ.get('PRIVATE_TOKEN')
TRIGGER_MAYDAY_ON_FAILURES = os.environ.get('TRIGGER_MAYDAY_ON_FAILURES') or 2
gl_url = "https://gitlab.ops.mist.io/api/v3/projects/2/builds"
headers = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

gmail_pwd = get_value_of('PASSWORD', '')
FROM = get_value_of('EMAIL', '')
TO = 'mayday@mistio.pagerduty.com'
SUBJECT = 'Mayday build failed twice'

TEXT = ''


request = requests.get(gl_url, headers=headers)
data = request.json()

failures = 0
#Checking twice the logs as we have two stages
for i in range(TRIGGER_MAYDAY_ON_FAILURES * 2):
    if data[i]['name'] == 'run_mayday_test' and data[i]['status'] == 'failed':
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
