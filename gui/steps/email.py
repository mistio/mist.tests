import shutil

import logging
import imaplib

from time import sleep
from time import time

from behaving.mail.steps import *

log = logging.getLogger(__name__)


@step(u'I follow the link contained in the email sent at "{address}" with '
      u'subject "{subject}"')
def follow_link_inside_email(context, address, subject):
    def get_subject_from_mail(mail):
        text, encoding = decode_header(mail.get('Subject'))[0]
        return text.decode(encoding) if encoding else text

    def filter_contents(mail):
        mail = email.message_from_string(mail)
        return subject == get_subject_from_mail(mail)

    mail = context.mail.user_messages(address, filter_contents)
    assert len(mail) == 1, "User has either more than one or no confirmation " \
                           "email"
    message = email.message_from_string(mail[0]).get_payload()
    str_end = message.find('\n\nIn the meantime')
    if str_end == -1:
        str_end = message.find('\n\nThis request originated')
    if str_end == -1:
        str_end = message.find('\n\nOnce you are done with the confirmation')
    if str_end == -1:
        str_end = message.find('\n\nOnce you are done with the registration')
    link_to_follow = message[(message.find('link:\n\n') + len('link:\n\n')):str_end]
    context.browser.get(link_to_follow)
    sleep(2)


@step(u'I save the confirmation link')
def save_link_inside_email(context):
    def get_subject_from_mail(mail):
        text, encoding = decode_header(mail.get('Subject'))[0]
        return text.decode(encoding) if encoding else text

    def filter_contents(mail):
        mail = email.message_from_string(mail)
        return '[mist.io] Confirm your registration' == get_subject_from_mail(mail)

    mail = context.mail.user_messages(context.mist_config['EMAIL'], filter_contents)
    assert len(mail) == 1, "User has either more than one or no confirmation " \
                           "email"
    message = email.message_from_string(mail[0]).get_payload()
    str_end = message.find('\n\nIn the meantime')
    if str_end == -1:
        str_end = message.find('\n\nThis request originated')
    link_to_follow = message[(message.find('link:\n\n') + len('link:\n\n')):str_end]
    context.mist_config['CONFIRMATION_LINK'] = link_to_follow


@step('I make sure that this link is the same as before at email address'
      ' "{email_address}"')
def check_links_in_confirmation_emails(context, email_address):
    def get_subject_from_mail(mail):
        text, encoding = decode_header(mail.get('Subject'))[0]
        return text.decode(encoding) if encoding else text

    def filter_contents(mail):
        mail = email.message_from_string(mail)
        return '[mist.io] Confirm your registration' == get_subject_from_mail(mail)

    mail = context.mail.user_messages(context.mist_config['EMAIL'], filter_contents)
    assert len(mail) == 1, "User has either more than one or no confirmation " \
                           "email"
    message = email.message_from_string(mail[0]).get_payload()
    str_end = message.find('\n\nIn the meantime')
    if str_end == -1:
        str_end = message.find('\n\nThis request originated')
    link_to_follow = message[(message.find('link:\n\n') + len('link:\n\n')):str_end]
    assert link_to_follow == context.mist_config['CONFIRMATION_LINK'], \
        "Confirmation links %s and %s do not " \
        "match" % (link_to_follow, context.mist_config['CONFIRMATION_LINK'])


@step('I delete the confirmation email')
def delete_confirmation_email(context):
    mailpath = context.mail.path + context.mist_config['EMAIL']
    shutil.rmtree(mailpath)


@step(u'I should receive an email at the address "{email_address}" with subject'
      u' "{subject}"')
def check_if_email_arrived(context, email_address, subject):
    if context.mist_config.get(email_address):
        email_address = context.mist_config.get(email_address)
    if context.mist_config.get(subject):
        subject = context.mist_config.get(subject)
    context.execute_steps(u'Then I should receive an email at "%s" with subject'
                          u' "%s"'% (email_address, subject))


@step(u'I follow the link contained in the email sent at the address '
      u'"{email_address}" with subject "{subject}"')
def follow_link_in_email(context, email_address, subject):
    if context.mist_config.get(email_address):
        email_address = context.mist_config.get(email_address)
    if context.mist_config.get(subject):
        subject = context.mist_config.get(subject)
    context.execute_steps(u'Then I follow the link contained in the email sent'
                          u' at "%s" with subject "%s"'
                          % (email_address, subject))


@step(u'I should receive an email at the address "{email_address}" with subject'
      u' "{subject}" within {seconds} seconds')
def check_if_email_arrived_with_delay(context, email_address, subject, seconds):
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            check_if_email_arrived(context, email_address, subject)
            return True
        except:
            pass
        sleep(1)
    assert False, "Email has not arrived after %s seconds"\
              % seconds


@step(u'I save the confirmation link and delete the email')
def dispose_registration_email(context):
    context.execute_steps(u"""
            Then I save the confirmation link
            And I delete the confirmation email
    """)


@step(u'I delete old emails')
def delete_emails(context):
    box = login_email(context)
    box.select("INBOX")
    typ, data = box.search(None, 'ALL')
    if not data[0].split():
        return

    for num in data[0].split():
        box.store(num, '+FLAGS', '\\Deleted')
    box.expunge()
    logout_email(box)


@step(u'I should receive an email within {seconds} seconds')
def receive_mail(context, seconds):
    end_time = time() + int(seconds)
    error = ""

    while time() < end_time:
        log.info("Looking if email has arrived\n\n")
        try:
            box = login_email(context)
            if not box:
                error = "login failed"
                continue
            inbox = box.select("INBOX")
        except Exception as e:
            log.info("An exception occurred: %s\n\n" % str(e))
            continue

        log.info("Searching in inbox for email\n\n")
        typ, data = box.search(None, 'ALL')

        if data[0].split():
            return
        else:
            logout_email(box)
            log.info("Email has not arrived yet. Sleeping for 15 seconds\n\n")
            sleep(15)

    assert False, u'Did not receive an email within %s seconds. %s' % (seconds,
                                                                       error)


def login_email(context):
    box = imaplib.IMAP4_SSL("imap.gmail.com")
    login = box.login(context.mist_config['GOOGLE_TEST_EMAIL'],
                      context.mist_config['GOOGLE_TEST_PASSWORD'])
    if 'OK' in login:
        return box
    else:
        return False


def logout_email(box):
    box.close()
    box.logout()

