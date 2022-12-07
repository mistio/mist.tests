from misttests.config import inject_vault_credentials
from misttests.config import MIST_URL
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.mistrequests import MistRequests

TEST_METHOD_ORDERING = [
    'create_zone',
    'create_record',
    'get_record',
    'list_records',
    'delete_record',
    'edit_zone',
    'get_zone',
    'list_zones',
    'delete_zone',
]

CLOUDS_ENDPOINT = 'api/v2/clouds'
RECORD_VALUE = '123.23.23.2'


def setup(api_token):
    cloud = uniquify_string('test-cloud')
    zone = uniquify_string('test-zone') + '.com'
    record = uniquify_string('test-record')
    add_cloud_request = {
        'name': cloud,
        'provider': 'google',
        'credentials': {
            'projectId': 'test',
            'privateKey': 'key',
            'email': 'email'
        },
        'features': {
            'compute': True,
            'dns': True
        }
    }
    inject_vault_credentials(add_cloud_request)
    uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)
    test_args = {
        'create_zone': {
            'request_body': {
                'name': zone,
                'cloud': cloud,
                'type': 'master',
                'ttl': '0'
            }
        },
        'create_record': {
            'request_body': {
                'name': record,
                'value': RECORD_VALUE,
            }
        },
        'get_record': {
            'query_string': [('', '')]
        },
        'list_records': {
            'query_string': [('', '')]
        },
        'delete_record': {
            'query_string': [('', '')]
        },
    }
    setup_data = dict(**test_args,
                      cloud=cloud,
                      zone=zone,
                      record=record,)
    return setup_data


def teardown(api_token, setup_data):
    cloud = setup_data['cloud']
    uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}/{cloud}'
    request = MistRequests(
        api_token=api_token, uri=uri)
    request.delete()
