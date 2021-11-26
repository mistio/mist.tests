from misttests.config import inject_vault_credentials
from misttests.config import MIST_URL
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.mistrequests import MistRequests

CLOUDS_ENDPOINT = 'api/v2/clouds'


def setup(api_token):
    cloud_name = uniquify_string('test-cloud')
    zone_name = uniquify_string('test-zone') + '.com'
    add_cloud_request = {
        'name': cloud_name,
        'provider': 'google',
        'credentials': {
            'projectId': None,
            'privateKey': None,
            'email': None
        },
    }
    inject_vault_credentials(add_cloud_request)
    uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)
    create_zone = {
        'request_body': {
            'name': zone_name,
            'cloud': cloud_name,
            'type': 'master',
            'ttl': '0'
        }
    }
    setup_data = dict(create_zone=create_zone,
                      cloud=cloud_name,
                      zone=zone_name)
    return setup_data


def teardown(api_token, setup_data):
    cloud_name = setup_data['cloud']
    uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}/{cloud_name}'
    request = MistRequests(
        api_token=api_token, uri=uri)
    request.delete()
