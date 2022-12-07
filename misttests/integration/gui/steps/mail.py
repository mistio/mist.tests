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


@step('I should receive an email at the address "{email_address}" with subject'
      ' "{subject}"')
def check_if_email_arrived(context, email_address, subject):
    if context.mist_config.get(email_address):
        email_address = context.mist_config.get(email_address)
    if context.mist_config.get(subject):
        subject = context.mist_config.get(subject)
    context.execute_steps('Then I should receive an email at "%s" with subject'
                          ' "%s"' % (email_address, subject))


@step('I should receive an email at the address "{email_address}" with subject'
      ' "{subject}" within {seconds} seconds')
def check_if_email_arrived_with_delay(context, email_address, subject, seconds):
    email = context.mist_config[email_address]

    # get machine's name
    if 'random' in subject:
        for i in subject.split(' '):
            if 'random' in i:
                machine = i.replace(':', '').replace('`', '')

        subject = subject.replace(machine, context.mist_config[machine])

    timeout = time() + int(seconds)
    while time() < timeout:
        emails = email_find(context, email, subject)
        if len(emails) > 0:
            return True
        else:
            sleep(1)
    assert False, "Email has not arrived after %s seconds" % seconds

@step('I should receive an email at the address "{email_address}" which contains subject terms: "{subject_terms}"'
      ' within {seconds} seconds')
def check_if_email_arrived_with_delay(context, email_address, subject_terms, seconds):
    email = context.mist_config[email_address]
    subject_terms = subject_terms.split(",")
    # get machine's name
    for i, subject_term in enumerate(subject_terms):
        if 'random' in subject_term:
            for word in subject_term.split(' '):
                if 'random' in word:
                    machine = word.replace(':', '').replace('`', '')

            subject_terms[i] = subject_term.replace(
                machine, context.mist_config[machine])

    timeout = time() + int(seconds)
    while time() < timeout:
        emails = email_find(context, email, subject_terms)
        if len(emails) > 0:
            return True
        else:
            sleep(1)
    assert False, "Email has not arrived after %s seconds" % seconds


@step('I delete old emails')
def delete_emails(context):
    box = login_email(context)
    box.select('INBOX')
    typ, data = box.search(None, 'ALL')
    if data and data[0]:
        for num in data[0].split():
            box.store(num, '+FLAGS', '\\Deleted')
    box.expunge()
    box.close()
    box.logout()
    return True


def email_find(context, address, subject_terms):
    if isinstance(subject_terms, str):
        subject_terms = [subject_terms]
    box = login_email(context)
    box.select("INBOX")
    result, data = box.search(None, '(TO ' + address + ')')
    fetched_mails = []

    if data and data[0]:
        ids = data[0].split()
        for i in ids:
            result, msgdata = box.fetch(i, "(RFC822)")
            raw = msgdata[0][1]
            email_message = email.message_from_bytes(raw)
            log.info("Checking email with subject: %s " %
                     email_message.get('Subject'))
            if address in email_message.get('To'):
                for subject_term in subject_terms:
                    if subject_term.lower() not in email_message.get('Subject').lower():
                        break
                else:
                    fetched_mails.append(raw.decode('utf-8'))
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
    link_regex = '(' + mist_url + \
        '+[\w\d:#@%/;$()~_?\+-=\\.&][a-zA-z0-9][^<>#]*)\n\n'
    urls = re.findall(link_regex, mail)

    if not urls:
        mist_url = context.mist_config['MIST_URL'].replace(
            'http://', 'https://')
        link_regex = '(' + mist_url + \
            '+[\w\d:#@%/;$()~_?\+-=\\.&][a-zA-z0-9][^<>#]*)\n\n'
        urls = re.findall(link_regex, mail)

    link = urls[0].split('\n\n')[0]
    context.link_inside_email = link

    box.logout()
    return fetched_mails


def login_email(context):
    imap_host = context.mist_config['IMAP_HOST']
    imap_port = context.mist_config['IMAP_PORT']

    if context.mist_config['IMAP_USE_SSL']:
        box = imaplib.IMAP4_SSL(imap_host, imap_port)
    else:
        box = imaplib.IMAP4(imap_host, imap_port)

    login = box.login('test', 'test')

    if 'OK' in login:
        return box
    else:
        assert False, "Logging in to localmail failed!"


def logout_email(box):
    box.close()
    box.logout()
