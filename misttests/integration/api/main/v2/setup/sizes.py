from misttests.config import inject_vault_credentials
from misttests.config import MIST_URL
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.helpers import poll
from misttests.integration.api.mistrequests import MistRequests

V2_ENDPOINT = 'api/v2'
CLOUDS_ENDPOINT = 'api/v2/clouds'
SIZES_ENDPOINT = f'{V2_ENDPOINT}/sizes'


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
    inject_vault_credentials(add_cloud_request)
    uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)
    # Wait until sizes are available
    assert poll(
        api_token=api_token,
        uri=f'{MIST_URL}/{SIZES_ENDPOINT}',
        query_params=[('cloud', cloud_name)],
        data={'name': 'medium'})
    setup_data = {
        'size': 'medium',
        'cloud': cloud_name
    }
    return setup_data


def teardown(api_token, setup_data):
    cloud_name = setup_data['cloud']
    uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}/{cloud_name}'
    request = MistRequests(api_token=api_token, uri=uri)
    request.delete()
