import json
import string
import random
import smtplib
import requests

from tests.api.utils import *

from tests.config import get_value_of

bash_script_no_shebang = """
touch ~/bla
echo "whatever" > ~/bla
echo "what else" >> ~/bla
"""

bash_script = """#!/bin/bash
touch ~/bla
echo "whatever" > ~/bla
echo "what else" >> ~/bla
"""

ansible_script_with_error = """
- name: Dummy ansible playbook
hosts: localhost
  tasks:
   - name: Dummy task
     debug:
       msg: "Hello World"
"""

ansible_script = """
- name: Dummy ansible playbook
  hosts: localhost
  tasks:
   - name: Dummy task
     debug:
       msg: "Hello World"
"""


def get_scripts_with_name(name, scripts):
    return filter(lambda x: x['name'] == name, scripts)


def get_random_script_name(existing_scripts):
    while True:
        random_script_name = ''.join([random.choice(string.ascii_letters +
                                                    string.digits) for _ in
                                      range(6)])
        scripts = get_scripts_with_name(random_script_name, existing_scripts)
        if len(scripts) == 0:
            return random_script_name


def add_bash_script(mist_core, valid_api_token):
    response = mist_core.list_scripts(api_token=valid_api_token).get()
    assert_response_ok(response)
    script_list = json.loads(response.content)
    script_name = get_random_script_name(script_list)
    response = mist_core.add_script(api_token=valid_api_token,
                                    name=script_name,
                                    location_type='inline',
                                    exec_type='executable',
                                    script=bash_script).post()
    assert_response_ok(response)
    response = mist_core.list_scripts(api_token=valid_api_token).get()
    assert_response_ok(response)
    script = get_scripts_with_name(
        script_name,
        json.loads(response.content))
    assert_list_not_empty(script, "Script was added but is not visible in"
                                  " the list of scripts")
    script = script[0]

    return script['id'], script_name


def get_teams_with_name(name, teams):
    return filter(lambda x: x['name'] == name, teams)


def get_random_str():
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in
                    range(6)])


def get_random_team_name(existing_teams):
    while True:
        random_team_name = get_random_str()
        teams = get_teams_with_name(random_team_name, existing_teams)
        if len(teams) == 0:
            return random_team_name


def get_keys_with_id(name, keys):
    return filter(lambda x: x['name'] == name, keys)


def get_random_key_id(existing_keys):
     while True:
        random_key_name = get_random_str()
        keys = get_keys_with_id(random_key_name, existing_keys)
        if len(keys) == 0:
            return random_key_name

def destroy_machine(log, mist_core, api_token, cloud_id, machine_id):
    response = mist_core.destroy_machine(api_token=api_token,
                                         cloud_id=cloud_id,
                                         machine_id=machine_id).post()
    try:
        assert_response_ok(response)
        log.info("Machine destruction command has been submitted successfully!")
    except AssertionError as e:
        log.error("Machine destruction was not successful!")
        raise e

def mp_fail_notify(error, provider, image_name, stage):
    slack_hook = get_value_of('SLACK_HOOK', '')
    #gmail_pwd = get_value_of('GOOGLE_TEST_PASSWORD', '')
    #FROM = get_value_of('GOOGLE_TEST_EMAIL', '')
    #TO = get_value_of('MP_NOTIFY_EMAIL', '')
    if stage == 'provision':
        SUBJECT = '[Multiprovision-tests] Provisioning failed for ' + provider + ' and image ' + image_name
    elif stage == 'deploy':
        SUBJECT = '[Multiprovision-tests] Deployment failed for ' + provider + ' and image ' + image_name
    elif stage == 'destroy':
        SUBJECT = '[Multiprovision-tests] Failed to destroy machine for ' + provider + ' and image ' + image_name
    #TEXT = error_json['error']

    #message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    #""" % (FROM, TO, SUBJECT, TEXT)

    #send an email
    #server = smtplib.SMTP('smtp.gmail.com:587')
    #server.ehlo()
    #server.starttls()
    #server.login(FROM, gmail_pwd)
    #server.sendmail(FROM, TO, message)
    #server.quit()

    #post to Slack
    attachments = [ { 'color':'danger', 'title': 'Error Message', 'text' : str(error.message) } ]
    headers = {"Content-type": "application/json"}
    payload = {"text": SUBJECT, "attachments": attachments}
    response = requests.post(slack_hook, json=payload)

def mp_success_notify(provider, image_name):
    slack_hook = get_value_of('SLACK_HOOK', '')
    SUBJECT = 'Provisioning worked for ' + provider + ' and image ' + image_name
    attachments = [ { 'color':'good', 'title': 'Test: ', 'text' : SUBJECT } ]
    #post to Slack
    headers = {"Content-type": "application/json"}
    payload = {"text": '[Multiprovision-tests] Test successful', "attachments": attachments}
    response = requests.post(slack_hook, json=payload)
