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
        "provider": "google",
        "credentials": {
            "projectId": "projectId",
            "privateKey": "privateKey",
            "email": "email"
        },
    }
    config.inject_vault_credentials(add_cloud_request)
    uri = config.MIST_URL + '/api/v2/clouds'
    request = MistRequests(
        api_token=api_token, uri=uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)
    # Add key
    add_key_request = {
        "name": KEY_NAME,
        "private": "-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQCqGKukO1De7zhZj6+H0qtjTkVxwTCpvKe4eCZ0FPqri0cb2JZfXJ/DgYSF6vUp wmJG8wVQZKjeGcjDOL5UlsuusFncCzWBQ7RKNUSesmQRMSGkVb1/3j+skZ6UtW+5u09lHNsj6tQ5 1s1SPrCBkedbNf0Tp0GbMJDyR4e9T04ZZwIDAQABAoGAFijko56+qGyN8M0RVyaRAXz++xTqHBLh 3tx4VgMtrQ+WEgCjhoTwo23KMBAuJGSYnRmoBZM3lMfTKevIkAidPExvYCdm5dYq3XToLkkLv5L2 pIIVOFMDG+KESnAFV7l2c+cnzRMW0+b6f8mR1CJzZuxVLL6Q02fvLi55/mbSYxECQQDeAw6fiIQX GukBI4eMZZt4nscy2o12KyYner3VpoeE+Np2q+Z3pvAMd/aNzQ/W9WaI+NRfcxUJrmfPwIGm63il AkEAxCL5HQb2bQr4ByorcMWm/hEP2MZzROV73yF41hPsRC9m66KrheO9HPTJuo3/9s5p+sqGxOlF L0NDt4SkosjgGwJAFklyR1uZ/wPJjj611cdBcztlPdqoxssQGnh85BzCj/u3WqBpE2vjvyyvyI5k X6zk7S0ljKtt2jny2+00VsBerQJBAJGC1Mg5Oydo5NwD6BiROrPxGo2bpTbu/fhrT8ebHkTz2epl U9VQQSQzY1oZMVX8i1m5WUTLPz2yLJIBQVdXqhMCQBGoiuSoSjafUhV7i1cEGpb88h5NBYZzWXGZ 37sJ5QsW+sJyoNde3xH8vdXhzU7eT82D6X/scw9RZz+/6rCJ4p0=\n-----END RSA PRIVATE KEY-----"
    }
    config.inject_vault_credentials(add_key_request)
    keys_uri = config.MIST_URL + '/api/v2/keys'
    request = MistRequests(
        api_token=api_token,
        uri=keys_uri,
        json=add_key_request)
    request_method = getattr(request, 'POST'.lower())
    response = request_method()
    assert_response_ok(response)
    location_found = False
    image_found = False
    size_found = False
    key_found = False
    resources_found = False

    while not resources_found:
        location_uri = f'{config.MIST_URL}/api/v2/locations/{MACHINE_LOCATION}'
        images_uri = f'{config.MIST_URL}/api/v2/images/{MACHINE_IMAGE}'
        size_uri = f'{config.MIST_URL}/api/v2/sizes/{MACHINE_SIZE}'
        key_uri = f'{config.MIST_URL}/api/v2/sizes/{KEY_NAME}'
        if not location_found:
            location_found = is_data_available(api_token, location_uri)
        if not image_found:
            image_found = is_data_available(api_token, images_uri)
        if not size_found:
            size_found = is_data_available(api_token, size_uri)
        if not key_found:
            key_found = is_data_available(api_token, key_uri)
        resources_found = location_found and image_found and size_found and \
            key_found
        if resources_found:
            break
        sleep(10)

    # Create a machine
    add_machine_request = {
        "name": MACHINE_NAME,
        "provider": "google",
        "cloud": CLOUD_NAME,
        "location": MACHINE_LOCATION,
        "image": MACHINE_IMAGE,
        "size": MACHINE_SIZE,
        "key": KEY_NAME,
        "dry": False
    }
    machines_uri = config.MIST_URL + '/api/v2/machines'
    request = MistRequests(
        api_token=api_token, uri=machines_uri, json=add_machine_request)
    response = request.post()
    assert_response_ok(response)
    global machine_job_id
    machine_job_id = response.json().get('jobId') or \
        response.json().get('job_id')
    return {'job_id': machine_job_id}


def teardown(api_token):
    jobs_uri = f'{config.MIST_URL}/api/v2/jobs/{machine_job_id}'
    if is_data_available(api_token, jobs_uri):
        sleep(200)
        # Destroy the machine
        uri = (f'{config.MIST_URL}/api/v2/machines'
               f'/{MACHINE_NAME}/actions/destroy')
        request = MistRequests(api_token=api_token, uri=uri)
        response = request.post()
    # Delete key
    uri = f'{config.MIST_URL}/api/v2/keys/{KEY_NAME}'
    request = MistRequests(api_token=api_token, uri=uri)
    request_method = getattr(request, 'DELETE'.lower())
    response = request_method()
    assert_response_ok(response)
    # Remove the cloud
    uri = f'{config.MIST_URL}/api/v2/clouds/{CLOUD_NAME}'
    request = MistRequests(
        api_token=api_token, uri=uri)
    response = request.delete()
    assert_response_ok(response)
