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
    test_args = {
        'create_network': {
            'request_body': {
                'name': network_name,
                'cloud': cloud_name,
                'extra': {
                    'cidr': f'10.{randint(1, 255 + 1)}.0.0/16'
                }
            }
        },
        'edit_network': {
            'network': network_name,
            'query_string': [('name', network_name)]
        },
        'delete_network': {
            'network': network_name,
            'query_string': [('cloud', cloud_name)]
        }
    }
    setup_data = dict(**test_args, cloud=cloud_name, network=network_name)
    return setup_data


def teardown(api_token, setup_data):
    cloud_name = setup_data['cloud']
    uri = f'{config.MIST_URL}/{CLOUDS_ENDPOINT}/{cloud_name}'
    request = MistRequests(
        api_token=api_token, uri=uri)
    request.delete()
