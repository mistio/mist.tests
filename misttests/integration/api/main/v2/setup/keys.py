from misttests import config
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.mistrequests import MistRequests

CLOUDS_ENDPOINT = 'api/v2/clouds'


def setup(api_token):
    cloud_name = uniquify_string('test-cloud')
    add_cloud_request = {
        'name': cloud_name,
        'provider': 'google',
        'credentials': {
            'projectId': None,
            'privateKey': None,
            'email': None
        },
    }
    config.inject_vault_credentials(add_cloud_request)
    uri = f'{config.MIST_URL}/{CLOUDS_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)
    key_name = uniquify_string('test-key')
    test_args = {
        'add_key': {'request_body': {'name': key_name, 'generate': True}},
        'edit_key': {'key': key_name, 'query_string': [('name', key_name)]},
        'delete_key': {'key': key_name}
    }
    setup_data = dict(**test_args, cloud=cloud_name, key=key_name)
    return setup_data


def teardown(api_token, setup_data):
    cloud_name = setup_data['cloud']
    uri = f'{config.MIST_URL}/{CLOUDS_ENDPOINT}/{cloud_name}'
    request = MistRequests(api_token=api_token, uri=uri)
    request.delete()
