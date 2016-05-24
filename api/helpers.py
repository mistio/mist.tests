import json
import string
import random

from tests.api.utils import *

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

    return script['script_id'], script_name


def get_teams_with_name(name, teams):
    return filter(lambda x: x['name'] == name, teams)


def get_random_team_name(existing_teams):
    while True:
        random_team_name = ''.join([random.choice(string.ascii_letters +
                                                    string.digits) for _ in
                                      range(6)])
        teams = get_teams_with_name(random_team_name, existing_teams)
        if len(teams) == 0:
            return random_team_name


def get_keys_with_name(name, keys):
    return filter(lambda x: x['name'] == name, keys)


def get_random_key_name(existing_keys):
     while True:
        random_key_name = ''.join([random.choice(string.ascii_letters +
                                                string.digits) for _ in
                                  range(6)])
        keys = get_keys_with_name(random_key_name, existing_keys)
        if len(keys) == 0:
            return random_key_name
