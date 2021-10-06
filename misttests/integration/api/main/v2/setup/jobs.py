from time import sleep
from misttests import config
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.mistrequests import MistRequests


def setup(api_token):
    # Add a cloud
    add_cloud_request = {
        "name": "example-cloud",
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
        "name": "example-key",
        "private": "-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQCqGKukO1De7zhZj6+H0qtjTkVxwTCpvKe4eCZ0FPqri0cb2JZfXJ/DgYSF6vUp wmJG8wVQZKjeGcjDOL5UlsuusFncCzWBQ7RKNUSesmQRMSGkVb1/3j+skZ6UtW+5u09lHNsj6tQ5 1s1SPrCBkedbNf0Tp0GbMJDyR4e9T04ZZwIDAQABAoGAFijko56+qGyN8M0RVyaRAXz++xTqHBLh 3tx4VgMtrQ+WEgCjhoTwo23KMBAuJGSYnRmoBZM3lMfTKevIkAidPExvYCdm5dYq3XToLkkLv5L2 pIIVOFMDG+KESnAFV7l2c+cnzRMW0+b6f8mR1CJzZuxVLL6Q02fvLi55/mbSYxECQQDeAw6fiIQX GukBI4eMZZt4nscy2o12KyYner3VpoeE+Np2q+Z3pvAMd/aNzQ/W9WaI+NRfcxUJrmfPwIGm63il AkEAxCL5HQb2bQr4ByorcMWm/hEP2MZzROV73yF41hPsRC9m66KrheO9HPTJuo3/9s5p+sqGxOlF L0NDt4SkosjgGwJAFklyR1uZ/wPJjj611cdBcztlPdqoxssQGnh85BzCj/u3WqBpE2vjvyyvyI5k X6zk7S0ljKtt2jny2+00VsBerQJBAJGC1Mg5Oydo5NwD6BiROrPxGo2bpTbu/fhrT8ebHkTz2epl U9VQQSQzY1oZMVX8i1m5WUTLPz2yLJIBQVdXqhMCQBGoiuSoSjafUhV7i1cEGpb88h5NBYZzWXGZ 37sJ5QsW+sJyoNde3xH8vdXhzU7eT82D6X/scw9RZz+/6rCJ4p0=\n-----END RSA PRIVATE KEY-----"
    }
    config.inject_vault_credentials(add_key_request)
    uri = config.MIST_URL + '/api/v2/keys'
    request = MistRequests(
        api_token=api_token,
        uri=uri,
        json=add_key_request)
    request_method = getattr(request, 'POST'.lower())
    response = request_method()
    assert_response_ok(response)
    sleep(200)
    # Create a machine
    add_machine_request = {
        "name": "example-machine",
        "provider": "google",
        "cloud": "example-cloud",
        "location": "us-east1-b",
        "image": "ubuntu-1804-bionic-v20210928",
        "size": "f1-micro",
        "key": "example-key",
        "dry": False
    }
    uri = config.MIST_URL + '/api/v2/machines'
    request = MistRequests(
        api_token=api_token, uri=uri, json=add_machine_request)
    response = request.post()
    assert_response_ok(response)
    job_id = response.json().get('jobId') or response.json().get('job_id')
    sleep(60)
    return {'job_id': job_id}


def teardown(api_token):
    # Destroy the machine
    uri = config.MIST_URL + '/api/v2/machines/example-machine/actions/destroy'
    request = MistRequests(api_token=api_token, uri=uri)
    response = request.post()
    assert_response_ok(response)
    # Delete key
    uri = config.MIST_URL + '/api/v2/keys/example-key'
    request = MistRequests(api_token=api_token, uri=uri)
    request_method = getattr(request, 'DELETE'.lower())
    response = request_method()
    assert_response_ok(response)
    # Remove the cloud
    uri = config.MIST_URL + '/api/v2/clouds/example-cloud'
    request = MistRequests(
        api_token=api_token, uri=uri)
    response = request.delete()
    assert_response_ok(response)
