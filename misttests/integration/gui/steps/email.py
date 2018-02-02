import shutil
import logging
import imaplib
import email
import re

from time import sleep
from time import time

from behaving.mail.steps import *

log = logging.getLogger(__name__)


@step('I follow the link inside the email')
def follow_link(context):
    link = context.link_inside_email
    if not link:
        assert False, "No link inside the email received"
    context.browser.get(link)
    sleep(2)


@step(u'I should receive an email at the address "{email_address}" with subject'
      u' "{subject}"')
def check_if_email_arrived(context, email_address, subject):
    if context.mist_config.get(email_address):
        email_address = context.mist_config.get(email_address)
    if context.mist_config.get(subject):
        subject = context.mist_config.get(subject)
    context.execute_steps(u'Then I should receive an email at "%s" with subject'
                          u' "%s"' % (email_address, subject))


@step(u'I should receive an email at the address "{email_address}" with subject'
      u' "{subject}" within {seconds} seconds')
def check_if_email_arrived_with_delay(context, email_address, subject, seconds):
    email = context.mist_config[email_address]
    timeout = time() + int(seconds)
    while time() < timeout:
        emails = email_find(context, email, subject)
        if len(emails) > 0:
            return True
        else:
            sleep(1)
    assert False, "Email has not arrived after %s seconds" % seconds


@step(u'I delete old emails')
def delete_emails(context):
    box = login_email(context)
    box.select('INBOX')
    typ, data = box.search(None, 'ALL')
    if data:
        for num in data[0].split():
            box.store(num, '+FLAGS', '\\Deleted')
    box.expunge()
    box.close()
    box.logout()
    return True


def email_find(context, address, subject):
    box = login_email(context)
    box.select("INBOX")
    result, data = box.search(None, '(TO ' + address + ')')
    ids = data[0].split()
    fetched_mails = []
    for i in ids:
        result, msgdata = box.fetch(i, "(RFC822)")
        raw = msgdata[0][1]
        email_message = email.message_from_string(raw)
        log.info("Checking email with subject: %s " % email_message.get('Subject'))
        if subject in email_message.get('Subject') and address in email_message.get('To'):
            fetched_mails.append(raw)
            # delete the email
            box.store(i, '+FLAGS', '\\Deleted')
            box.expunge()
            break

    if not fetched_mails:
        context.link_inside_email = ''
        box.logout()
        return fetched_mails

    mail = fetched_mails[0]

    mist_url = context.mist_config['MIST_URL']
    link_regex = '(' + mist_url + '+[\w\d:#@%/;$()~_?\+-=\\.&][a-zA-z0-9][^<>#]*)\n\n'
    urls = re.findall(link_regex, mail)
    link = urls[0].split('\n\n')[0]
    if urls:
        context.link_inside_email = link

    box.logout()
    return fetched_mails


def get_imap_host_kubernetes(context):
    # mailmock pod is resolvable: mailmock.{namespace}
    if context.mist_config['CORE_TEST']:
        prefix = 'mailmock.' + 'core-test-'
        return prefix + context.mist_config['MIST_URL'].replace('http://', '').replace('.core.test.ops.mist.io', '')
    else:
        prefix = 'mailmock.' + 'io-test-'
        return prefix + context.mist_config['MIST_URL'].replace('http://', '').replace('.io.test.ops.mist.io', '')


def login_email(context):
    if context.mist_config['LOCAL']:
        imap_host = context.mist_config['IMAP_HOST']
    else:
        imap_host = get_imap_host_kubernetes(context)

    imap_port = context.mist_config['IMAP_PORT']

    if context.mist_config['IMAP_USE_SSL']:
        box = imaplib.IMAP4_SSL(imap_host, imap_port)
    else:
        box = imaplib.IMAP4(imap_host, imap_port)

    login = box.login('test','test')

    if 'OK' in login:
        return box
    else:
        assert False, "Logging in to localmail failed!"


def logout_email(box):
    box.close()
    box.logout()