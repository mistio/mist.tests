from misttests import config
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.mistrequests import MistRequests

CLOUDS_ENDPOINT = 'api/v2/clouds'


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
    config.inject_vault_credentials(add_cloud_request)
    uri = f'{config.MIST_URL}/{CLOUDS_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)
    request_body = {
        'name': volume_name,
        'cloud': cloud_name,
        'location': 'ap-northeast-1a',
        'size': 1,
        'ex_volume_type': 'standard',
        'ex_iops': ''
    }
    query_string = {
        'edit_volume': [('name', volume_name)]
    }
    return dict(overwrite_request=request_body,
                query_string=query_string,
                cloud=cloud_name,
                volume=volume_name)


def teardown(api_token, setup_data):
    cloud_name = setup_data['cloud']
    uri = f'{config.MIST_URL}/{CLOUDS_ENDPOINT}/{cloud_name}'
    request = MistRequests(api_token=api_token, uri=uri)
    request.delete()
