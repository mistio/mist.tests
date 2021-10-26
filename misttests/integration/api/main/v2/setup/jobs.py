from time import sleep
from misttests import config
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.mistrequests import MistRequests


def setup(api_token):
    # Add a cloud
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
    uri = config.MIST_URL + '/api/v2/clouds'
    request = MistRequests(
        api_token=api_token, uri=uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)
    # Get cloud id
    cloud_uri = f'{config.MIST_URL}/api/v2/clouds/{cloud_name}'
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
    machine_name = uniquify_string('test-machine')
    add_machine_request = {
        "name": machine_name,
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
    return {
        'cloud': cloud_name,
        'machine': machine_name,
        'job_id': job_id
    }


def teardown(api_token, setup_data):
    # Destroy the machine
    machine_name = setup_data['machine']
    uri = (f'{config.MIST_URL}/api/v2/machines'
           f'/{machine_name}/actions/destroy')
    request = MistRequests(api_token=api_token, uri=uri)
    response = request.post()
    assert_response_ok(response)
    # Remove the cloud
    cloud_name = setup_data['cloud']
    uri = f'{config.MIST_URL}/api/v2/clouds/{cloud_name}'
    request = MistRequests(
        api_token=api_token, uri=uri)
    response = request.delete()
    assert_response_ok(response)
