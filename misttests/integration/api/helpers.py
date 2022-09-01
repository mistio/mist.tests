import time
import uuid
import json
import string
import random

from misttests.integration.api.utils import *
from misttests.integration.api.mistrequests import MistRequests
from misttests import config

from misttests.config import safe_get_var


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
    return [x for x in scripts if x['name'] == name]


def get_random_script_name(existing_scripts):
    while True:
        random_script_name = ''.join([random.choice(string.ascii_letters +
                                                    string.digits) for _ in
                                      range(6)])
        scripts = get_scripts_with_name(random_script_name, existing_scripts)
        if len(scripts) == 0:
            return random_script_name


def add_bash_script(mist_api_v1, valid_api_token):
    response = mist_api_v1.list_scripts(api_token=valid_api_token).get()
    assert_response_ok(response)
    script_list = json.loads(response.content)
    script_name = get_random_script_name(script_list)
    response = mist_api_v1.add_script(api_token=valid_api_token,
                                    name=script_name,
                                    location_type='inline',
                                    exec_type='executable',
                                    script=bash_script).post()
    assert_response_ok(response)
    response = mist_api_v1.list_scripts(api_token=valid_api_token).get()
    assert_response_ok(response)
    script = get_scripts_with_name(
        script_name,
        json.loads(response.content))
    assert_list_not_empty(script, "Script was added but is not visible in"
                                  " the list of scripts")
    script = script[0]

    return script['id'], script_name


def get_teams_with_name(name, teams):
    return [x for x in teams if x['name'] == name]


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
    return [x for x in keys if x['name'] == name]


def get_random_key_name(existing_keys):
    while True:
        random_key_name = get_random_str()
        keys = get_keys_with_id(random_key_name, existing_keys)
        if len(keys) == 0:
            return random_key_name


def uniquify_string(string):
    return f"{string}-{str(uuid.uuid4()).split('-')[0]}"


def destroy_machine(log, mist_api_v1, api_token, cloud_id, machine_id):
    mist_api_v1.list_machines(cloud_id=cloud_id, api_token=api_token).get()
    response = mist_api_v1.destroy_machine(api_token=api_token,
                                         cloud_id=cloud_id,
                                         machine_id=machine_id).post()
    try:
        assert_response_ok(response)
        log.info("Machine destruction command has been submitted successfully!")
    except AssertionError as e:
        log.error("Machine destruction was not successful!")
        raise e


def find_subdict(obj, subdict, exact_match=False):
    def contains(dict1, dict2):
        if exact_match:
            return dict2.items() <= dict1.items()
        for k, v in dict2.items():
            kcontained = k in dict1
            if kcontained and isinstance(v, dict):
                valcontained = v.items() <= dict1[k].items()
            elif kcontained and isinstance(v, int):
                valcontained = (v == dict1[k])
            elif kcontained:
                valcontained = v in dict1[k]
            if not kcontained or not valcontained:
                return False
        return True
    if isinstance(obj, dict):
        return contains(obj, subdict)
    for d in obj:
        if isinstance(d, dict) and contains(d, subdict):
            return True
    return False


def poll(api_token, uri, data={}, query_params=None,
         timeout=60 * 5, interval=10, post_delay=None):
    req_kwargs = dict(api_token=api_token, uri=uri)
    if query_params:
        req_kwargs['params'] = query_params
    request = MistRequests(**req_kwargs)
    t_end = time.time() + timeout
    while time.time() < t_end:
        response = request.get()
        response_body = response.json()
        try:
            response_data = response_body['data']
        except (KeyError, TypeError):
            response_data = response_body
        if response_data and not data:
            return True
        if data and find_subdict(response_data, data):
            if post_delay:
                time.sleep(post_delay)
            return True
        time.sleep(interval)
    return False
