from time import sleep
from misttests import config
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.mistrequests import MistRequests

V1_ENDPOINT = 'api/v1'
V2_ENDPOINT = 'api/v2'
CLOUDS_V1_ENDPOINT = f'{V1_ENDPOINT}/clouds'
CLOUDS_V2_ENDPOINT = f'{V2_ENDPOINT}/clouds'
MACHINES_ENDPOINT = f'{V2_ENDPOINT}/machines'
IMAGES_ENDPOINT = f'{V2_ENDPOINT}/images'


class ImageNotFound(Exception):
    pass


def setup(api_token):
    # Add cloud
    cloud_name = uniquify_string('test-cloud')
    add_cloud_request = {
        'name': cloud_name,
        'provider': 'vsphere',
        'credentials': {
            'ca_cert_file': None,
            'host': None,
            'password': None,
            'username': None
        }
    }
    config.inject_vault_credentials(add_cloud_request)
    uri = f'{config.MIST_URL}/{CLOUDS_V2_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)
    # Get cloud id
    cloud_uri = f'{config.MIST_URL}/{CLOUDS_V2_ENDPOINT}/{cloud_name}'
    request = MistRequests(
        api_token=api_token, uri=cloud_uri)
    response = request.get()
    assert_response_ok(response)
    cloud_id = response.json()['data']['id']
    # Get image id
    image_name = 'template'
    image_uri = f'{config.MIST_URL}/{IMAGES_ENDPOINT}/{image_name}'
    request = MistRequests(
        api_token=api_token, uri=image_uri)

    for _ in range(10):
        response = request.get()
        try:
            assert_response_ok(response)
            image_id = response.json()['data']['id']
        except (KeyError, AssertionError):
            sleep(10)
        else:
            break
    else:
        raise ImageNotFound()

    # Create machine
    machine_name = uniquify_string('test-machine')
    add_machine_request = {
        'name': machine_name,
        'image': image_id,
        'size': {'ram': 256, 'cpu': 1},
        'async': True
    }
    machines_uri = \
        f'{config.MIST_URL}/{CLOUDS_V1_ENDPOINT}/{cloud_id}/machines'
    request = MistRequests(
        api_token=api_token, uri=machines_uri, json=add_machine_request)
    response = request.post()
    assert_response_ok(response)
    snapshot_name = uniquify_string('test-snapshot')
    query_string = {'create_snapshot': [('name', snapshot_name)]}
    sleep(200)
    return {
        'cloud': cloud_name,
        'machine': machine_name,
        'snapshot': snapshot_name,
        'query_string': query_string
    }


def teardown(api_token, setup_data):
    # Destroy machine
    machine_name = setup_data['machine']
    uri = (f'{config.MIST_URL}/{MACHINES_ENDPOINT}'
           f'/{machine_name}/actions/destroy')
    request = MistRequests(api_token=api_token, uri=uri)
    request.post()
    # Remove cloud
    cloud_name = setup_data['cloud']
    uri = f'{config.MIST_URL}/{CLOUDS_V2_ENDPOINT}/{cloud_name}'
    request = MistRequests(
        api_token=api_token, uri=uri)
    request.delete()
