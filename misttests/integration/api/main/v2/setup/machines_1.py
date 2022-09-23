from misttests.config import inject_vault_credentials
from misttests.config import MIST_URL
from misttests.config import safe_get_var
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.helpers import poll
from misttests.integration.api.mistrequests import MistRequests

# This variable is used by the machines test module. It must contain a list of
# all the machines test methods in the specific order in which they should be
# run.
TEST_METHOD_ORDERING = [
    'create_machine',
    'reboot_machine',
    'stop_machine',
    'resize_machine',
    'start_machine',
]

DEFAULT_TIMEOUT = 600
KVM_PROVIDER = 'kvm'
AMAZON_PROVIDER = 'amazon'
AMAZON_IMAGE = 'ubuntu'
AMAZON_SIZE = 'nano'
V2_ENDPOINT = 'api/v2'
CLOUDS_ENDPOINT = f'{V2_ENDPOINT}/clouds'
CLOUDS_URI = f'{MIST_URL}/{CLOUDS_ENDPOINT}'
KEYS_ENDPOINT = f'{V2_ENDPOINT}/keys'
KEYS_URI = f'{MIST_URL}/{KEYS_ENDPOINT}'
IMAGES_ENDPOINT = f'{V2_ENDPOINT}/images'
IMAGES_URI = f'{MIST_URL}/{IMAGES_ENDPOINT}'
LOCATIONS_ENDPOINT = f'{V2_ENDPOINT}/locations'
SIZES_ENDPOINT = f'{V2_ENDPOINT}/sizes'
SIZES_URI = f'{MIST_URL}/{SIZES_ENDPOINT}'
MACHINES_ENDPOINT = f'{V2_ENDPOINT}/machines'
MACHINES_URI = f'{MIST_URL}/{MACHINES_ENDPOINT}'


def setup(api_token):
    amazon_cloud_name = uniquify_string('test-cloud')
    add_amazon_cloud_request = {
        'name': amazon_cloud_name,
        'provider': AMAZON_PROVIDER,
        'credentials': {
            'apikey': None,
            'apisecret': None,
            'region': None
        },
    }
    # Add amazon cloud
    inject_vault_credentials(add_amazon_cloud_request)
    request = MistRequests(
        api_token=api_token, uri=CLOUDS_URI, json=add_amazon_cloud_request)
    response = request.post()
    assert_response_ok(response)
    key_name = uniquify_string('test-key')
    kvm_private_key = safe_get_var(f'clouds/{KVM_PROVIDER}', 'key')
    add_key_request = {
        'name': key_name,
        'private': kvm_private_key
    }
    request = MistRequests(
        api_token=api_token,
        uri=KEYS_URI,
        json=add_key_request)
    response = request.post()
    assert_response_ok(response)
    # Wait until amazon image is available
    assert poll(
        api_token=api_token,
        uri=IMAGES_URI,
        query_params=[('cloud', amazon_cloud_name)],
        data={'name': AMAZON_IMAGE})
    # Wait until amazon size is available
    assert poll(
        api_token=api_token,
        uri=SIZES_URI,
        query_params=[('cloud', amazon_cloud_name), ('limit', 500)],
        data={'name': AMAZON_SIZE})
    amazon_machine_name = uniquify_string('test-machine')
    amazon_machine_uri = f'{MACHINES_URI}/{amazon_machine_name}'
    test_args = {
        'create_machine': {
            'request_body': {
                'name': amazon_machine_name,
                'provider': AMAZON_PROVIDER,
                'cloud': amazon_cloud_name,
                'image': AMAZON_IMAGE,
                'size': AMAZON_SIZE,
                'dry': False
            },
        },
        'reboot_machine': {'machine': amazon_machine_name},
        'stop_machine': {'machine': amazon_machine_name},
        'resize_machine': {
            'query_string': [('size', AMAZON_SIZE)],
            'machine': amazon_machine_name
        },
        'start_machine': {'machine': amazon_machine_name},
    }
    setup_data = dict(**test_args,
                      amazon_machine_uri=amazon_machine_uri,
                      amazon_cloud=amazon_cloud_name,
                      key=key_name)
    return setup_data


def teardown(api_token, setup_data):
    # Destroy amazon machine
    machine_name = setup_data['create_machine']['request_body']['name']
    uri = f'{MACHINES_URI}/{machine_name}/actions/destroy'
    request = MistRequests(api_token=api_token, uri=uri)
    request.post()
    # Delete key
    key_name = setup_data['key']
    uri = f'{KEYS_URI}/{key_name}'
    request = MistRequests(api_token=api_token, uri=uri)
    request.delete()
    # Remove amazon cloud
    amazon_cloud_name = setup_data['amazon_cloud']
    uri = f'{CLOUDS_URI}/{amazon_cloud_name}'
    request = MistRequests(api_token=api_token, uri=uri)
    request.delete()
