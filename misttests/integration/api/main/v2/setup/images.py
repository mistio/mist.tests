from misttests.config import inject_vault_credentials
from misttests.config import MIST_URL
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.helpers import poll
from misttests.integration.api.mistrequests import MistRequests

CLOUDS_ENDPOINT = 'api/v2/clouds'
IMAGES_ENDPOINT = 'api/v2/images'


def setup(api_token):
    cloud_name = uniquify_string('test-cloud')
    add_cloud_request = {
        "name": cloud_name,
        "provider": "google",
        "credentials": {
            "projectId": None,
            "privateKey": None,
            "email": None
        },
    }
    inject_vault_credentials(add_cloud_request)
    clouds_uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=clouds_uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)
    # Wait until images are available
    assert poll(
        api_token=api_token,
        uri=f'{MIST_URL}/{IMAGES_ENDPOINT}',
        query_params=[('cloud', cloud_name)],
        data={'name': 'ubuntu'})
    setup_data = {
        'get_image': {
            'image': 'ubuntu'
        },
        'cloud': cloud_name
    }
    return setup_data


def teardown(api_token, setup_data):
    cloud = setup_data['cloud']
    clouds_uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}/{cloud}'
    request = MistRequests(api_token=api_token, uri=clouds_uri)
    request.delete()
