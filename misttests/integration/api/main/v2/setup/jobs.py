from time import sleep
from misttests import config
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.mistrequests import MistRequests


CLOUD_NAME = 'example-cloud'
KEY_NAME = 'example-key'
MACHINE_NAME = 'example-machine'
MACHINE_LOCATION = 'us-east1-b'
MACHINE_IMAGE = 'ubuntu-1804-bionic-v20210928'
MACHINE_SIZE = 'f1-micro'

machine_job_id = None


def is_data_available(api_token, uri):
    request = MistRequests(api_token=api_token, uri=uri)
    response = request.get()
    assert_response_ok(response)
    return bool(response.json().get('data'))


def setup(api_token):
    # Add a cloud
    add_cloud_request = {
        "name": CLOUD_NAME,
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
    uri = config.MIST_URL + '/api/v2/clouds'
    request = MistRequests(
        api_token=api_token, uri=uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)
    # Get cloud id
    cloud_uri = f'{config.MIST_URL}/api/v2/clouds/{CLOUD_NAME}'
    request = MistRequests(
        api_token=api_token, uri=cloud_uri)
    response = request.get()
    assert_response_ok(response)
    cloud_id = response.json().get('data', {}).get('id', '')
    # Get image id
    image_name = 'Debian Bullseye with SSH server'
    image_uri = f'{config.MIST_URL}/api/v2/images/{image_name}'
    request = MistRequests(
        api_token=api_token, uri=image_uri)
    response = request.get()
    assert_response_ok(response)
    image_id = response.json().get('data', {}).get('id', '')
    # Create a machine
    add_machine_request = {
        "name": MACHINE_NAME,
        "provider": "docker",
        "image": image_id,
        "size": '',
        "async": True
    }
    machines_uri = f'{config.MIST_URL}/api/v1/clouds/{cloud_id}/machines'
    request = MistRequests(
        api_token=api_token, uri=machines_uri, json=add_machine_request)
    response = request.post()
    assert_response_ok(response)
    job_id = response.json().get('jobId') or response.json().get('job_id')
    sleep(30)
    return {'job_id': job_id}


def teardown(api_token):
    # Destroy the machine
    uri = (f'{config.MIST_URL}/api/v2/machines'
           f'/{MACHINE_NAME}/actions/destroy')
    request = MistRequests(api_token=api_token, uri=uri)
    response = request.post()
    assert_response_ok(response)
    # Delete key
    uri = f'{config.MIST_URL}/api/v2/keys/{KEY_NAME}'
    request = MistRequests(api_token=api_token, uri=uri)
    request.delete()
    # Remove the cloud
    uri = f'{config.MIST_URL}/api/v2/clouds/{CLOUD_NAME}'
    request = MistRequests(
        api_token=api_token, uri=uri)
    response = request.delete()
    assert_response_ok(response)
