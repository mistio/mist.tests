from misttests.config import inject_vault_credentials
from misttests.config import MIST_URL
from misttests.integration.api.helpers import poll
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.mistrequests import MistRequests

V2_ENDPOINT = 'api/v2'
CLOUDS_ENDPOINT = f'{V2_ENDPOINT}/clouds'
MACHINES_ENDPOINT = f'{V2_ENDPOINT}/machines'
IMAGES_ENDPOINT = f'{V2_ENDPOINT}/images'
LOCATIONS_ENDPOINT = f'{V2_ENDPOINT}/locations'
VSPHERE_IMAGE = 'debian11-installer'


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
        },
        'extra': {
            'datastore': 'datastore2'
        },
    }
    inject_vault_credentials(add_cloud_request)
    clouds_uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=clouds_uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)
    # Wait for cloud to become available
    assert poll(api_token=api_token, uri=f'{clouds_uri}/{cloud_name}')
    # Wait for image to become available
    assert poll(api_token=api_token,
                uri=f'{MIST_URL}/{IMAGES_ENDPOINT}',
                query_params=[('cloud', cloud_name)],
                data={'name': VSPHERE_IMAGE},
                timeout=800)
    # Wait for locations to become available
    assert poll(api_token=api_token,
                uri=f'{MIST_URL}/{LOCATIONS_ENDPOINT}',
                query_params=[('cloud', cloud_name)],
                timeout=800)
    # Create machine
    machine_name = uniquify_string('test-machine')
    add_machine_request = {
        'name': machine_name,
        'cloud': cloud_name,
        'image': VSPHERE_IMAGE,
        'size': {'memory': 256, 'cpu': 1},
        'dry': False
    }
    machines_uri = f'{MIST_URL}/{MACHINES_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=machines_uri, json=add_machine_request)
    response = request.post()
    assert_response_ok(response)
    # Wait for machine to become available
    assert poll(api_token=api_token,
                uri=machines_uri,
                query_params=[('cloud', cloud_name)],
                data={'name': machine_name},
                timeout=800)
    snapshot_name = uniquify_string('test-snapshot')
    setup_data = {
        'create_snapshot': {'query_string': [('name', snapshot_name)]},
        'snapshot': snapshot_name,
        'cloud': cloud_name,
        'machine': machine_name,
    }
    return setup_data


def teardown(api_token, setup_data):
    # Destroy machine
    machine_name = setup_data['machine']
    uri = (f'{MIST_URL}/{MACHINES_ENDPOINT}'
           f'/{machine_name}/actions/destroy')
    request = MistRequests(api_token=api_token, uri=uri)
    request.post()
    # Remove cloud
    cloud_name = setup_data['cloud']
    uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}/{cloud_name}'
    request = MistRequests(
        api_token=api_token, uri=uri)
    request.delete()
