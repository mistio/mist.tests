import logging
import imaplib
import requests

from mist.io.tests import config

from mist.io.tests.gui.features.steps.ssh import *

from mist.core.tests.gui.steps.machines import *
from mist.core.tests.gui.steps.user_actions import *
from mist.core.tests.gui.steps.sso import *
from mist.core.tests.gui.steps.clouds import *
from mist.core.tests.gui.steps.general import *

log = logging.getLogger(__name__)


@when(u'I fill my production credentials')
def fill_prod_creds(context):
    email_textfield = context.browser.find_element_by_id("signin-email")
    password_textfield = context.browser.find_element_by_id("signin-password")

    email_textfield.send_keys(context.mist_config['EMAIL'])
    password_textfield.send_keys(context.mist_config['PASSWORD1'])


@when(u'I delete old emails')
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


@then(u'I should receive an email within {seconds} seconds')
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


@given(u'That the account with email "{email}" is deleted')
def delete_email_acount(context, email):
    requests.packages.urllib3.disable_warnings()
    payload = {'password': ''}
    url = "{0}/{1}/{2}".format(context.mist_config['MIST_URL'], 'delete_account'
                               , email)
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        raise requests.RequestException("Status code of response received "
                                        "was not 200")


@given(u'special {service} account for registration testing')
def override_sso_creds(context, service):
    if service == 'Google':
        context.mist_config['GOOGLE_TEST_EMAIL'] = \
            config.GOOGLE_REGISTRATION_TEST_EMAIL
        context.mist_config['GOOGLE_TEST_PASSWORD'] = \
            config.GOOGLE_REGISTRATION_TEST_PASSWORD
    elif service == 'Github':
        context.mist_config['GITHUB_TEST_EMAIL'] = \
            config.GITHUB_REGISTRATION_TEST_EMAIL
        context.mist_config['GITHUB_TEST_PASSWORD'] = \
            config.GITHUB_REGISTRATION_TEST_PASSWORD
    else:
        raise ValueError("Unknown authentication provider")


@then(u'my name should be "{my_name}"')
def check_user_name(context, my_name):
    user_span = context.browser.find_element_by_class_name('owner')
    user_span_text = safe_get_element_text(user_span)
    assert user_span_text.lower() == my_name.lower(), "Name appearing on the" \
                                                      " screen is not " \
                                                      "than %s" % my_name


@then(u'I should read "{something}" in input with id "{input_id}"')
def check_input_for_text(context, something, input_id):
    input = None
    try:
        input = context.browser.find_element_by_id(input_id)
    except NoSuchElementException:
        pass
    assert input, 'Could not find element with id %s' % input_id
    assert input.get_attribute('value').lower() == something.lower(), \
        "Input text did not match what was expected"
