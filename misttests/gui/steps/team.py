from behave import step

from .buttons import clicketi_click

from .utils import safe_get_element_text

import random
import requests
import json


def get_team_lists(context):
    return context.browser.find_elements_by_css_selector(
        'div#content div.team-page paper-material.team-page')


def get_member_list(context):
    team_lists = get_team_lists(context)
    widget_title = team_lists[0].find_element_by_tag_name('h3')
    if 'members in' in safe_get_element_text(widget_title).strip().lower():
        return team_lists[0]
    return team_lists[1]


def get_policy_list(context):
    team_lists = get_team_lists(context)
    widget_title = team_lists[0].find_element_by_tag_name('h3')
    if 'team policy' in safe_get_element_text(widget_title).strip().lower():
        return team_lists[0]
    return team_lists[1]


@step(u'user with email "{email}" should be {user_state}')
def check_user_state(context, email, user_state):
    user_state = user_state.strip().lower()
    if email in context.mist_config:
        email = context.mist_config[email]
    email = email.strip().lower()
    member_list = get_member_list(context)
    members = member_list.find_elements_by_tag_name('paper-item')
    for member in members:
        spans = map(lambda el: safe_get_element_text(el), member.find_elements_by_tag_name('span'))
        if spans[-1] == email:
            if user_state == 'pending' and spans[1] == 'pending':
                return True
            elif user_state == 'confirmed' and 'pending' != spans[1]:
                return True
            assert False, "User's(%s) state is not %s" % (spans[-1], user_state)
    assert False, "User is not among the team members"


@step(u'I delete user "{email}" from team')
def delete_member_from_team(context, email):
    member_list = get_member_list(context)
    members = member_list.find_elements_by_tag_name('paper-item')
    if email in context.mist_config:
        email = context.mist_config[email]
    email = email.strip().lower()
    for member in members:
        spans = map(lambda el: safe_get_element_text(el),
                    member.find_elements_by_tag_name('span'))
        if spans[-1] == email:
            button = member.find_element_by_class_name('delete-member')
            clicketi_click(context, button)
            return True
    assert False, "User is not among the team members"


@step(u'rbac members are initialized')
def initialize_rbac_members(context):
    BASE_EMAIL = context.mist_config['BASE_EMAIL']
    context.mist_config['MEMBER1_EMAIL'] = "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1,200000))
    context.mist_config['MEMBER2_EMAIL'] = "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1,200000))

    context.mist_config['ORG_NAME'] = "rbac_org_%d" % random.randint(1,200000)

    payload = {
        'email': context.mist_config['MEMBER1_EMAIL'],
        'password': context.mist_config['MEMBER1_PASSWORD'],
        'name': "Atheofovos Gkikas"
    }

    re = requests.post("%s/api/v1/dev/register" % context.mist_config['MIST_URL'], data=json.dumps(payload))

    return


@step(u'rbac members, organization and team are initialized')
def initialize_rbac_members(context):
    BASE_EMAIL = context.mist_config['BASE_EMAIL']
    context.mist_config['MEMBER1_EMAIL'] = "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1,200000))

    payload = {
        'email': context.mist_config['MEMBER1_EMAIL'],
        'password': context.mist_config['MEMBER1_PASSWORD'],
        'name': "Atheofovos Gkikas"
    }
    re = requests.post("%s/api/v1/dev/register" % context.mist_config['MIST_URL'], data=json.dumps(payload))

    payload = {
        'email': context.mist_config['EMAIL'],
        'password': context.mist_config['PASSWORD1'],
        'org_id': context.mist_config['ORG_ID']
    }
    re = requests.post("%s/api/v1/tokens" % context.mist_config['MIST_URL'], data=json.dumps(payload))

    api_token = re.json()['token']
    headers = {'Authorization': api_token}

    payload = {
        'name': "Test Team"
    }
    requests.post(context.mist_config['MIST_URL'] + "/api/v1/org/" + context.mist_config['ORG_ID'] + "/teams", data=json.dumps(payload), headers=headers)

    return


@step(u'script "{script_name}" is added')
def create_script_api_request(context, script_name):
    script_data = {'location_type':'inline','exec_type':'executable', 'name': script_name}
    bash_script = """#!/bin/bash
    touch ~/bla
    echo "whatever" > ~/bla
    echo "what else" >> ~/bla
    """
    payload = {
        'email': context.mist_config['EMAIL'],
        'password': context.mist_config['PASSWORD1'],
        'org_id': context.mist_config['ORG_ID']
    }

    re = requests.post("%s/api/v1/tokens" % context.mist_config['MIST_URL'], data=json.dumps(payload))

    api_token = re.json()['token']
    headers = {'Authorization': api_token}

    script_data['script'] = bash_script

    requests.post(context.mist_config['MIST_URL'] + "/api/v1/scripts" , data=json.dumps(script_data), headers=headers)


@step(u'cloud Docker has been added')
def add_docker_api_request(context):
    payload = {
        'email': context.mist_config['EMAIL'],
        'password': context.mist_config['PASSWORD1'],
        'org_id': context.mist_config['ORG_ID']
    }

    re = requests.post("%s/api/v1/tokens" % context.mist_config['MIST_URL'], data=json.dumps(payload))

    api_token = re.json()['token']
    headers = {'Authorization': api_token}

    payload = {
        'title': "Docker",
        'provider': "docker",
        'docker_host': context.mist_config['CREDENTIALS']['DOCKER']['host'],
        'docker_port': context.mist_config['CREDENTIALS']['DOCKER']['port'],
        'authentication': context.mist_config['CREDENTIALS']['DOCKER']['authentication'],
        'ca_cert_file': context.mist_config['CREDENTIALS']['DOCKER']['ca'],
        'key_file': context.mist_config['CREDENTIALS']['DOCKER']['key'],
        'cert_file': context.mist_config['CREDENTIALS']['DOCKER']['cert']
    }

    response = requests.post(context.mist_config['MIST_URL'] + "/api/v1/clouds", data=json.dumps(payload), headers=headers)
