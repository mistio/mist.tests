from misttests.config import inject_vault_credentials
from misttests.config import MIST_URL
from misttests.integration.api.helpers import poll
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.mistrequests import MistRequests

CLOUDS_ENDPOINT = 'api/v2/clouds'
LOCATIONS_ENDPOINT = 'api/v2/locations'
AMAZON_LOCATION = 'ap-northeast-1a'


def setup(api_token):
    cloud_name = uniquify_string('test-cloud')
    volume_name = uniquify_string('test-volume')
    add_cloud_request = {
        "name": cloud_name,
        "provider": "amazon",
        "credentials": {
            "apikey": None,
            "apisecret": None,
            "region": None
        },
    }
    inject_vault_credentials(add_cloud_request)
    uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)
    # Wait for location to become available
    assert poll(
        api_token=api_token,
        uri=f'{MIST_URL}/{LOCATIONS_ENDPOINT}',
        query_params=[('cloud', cloud_name)],
        data={'name': AMAZON_LOCATION})
    test_args = {
        'create_volume': {
            'request_body': {
                'name': volume_name,
                'cloud': cloud_name,
                'location': AMAZON_LOCATION,
                'size': 1,
                'ex_volume_type': 'standard',
                'ex_iops': ''
            }
        },
        'edit_volume': {
            'query_string': [('name', volume_name)]
        }
    }
    setup_data = dict(**test_args, cloud=cloud_name, volume=volume_name)
    return setup_data


def teardown(api_token, setup_data):
    cloud_name = setup_data['cloud']
    uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}/{cloud_name}'
    request = MistRequests(api_token=api_token, uri=uri)
    request.delete()
