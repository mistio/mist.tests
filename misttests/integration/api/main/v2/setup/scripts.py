from misttests.config import inject_vault_credentials
from misttests.config import MIST_URL
from misttests.integration.api.helpers import poll
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.mistrequests import MistRequests

V2_ENDPOINT = 'api/v2'
CLOUDS_V2_ENDPOINT = f'{V2_ENDPOINT}/clouds'
KEYS_ENDPOINT = f'{V2_ENDPOINT}/keys'
MACHINES_ENDPOINT = f'{V2_ENDPOINT}/machines'
IMAGES_ENDPOINT = f'{V2_ENDPOINT}/images'
DOCKER_IMAGE = 'debian-ssh'


def setup(api_token):
    # Add cloud
    cloud_name = uniquify_string('test-cloud')
    add_cloud_request = {
        'name': cloud_name,
        'provider': 'docker',
        'credentials': {
            'tlsCaCert': None,
            'tlsCert': None,
            'tlsKey': None,
            'host': None,
            'port': None
        }
    }
    inject_vault_credentials(add_cloud_request)
    uri = f'{MIST_URL}/{CLOUDS_V2_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)
    # Add key
    key_name = uniquify_string('test-key')
    add_key_request = {
        'name': key_name,
        'generate': True
    }
    keys_uri = f'{MIST_URL}/{KEYS_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=keys_uri, json=add_key_request)
    response = request.post()
    assert_response_ok(response)
    # Wait for image to become available
    assert poll(
        api_token=api_token,
        uri=f'{MIST_URL}/{IMAGES_ENDPOINT}',
        query_params=[('cloud', cloud_name)],
        data={'name': DOCKER_IMAGE})
    # Create machine
    machine_name = uniquify_string('test-machine')
    add_machine_request = {
        'name': machine_name,
        'cloud': cloud_name,
        'provider': 'docker',
        'image': DOCKER_IMAGE,
        'key': key_name,
        'dry': False
    }
    machines_uri = f'{MIST_URL}/{MACHINES_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=machines_uri, json=add_machine_request)
    response = request.post()
    assert_response_ok(response)
    # Wait for machine to become available
    assert poll(
        api_token=api_token,
        uri=machines_uri,
        query_params=[('cloud', cloud_name)],
        data={'name': machine_name},
        timeout=800)
    script_name = uniquify_string('test-script')
    test_args = {
        'add_script': {
            'request_body': {
                'name': script_name,
                'exec_type': 'executable',
                'script': '#!/usr/bin/env bash\necho Hello, World!',
                'location_type': 'inline'
            },
        },
        'edit_script': {'query_string': [('name', script_name)]},
        'run_script': {
            'request_body': {
                'su': 'false',
                'machine': machine_name
            }
        }
    }
    setup_data = dict(**test_args,
                      script=script_name,
                      cloud=cloud_name,
                      key=key_name,
                      machine=machine_name)
    return setup_data


def teardown(api_token, setup_data):
    # Destroy machine
    machine_name = setup_data['machine']
    uri = (f'{MIST_URL}/{MACHINES_ENDPOINT}'
           f'/{machine_name}/actions/destroy')
    request = MistRequests(api_token=api_token, uri=uri)
    request.post()
    # Delete key
    key_name = setup_data['key']
    uri = f'{MIST_URL}/{KEYS_ENDPOINT}/{key_name}'
    request = MistRequests(api_token=api_token, uri=uri)
    request.delete()
    # Remove cloud
    cloud_name = setup_data['cloud']
    uri = f'{MIST_URL}/{CLOUDS_V2_ENDPOINT}/{cloud_name}'
    request = MistRequests(api_token=api_token, uri=uri)
    request.delete()
