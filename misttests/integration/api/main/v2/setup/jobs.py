from misttests.config import inject_vault_credentials
from misttests.config import MIST_URL
from misttests.integration.api.helpers import poll
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.mistrequests import MistRequests

V2_ENDPOINT = 'api/v2'
CLOUDS_V2_ENDPOINT = f'{V2_ENDPOINT}/clouds'
MACHINES_ENDPOINT = f'{V2_ENDPOINT}/machines'
IMAGES_ENDPOINT = f'{V2_ENDPOINT}/images'
DOCKER_IMAGE = 'Debian Bullseye with SSH server'


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
        'dry': False
    }
    machines_uri = f'{MIST_URL}/{MACHINES_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=machines_uri, json=add_machine_request)
    response = request.post()
    assert_response_ok(response)
    response_json = response.json()
    job_id = response_json.get('jobId') or response_json.get('job_id')
    # Wait for machine to become available
    assert poll(
        api_token=api_token,
        uri=machines_uri,
        query_params=[('cloud', cloud_name)],
        data={'name': machine_name},
        timeout=800)
    setup_data = {
        'get_job': {'job_id': job_id},
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
    uri = f'{MIST_URL}/{CLOUDS_V2_ENDPOINT}/{cloud_name}'
    request = MistRequests(
        api_token=api_token, uri=uri)
    request.delete()
