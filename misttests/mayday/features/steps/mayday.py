import os

from datetime import datetime

from selenium.webdriver.common.by import By

from misttests.integration.gui.steps.mail import *
from misttests.integration.gui.steps.sso import *
from misttests.integration.gui.steps.navigation import *
from misttests.integration.gui.steps.landing import *
from misttests.integration.gui.steps.clouds import *
from misttests.integration.gui.steps.search import search_for_something
from misttests.integration.gui.steps.graphs import *
from misttests.integration.gui.steps.machines import *
from misttests.integration.gui.steps.popups import *
from misttests.integration.gui.steps.modals import *
from misttests.integration.gui.steps.ssh import *
from misttests.integration.gui.steps.browser import *
from misttests.integration.gui.steps.dialog import *
from misttests.integration.gui.steps.list import *
from misttests.integration.gui.steps.logs import *
from misttests.integration.gui.steps.utils import safe_get_element_text, expand_shadow_root, get_page_element

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from behave import step
from time import sleep, time

import requests


@step('I search for the mayday machine')
def search_for_mayday_machine(context):
    text = context.mist_config.get('MAYDAY_MACHINE', 'mayday')
    search_for_something(context, text)


def _get_imap_box(context):
    # using dmo.bar email service now as google won't allow less secure sign-ins
    # host, port = os.getenv('GMAIL_SOCKS_HOST'), os.getenv('GMAIL_SOCKS_PORT')
    host = context.mist_config['RULES_TEST_HOST']
    port = context.mist_config.get('RULES_TEST_PORT', None)
    try:
        port = int(port)
    except (ValueError, TypeError):
        port = None
    if host and port:
        return imaplib.IMAP4_SSL(host, port)
    elif host:
        return imaplib.IMAP4_SSL(host)
    else:
        return imaplib.IMAP4_SSL("imap.gmail.com")


@step('I delete old mayday emails')
def delete_old_mayday_emails(context):

    box = _get_imap_box(context)
    box.login(context.mist_config['RULES_TEST_EMAIL'],
                      context.mist_config['RULES_TEST_PASSWORD'])
    box.select("INBOX")
    typ, data = box.search(None, 'ALL')
    if not data[0].split():
        return

    for num in data[0].split():
        box.store(num, '+FLAGS', '\\Deleted')
    box.expunge()
    logout_email(box)


@step('I should receive an email within {seconds} seconds')
def receive_mail(context, seconds):
    end_time = time() + int(seconds)
    error = ""

    while time() < end_time:
        try:
            box = _get_imap_box(context)
            box.login(context.mist_config['RULES_TEST_EMAIL'],
                              context.mist_config['RULES_TEST_PASSWORD'])
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

    assert False, 'Did not receive an email within %s seconds. %s' % (seconds,
                                                                       error)

@step('I click the mayday machine')
def click_mayday_machine(context):
    """
    This function will try to click a button that says exactly the same thing as
    the text given. If it doesn't find any button like that then it will try
    to find a button that contains the text given. If text is a key inside
    mist_config dict then it's value will be used.
    """
    if context.mist_config.get('MAYDAY_MACHINE'):
        text = context.mist_config['MAYDAY_MACHINE']
    button = context.browser.find_element(By.XPATH, "//vaadin-grid-table-row[.//strong[text()='%s']]" % text)
    clicketi_click(context, button)


@step('Mayday machine state should be "{state}" within {seconds} seconds')
def assert_mayday_machine_state(context, state, seconds):
    if context.mist_config.get('MAYDAY_MACHINE'):
        name = context.mist_config.get('MAYDAY_MACHINE')
    end_time = time() + int(seconds)
    while time() < end_time:
        machine = get_machine(context, name)
        if machine:
            try:
                if state in safe_get_element_text(machine):
                    return
            except NoSuchElementException:
                pass
            except StaleElementReferenceException:
                pass
        sleep(2)

    assert False, '%s state is not "%s"' % (name, state)


@step('I choose the mayday machine')
def reboot_mayday_machine(context):
    if context.mist_config.get('MAYDAY_MACHINE'):
        name = context.mist_config.get('MAYDAY_MACHINE')

    end_time = time() + 20
    while time() < end_time:
        machine = get_machine(context, name)
        if machine:
            checkbox = machine.find_element(By.CSS_SELECTOR, ".mist-check")
            checkbox.click()
            return

        sleep(2)
    assert False, 'Could not choose/tick %s machine' % name


@step('I fill "{value}" as metric value')
def rule_value(context, value):
    value_input = context.browser.find_element(By.XPATH, "//paper-input[@id='metricValue']")
    actions = ActionChains(context.browser)
    actions.move_to_element(value_input)
    actions.click()
    actions.send_keys(Keys.BACK_SPACE)
    actions.perform()

    actions.move_to_element(value_input)
    actions.click()
    actions.send_keys("0")
    actions.perform()


@step('I should see the incident "{incident}"')
def check_for_incident(context, incident):
    dashboard_page = get_page_element(context, 'dashboard')
    dashboard_shadow = expand_shadow_root(context, dashboard_page)
    app_incidents = dashboard_shadow.find_element(By.CSS_SELECTOR, 'app-incidents')
    app_incidents_shadow = expand_shadow_root(context, app_incidents)
    incidents_list = app_incidents_shadow.find_elements(By.CSS_SELECTOR, 'span.rule-condition')
    for item in incidents_list:
        if incident in safe_get_element_text(item):
            return

    assert False, "Incident %s was not found in the home page" % incident


@step('I add the MaydaySchedule via api')
def add_mayday_schedule(context):
    headers = {'Authorization': context.mist_config['MAYDAY_TOKEN']}
    conditions = [{'type': 'tags', 'tags': {'mayday-test': ''}}]

    payload = {
     'name': 'MaydayScheduler',
     'action':'stop',
     'schedule_type':'interval',
     'conditions': conditions,
     'schedule_entry': {'every': 4, 'period':'minutes'},
     'task_enabled': True
    }

    uri = context.mist_config['MIST_URL'] + '/api/v1/schedules'
    response = requests.post(uri, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200, "Could not add MaydayScheduler schedule!"


@step('I verify that machine with id "{machine_id}" has been seen the last {seconds} seconds')
def check_machine_last_seen(context, machine_id, seconds):
    celery_limit = int(seconds)
    if context.mist_config.get(machine_id):
        mayday_machine_id = context.mist_config[machine_id]

    headers = {'Authorization': context.mist_config['MAYDAY_TOKEN']}
    uri = context.mist_config['MIST_URL'] + '/api/v1/machines'
    response = requests.get(uri, headers=headers)

    for machine in response.json():
        if machine.get('id') == mayday_machine_id:
            machine_last_seen = datetime.strptime(machine.get('last_seen'), '%Y-%m-%d %H:%M:%S.%f')
            log.info('Machine last seen: ' + str(machine_last_seen))
            now = datetime.now()
            log.info('Now: ' + str(now))
            time_delta = (now - machine_last_seen).total_seconds()
            log.info('Timedelta: ' + str(time_delta))
            assert time_delta < celery_limit, "Machine has not been seen " \
                                              "the last %d seconds" % celery_limit
            return

    assert False, "Mayday machine with id %s was not found!" % mayday_machine_id
