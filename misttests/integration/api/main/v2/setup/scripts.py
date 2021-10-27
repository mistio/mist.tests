from misttests import config
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.mistrequests import MistRequests

V1_ENDPOINT = 'api/v1'
V2_ENDPOINT = 'api/v2'
CLOUDS_V1_ENDPOINT = f'{V1_ENDPOINT}/clouds'
CLOUDS_V2_ENDPOINT = f'{V2_ENDPOINT}/clouds'
KEYS_ENDPOINT = f'{V2_ENDPOINT}/keys'
MACHINES_ENDPOINT = f'{V2_ENDPOINT}/machines'
IMAGES_ENDPOINT = f'{V2_ENDPOINT}/images'


def setup(api_token):
    # Add cloud
    cloud_name = uniquify_string('test-cloud')
    add_cloud_request = {
        "name": cloud_name,
        "provider": "docker",
        "credentials": {
            "tlsCaCert": None,
            "tlsCert": None,
            "tlsKey": None,
            "host": None,
            "port": None
        }
    }
    config.inject_vault_credentials(add_cloud_request)
    uri = f'{config.MIST_URL}/{CLOUDS_V2_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)
    # Add key
    key_name = uniquify_string('test-key')
    add_key_request = {
        "name": key_name,
        "generate": True
    }
    keys_uri = f'{config.MIST_URL}/{KEYS_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=keys_uri, json=add_key_request)
    response = request.post()
    assert_response_ok(response)
    key_id = response.json().get('id')
    # Get cloud id
    cloud_uri = f'{config.MIST_URL}/{CLOUDS_V2_ENDPOINT}/{cloud_name}'
    request = MistRequests(
        api_token=api_token, uri=cloud_uri)
    response = request.get()
    assert_response_ok(response)
    cloud_id = response.json().get('data', {}).get('id', '')
    # Get image id
    image_name = 'debian-ssh'
    image_uri = f'{config.MIST_URL}/{IMAGES_ENDPOINT}/{image_name}'
    request = MistRequests(
        api_token=api_token, uri=image_uri)
    response = request.get()
    assert_response_ok(response)
    image_id = response.json().get('data', {}).get('id', '')
    # Create machine
    machine_name = uniquify_string('test-machine')
    add_machine_request = {
        "name": machine_name,
        "provider": "docker",
        "image": image_id,
        "key": key_id,
        "size": ''
    }
    machines_uri = \
        f'{config.MIST_URL}/{CLOUDS_V1_ENDPOINT}/{cloud_id}/machines'
    request = MistRequests(
        api_token=api_token, uri=machines_uri, json=add_machine_request)
    response = request.post()
    assert_response_ok(response)
    return {
        'cloud': cloud_name,
        'key': key_name,
        'machine': machine_name
    }


def teardown(api_token, setup_data):
    # Destroy machine
    machine_name = setup_data['machine']
    uri = (f'{config.MIST_URL}/{MACHINES_ENDPOINT}'
           f'/{machine_name}/actions/destroy')
    request = MistRequests(api_token=api_token, uri=uri)
    response = request.post()
    assert_response_ok(response)
    # Delete key
    key_name = setup_data['key']
    uri = f'{config.MIST_URL}/{KEYS_ENDPOINT}/{key_name}'
    request = MistRequests(api_token=api_token, uri=uri)
    response = request.delete()
    assert_response_ok(response)
    # Remove cloud
    cloud_name = setup_data['cloud']
    uri = f'{config.MIST_URL}/{CLOUDS_V2_ENDPOINT}/{cloud_name}'
    request = MistRequests(
        api_token=api_token, uri=uri)
    response = request.delete()
    assert_response_ok(response)
