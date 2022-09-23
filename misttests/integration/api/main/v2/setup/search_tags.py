from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.mistrequests import MistRequests
from misttests.config import MIST_URL
from misttests.integration.api.utils import assert_equal
from misttests.integration.api.utils import assert_response_not_found


V2_ENDPOINT = 'api/v2'
KEYS_ENDPOINT = f'{V2_ENDPOINT}/keys'
TAGS_ENDPOINT = f'{V2_ENDPOINT}/tags'
KEYS_URI = f'{MIST_URL}/{KEYS_ENDPOINT}'
TAGS_URI = f'{MIST_URL}/{TAGS_ENDPOINT}'
N_KEYS = 10
N_TAGGED = 4
KEY_NAMES = N_TAGGED*['tagged-key'] + (N_KEYS - N_TAGGED)*['key']
SLEEP = 3


def setup(api_token):

    # Add keys
    setup_data = {
        'keys': [], 'tagged': [],
        'tag_request': {
            "operations": [
                {
                    "operation": "add",
                    "resources": [],
                    "tags": [{
                        "key": "dev",
                        "value": "value1"
                        }]
                }
            ]
        }
    }
    setup_data['N_KEYS'] = N_KEYS

    for key_name in KEY_NAMES:
        key_name = uniquify_string(key_name)
        add_key_request = {
            'name': key_name,
            'generate': True
        }

        request = MistRequests(
            api_token=api_token, uri=KEYS_URI, json=add_key_request)
        response = request.post()
        assert_response_ok(response)

        key_id = response.json()['id']
        setup_data['keys'].append((key_name, key_id))

        if 'tagged-key' in key_name:

            setup_data['tag_request']['operations'][0]['resources'].append({
                'resource_type': 'keys', 'resource_id': key_id})

            setup_data['tagged'].append({'id': key_id})

    # Check if the keys were created
    query_string = [('only', 'id')]

    response = MistRequests(
        api_token=api_token,
        uri=KEYS_URI,
        params=query_string).get()
    assert_response_ok(response)

    assert_equal(response.json()['meta']['total'], setup_data['N_KEYS'])

    setup_data['tag_keys'] = {'sleep': SLEEP}
    setup_data['untag_keys'] = {'sleep': SLEEP}

    return setup_data


def teardown(api_token, setup_data):
    for _, key_id in setup_data['keys']:
        uri = f'{KEYS_URI}/{key_id}'
        request = MistRequests(api_token=api_token, uri=uri)
        response = request.delete()

        assert_response_ok(response)
        assert_response_not_found(request.get())
