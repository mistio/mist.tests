from behave import step

from misttests.config import safe_get_var, DEFAULT_IMAGE_NAME
import requests
import random
import json

from random import randrange


@step('rbac member1 has been registered')
def register_member_1(context):
    BASE_EMAIL = context.mist_config['BASE_EMAIL']
    context.mist_config['MEMBER1_EMAIL'] = "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1,200000))
    context.mist_config['MEMBER2_EMAIL'] = "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1,200000))
    context.mist_config['ORG_NAME'] = "rbac_org_%d" % random.randint(1,200000)
    payload = {
        'email': context.mist_config['MEMBER1_EMAIL'],
        'password': context.mist_config['MEMBER1_PASSWORD'],
        'name': "Atheofovos Gkikas"
    }

    requests.post("%s/api/v1/dev/register" % context.mist_config['MIST_URL'], data=json.dumps(payload))

    return


def get_owner_api_token(context):
    payload = {
        'email': context.mist_config['EMAIL'],
        'password': context.mist_config['PASSWORD1'],
        'org_id': context.mist_config['ORG_ID']
    }
    re = requests.post("%s/api/v1/tokens" % context.mist_config['MIST_URL'], data=json.dumps(payload))

    api_token = re.json()['token']

    return api_token


def add_user_to_team(context, email):

    headers = {'Authorization': get_owner_api_token(context)}

    payload = {
        'email': email
    }

    endpoint = context.mist_config['MIST_URL'] + "/api/v1/dev/orgs/" + context.mist_config['ORG_ID'] + "/teams/" + context.mist_config['TEAM_ID']

    response = requests.post(endpoint, data=json.dumps(payload), headers=headers)

    assert response.status_code == 200, "Could not add %s to Test Team. Response was %s" % (email, response.status_code)


def register_member(context, email, password):
    payload = {
        'email': email,
        'password': password,
        'name': "Atheofovos Gkikas"
    }

    requests.post("%s/api/v1/dev/register" % context.mist_config['MIST_URL'], data=json.dumps(payload))


@step(u'rbac members, organization and team are initialized')
def initialize_rbac_members(context):


    BASE_EMAIL = context.mist_config['BASE_EMAIL']
    context.mist_config['MEMBER1_EMAIL'] = "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1,200000))
    context.mist_config['MEMBER2_EMAIL'] = "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1,200000))

    register_member(context, context.mist_config['MEMBER1_EMAIL'], context.mist_config['MEMBER1_PASSWORD'])
    register_member(context, context.mist_config['MEMBER2_EMAIL'], context.mist_config['MEMBER2_PASSWORD'])

    headers = {'Authorization': get_owner_api_token(context)}

    payload = {
        'name': "Test Team"
    }
    response = requests.post(context.mist_config['MIST_URL'] + "/api/v1/org/" + context.mist_config['ORG_ID'] + "/teams", data=json.dumps(payload), headers=headers)

    assert response.status_code == 200, "Could not add Test Team. Response was %s" % response.status_code

    context.mist_config['TEAM_ID'] = response.json()['id']

    add_user_to_team(context, context.mist_config['MEMBER1_EMAIL'])
    add_user_to_team(context, context.mist_config['MEMBER2_EMAIL'])

    return

@step('"{protocol_name}" organization and teams are initialized')
def initialize_ad_org_teams(context, protocol_name):
    # Change organization name to AD_ORG_NAME
    payload = {
        'new_name': context.mist_config['AD_ORG_NAME']
    }
    headers = {'Authorization': get_owner_api_token(context)}

    response = requests.put('{}/api/v1/org/{}'.format(
        context.mist_config['MIST_URL'], context.mist_config['ORG_ID']),
        data=json.dumps(payload), headers=headers)
    # 409 means that the test is running again and org was created
    if(response.status_code != 409):
        assert response.status_code == 200, "Could not change org name. Response was {}, error was {}".format(response.status_code, response.text)
    # Add teams devs, finance and ops for AD login test or mistDev for LDAP
    if protocol_name == 'ad':
        teams = ['devs', 'finance', 'ops']
    if protocol_name == 'ldap':
        teams = ['mistDev']
    for team in teams:
        payload = {
            'name': team
        }
        team_response = requests.post(context.mist_config['MIST_URL'] + "/api/v1/org/" + context.mist_config['ORG_ID'] + "/teams", data=json.dumps(payload), headers=headers)
        assert team_response.status_code == 200, "Could not add {} team. Response was {}, error was {}".format(team, team_response.status_code, team_response.text)
        team_id = team_response.json()['id']
        rule1 = {'operator': 'ALLOW', 'action': '', 'rtype': 'cloud', 'rid': '', 'constraints': {}, 'rtags': {}}
        rule2 = {'operator': 'ALLOW', 'action': '', 'rtype': 'machine', 'rid': '', 'constraints': {}, 'rtags': {}}
        policy_payload = {'policy': {'rules': [rule1, rule2], 'operator': 'DENY'}}
        policy_url = context.mist_config['MIST_URL'] + '/api/v1/org/' + context.mist_config['ORG_ID'] + '/teams/' + team_id + '/policy'
        policy_response = requests.put(policy_url, data=json.dumps(policy_payload), headers=headers) 
        assert policy_response.status_code == 200, "Could not update policy for {} team. Response was {}, error was {}".format(team, policy_response.status_code, policy_response.text)

@step('script "{script_name}" has been added via API request')
def create_script_api_request(context, script_name):
    script_data = {'location_type':'inline','exec_type':'executable', 'name': script_name}
    bash_script = """#!/bin/bash\ntouch /var/dummy_file
    """
    headers = {'Authorization': get_owner_api_token(context)}

    script_data['script'] = bash_script

    requests.post(context.mist_config['MIST_URL'] + "/api/v1/scripts" , data=json.dumps(script_data), headers=headers)


@step('key "{key_name}" has been added via API request')
def add_key_api_request(context, key_name):
    if "random" in key_name:
        value_key = key_name
        key_name = key_name.replace("random", str(randrange(1000)))
        context.mist_config[value_key] = key_name
    payload = {
        'name': key_name,
        'priv': safe_get_var('keys/api_testing_machine_private_key', 'priv_key', context.mist_config['TESTING_PRIVATE_KEY'])
    }
    headers = {'Authorization': get_owner_api_token(context)}

    re = requests.put(context.mist_config['MIST_URL'] + "/api/v1/keys" , data=json.dumps(payload), headers=headers)
    assert re.status_code == 200, "Could not add key. Response was %s" % re.status_code
    context.mist_config['ASSOCIATED_KEY'] = re.json()['id']


@step('key "{key_name}" has been generated and added via API request')
def generate_add_key_api_request(context, key_name):
    if "random" in key_name:
        value_key = key_name
        key_name = key_name.replace("random", str(randrange(1000)))
        context.mist_config[value_key] = key_name
    headers = {'Authorization': get_owner_api_token(context)}

    re = requests.post(context.mist_config['MIST_URL'] + "/api/v1/keys" , headers=headers)
    payload = {
        'name': key_name,
        'priv': re.json().get('priv')
    }

    re = requests.put(context.mist_config['MIST_URL'] + "/api/v1/keys" , data=json.dumps(payload), headers=headers)
    assert re.status_code == 200, "Could not add key. Response was %s" % re.status_code


@step('cloud "{cloud}" has been added via API request')
def add_cloud_api_request(context, cloud):
    headers = {'Authorization': get_owner_api_token(context)}

    if cloud == 'Docker':

        if context.mist_config['LOCAL']:
            payload = {
                'name': "Docker",
                'provider': "docker",
                'docker_host': context.mist_config['LOCAL_DOCKER'],
                'docker_port': '2375',
                'show_all': True
            }

        else:

            payload = {
                'name': "Docker",
                'provider': "docker",
                'docker_host': safe_get_var('clouds/dockerhost', 'host', context.mist_config['CREDENTIALS']['DOCKER']['host']),
                'docker_port': safe_get_var('clouds/dockerhost', 'port', context.mist_config['CREDENTIALS']['DOCKER']['port']),
                'authentication': safe_get_var('clouds/dockerhost', 'authentication', context.mist_config['CREDENTIALS']['DOCKER']['authentication']),
                'ca_cert_file': safe_get_var('clouds/dockerhost', 'tlsCaCert', context.mist_config['CREDENTIALS']['DOCKER']['tlsCaCert']),
                'key_file': safe_get_var('clouds/dockerhost', 'tlsKey', context.mist_config['CREDENTIALS']['DOCKER']['tlsKey']),
                'cert_file': safe_get_var('clouds/dockerhost', 'tlsCert', context.mist_config['CREDENTIALS']['DOCKER']['tlsCert']),
                'show_all': True
            }

    elif cloud == 'GCE':
        payload = {
            'name': 'GCE',
            'provider': 'gce',
            'project_id': safe_get_var('clouds/gce/mist-dev-tests', 'projectId',
                                      context.mist_config['CREDENTIALS']['GCE']['projectId']),
            'private_key': json.dumps(safe_get_var('clouds/gce/mist-dev-tests', 'privateKeyDetailed',
                                   context.mist_config['CREDENTIALS']['GCE']['privateKeyDetailed'])),
            'dns_enabled': True
        }

    requests.post(context.mist_config['MIST_URL'] + "/api/v1/clouds", data=json.dumps(payload), headers=headers)


@step('Docker machine "{machine_name}" has been added via API request')
def create_docker_machine(context, machine_name):
    headers = {'Authorization': get_owner_api_token(context)}

    re = requests.get(context.mist_config['MIST_URL'] + "/api/v1/clouds", headers=headers)

    for cloud in re.json():
        if 'docker' in cloud['provider']:
            cloud_id = cloud['id']
            break
    else:
        raise Exception('No docker cloud added %s' % re.json())

    re = requests.get(context.mist_config['MIST_URL'] + "/api/v1/clouds/" + cloud_id + "/images", headers=headers)

    for image in re.json():
        if DEFAULT_IMAGE_NAME in image['name']:
            image_id = image['id']
            break

    if 'random' in machine_name:
        value_key = machine_name
        machine_name = machine_name.replace("random", str(randrange(1000)))
        context.mist_config[value_key] = machine_name

    payload = {
        'image': image_id,
        'name': machine_name,
        'provider': 'docker',
        'location': '',
        'size': '',
        'key': context.mist_config['ASSOCIATED_KEY'],
        'async': 1
    }

    re = requests.post(context.mist_config['MIST_URL'] + "/api/v1/clouds/" + cloud_id + "/machines", data=json.dumps(payload), headers=headers)
    assert re.status_code == 200, "Could not create machine. Response was %s" % re.status_code


@step('Docker machine "{machine_name}" with "{key_name}" key and "{script_name}" script has been added via API-v2 request')
def create_docker_machine_with_scheduled_script_v2(context,
                                                   machine_name,
                                                   key_name,
                                                   script_name):
    headers = {
        'Authorization': get_owner_api_token(context),
        'Content-Type': 'application/json',
    }

    if 'random' in machine_name:
        value_key = machine_name
        machine_name = machine_name.replace("random", str(randrange(1000)))
        context.mist_config[value_key] = machine_name

    payload = {
        'name': machine_name,
        'image': DEFAULT_IMAGE_NAME,
        'key': key_name,
        'schedules': [{
            'when': {
                'schedule_type': 'interval',
                'every': 1,
                'period': 'minutes',
            },
            'actions': [{
                'action_type': 'run_script',
                'script_type': 'existing',
                'script': script_name,
                'params': ''
            }],
        }],
        'dry': False,
    }

    response = requests.post(context.mist_config['MIST_URL'] + '/api/v2/machines',
                             data=json.dumps(payload), headers=headers)

    assert response.status_code == 200, 'Could not create machine. Response was %s' % response.status_code
