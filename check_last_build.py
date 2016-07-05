import requests
import smtplib

from email.mime.text import MIMEText


gl_url = "https://gitlab.ops.mist.io/api/v3/projects/7/builds"
TOKEN = '******'
headers = {"PRIVATE-TOKEN": TOKEN}

gmail_pwd = '******'
FROM = 'tester.mist.io@gmail.com'
TO = 'mayday@mistio.pagerduty.com'
SUBJECT = 'Mayday build failed twice'

TEXT = ''


request = requests.get(gl_url, headers=headers)
data = request.json()

if data[0]['status'] == 'failed' and data[1]['status'] == 'failed':

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, TO, SUBJECT, TEXT)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(FROM,gmail_pwd)

    server.sendmail(FROM, TO, message)
    server.quit()
