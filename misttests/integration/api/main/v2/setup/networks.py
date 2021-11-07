from random import randint
from misttests import config
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.mistrequests import MistRequests

CLOUDS_ENDPOINT = 'api/v2/clouds'


def setup(api_token):
    cloud_name = uniquify_string('test-cloud')
    network_name = uniquify_string('test-network')
    add_cloud_request = {
        'name': cloud_name,
        'provider': 'amazon',
        'credentials': {
            'apikey': None,
            'apisecret': None,
            'region': None
        },
    }
    config.inject_vault_credentials(add_cloud_request)
    uri = f'{config.MIST_URL}/{CLOUDS_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)
    request_body = {
        'name': network_name,
        'cloud': cloud_name,
        'extra': {
            'cidr': f'10.{randint(1, 255 + 1)}.0.0/16'
        }
    }
    query_string = {
        'delete_network': [('cloud', cloud_name)],
        'edit_network': [('name', network_name)]
    }
    return dict(overwrite_request=request_body,
                query_string=query_string,
                cloud=cloud_name,
                network=network_name)


def teardown(api_token, setup_data):
    cloud_name = setup_data['cloud']
    uri = f'{config.MIST_URL}/{CLOUDS_ENDPOINT}/{cloud_name}'
    request = MistRequests(
        api_token=api_token, uri=uri)
    request.delete()
