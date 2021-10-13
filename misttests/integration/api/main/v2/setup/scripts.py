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
    # Create key
    create_key_request = {
        "name": "example-key",
        "private": "-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQCqGKukO1De7zhZj6+H0qtjTkVxwTCpvKe4eCZ0FPqri0cb2JZfXJ/DgYSF6vUp wmJG8wVQZKjeGcjDOL5UlsuusFncCzWBQ7RKNUSesmQRMSGkVb1/3j+skZ6UtW+5u09lHNsj6tQ5 1s1SPrCBkedbNf0Tp0GbMJDyR4e9T04ZZwIDAQABAoGAFijko56+qGyN8M0RVyaRAXz++xTqHBLh 3tx4VgMtrQ+WEgCjhoTwo23KMBAuJGSYnRmoBZM3lMfTKevIkAidPExvYCdm5dYq3XToLkkLv5L2 pIIVOFMDG+KESnAFV7l2c+cnzRMW0+b6f8mR1CJzZuxVLL6Q02fvLi55/mbSYxECQQDeAw6fiIQX GukBI4eMZZt4nscy2o12KyYner3VpoeE+Np2q+Z3pvAMd/aNzQ/W9WaI+NRfcxUJrmfPwIGm63il AkEAxCL5HQb2bQr4ByorcMWm/hEP2MZzROV73yF41hPsRC9m66KrheO9HPTJuo3/9s5p+sqGxOlF L0NDt4SkosjgGwJAFklyR1uZ/wPJjj611cdBcztlPdqoxssQGnh85BzCj/u3WqBpE2vjvyyvyI5k X6zk7S0ljKtt2jny2+00VsBerQJBAJGC1Mg5Oydo5NwD6BiROrPxGo2bpTbu/fhrT8ebHkTz2epl U9VQQSQzY1oZMVX8i1m5WUTLPz2yLJIBQVdXqhMCQBGoiuSoSjafUhV7i1cEGpb88h5NBYZzWXGZ 37sJ5QsW+sJyoNde3xH8vdXhzU7eT82D6X/scw9RZz+/6rCJ4p0=\n-----END RSA PRIVATE KEY-----"
    }
    keys_uri = f'{config.MIST_URL}/api/v2/keys'
    request = MistRequests(
        api_token=api_token, uri=keys_uri, json=create_key_request)
    response = request.post()
    assert_response_ok(response)
    key_id = response.json().get('id')
    # Get cloud id
    cloud_uri = f'{config.MIST_URL}/api/v2/clouds/{CLOUD_NAME}'
    request = MistRequests(
        api_token=api_token, uri=cloud_uri)
    response = request.get()
    assert_response_ok(response)
    cloud_id = response.json().get('data', {}).get('id', '')
    # Get image id
    image_name = 'debian-ssh'
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
        "key": key_id,
        "size": ''
    }
    machines_uri = f'{config.MIST_URL}/api/v1/clouds/{cloud_id}/machines'
    request = MistRequests(
        api_token=api_token, uri=machines_uri, json=add_machine_request)
    response = request.post()
    assert_response_ok(response)


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
    response = request.delete()
    assert_response_ok(response)
    # Remove the cloud
    uri = f'{config.MIST_URL}/api/v2/clouds/{CLOUD_NAME}'
    request = MistRequests(
        api_token=api_token, uri=uri)
    response = request.delete()
    assert_response_ok(response)
