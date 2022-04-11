from requests import codes
from functools import partial
from datetime import datetime, timedelta

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
    'associate_key',
    'ssh',
    'disassociate_key',
    'edit_machine',
    'rename_machine',
    'get_machine',
    'list_machines',
    'clone_machine',
    'console',
    'suspend_machine',
    'resume_machine',
    'destroy_machine',
    'undefine_machine',
]

AMAZON_PROVIDER = 'amazon'
AMAZON_IMAGE = 'ubuntu'
AMAZON_SIZE = 'nano'
KVM_PROVIDER = 'kvm'
KVM_IMAGE = 'cirros-0.5.1-x86_64-disk.img'
V2_ENDPOINT = 'api/v2'
CLOUDS_ENDPOINT = f'{V2_ENDPOINT}/clouds'
KEYS_ENDPOINT = f'{V2_ENDPOINT}/keys'
IMAGES_ENDPOINT = f'{V2_ENDPOINT}/images'
LOCATIONS_ENDPOINT = f'{V2_ENDPOINT}/locations'
SIZES_ENDPOINT = f'{V2_ENDPOINT}/sizes'
MACHINES_ENDPOINT = f'{V2_ENDPOINT}/machines'


def setup(api_token):
    amazon_cloud_name = uniquify_string('test-cloud')
    kvm_cloud_name = uniquify_string('test-cloud')
    add_amazon_cloud_request = {
        'name': amazon_cloud_name,
        'provider': AMAZON_PROVIDER,
        'credentials': {
            'apikey': None,
            'apisecret': None,
            'region': None
        },
    }
    kvm_host = safe_get_var(
        f'clouds/{KVM_PROVIDER}', 'hostname')
    add_kvm_cloud_request = {
        'name': kvm_cloud_name,
        'provider': 'kvm',
        'credentials': {
            'hosts': [{
                'host': kvm_host,
                'key': None
            }]
        }
    }
    clouds_uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}'
    # Add amazon cloud
    inject_vault_credentials(add_amazon_cloud_request)
    request = MistRequests(
        api_token=api_token, uri=clouds_uri, json=add_amazon_cloud_request)
    response = request.post()
    assert_response_ok(response)
    # Add kvm cloud
    kvm_private_key = safe_get_var(
        f'clouds/{KVM_PROVIDER}', 'key')
    key_name = uniquify_string('test-key')
    add_key_request = {
        'name': key_name,
        'private': kvm_private_key
    }
    keys_uri = f'{MIST_URL}/{KEYS_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=keys_uri, json=add_key_request)
    response = request.post()
    assert_response_ok(response)
    kvm_key_id = response.json().get('id')
    add_kvm_cloud_request['credentials']['hosts'][0]['key'] = kvm_key_id
    request = MistRequests(
        api_token=api_token, uri=clouds_uri, json=add_kvm_cloud_request)
    response = request.post()
    assert_response_ok(response)
    # Wait for kvm cloud to become available
    assert poll(api_token=api_token, uri=f'{clouds_uri}/{kvm_cloud_name}')
    # Wait until amazon image is available
    assert poll(
        api_token=api_token,
        uri=f'{MIST_URL}/{IMAGES_ENDPOINT}',
        query_params=[('cloud', amazon_cloud_name)],
        data={'name': AMAZON_IMAGE})
    # Wait until amazon size is available
    assert poll(
        api_token=api_token,
        uri=f'{MIST_URL}/{SIZES_ENDPOINT}',
        query_params=[('cloud', amazon_cloud_name), ('limit', 500)],
        data={'name': AMAZON_SIZE})
    # Wait until kvm image is available
    assert poll(
        api_token=api_token,
        uri=f'{MIST_URL}/{IMAGES_ENDPOINT}',
        query_params=[('cloud', kvm_cloud_name)],
        data={'name': KVM_IMAGE},
        timeout=800)
    # Wait for kvm locations to become available
    assert poll(api_token=api_token,
                uri=f'{MIST_URL}/{LOCATIONS_ENDPOINT}',
                query_params=[('cloud', kvm_cloud_name)],
                timeout=800)
    # Create kvm machine
    kvm_machine_name = uniquify_string('test-machine')
    create_kvm_machine_request = {
        'name': kvm_machine_name,
        'provider': KVM_PROVIDER,
        'cloud': kvm_cloud_name,
        'key': key_name,
        'image': KVM_IMAGE,
        'size': {'memory': 256, 'cpu': 1},
        'disks': {
            'disk_path': f'/var/lib/libvirt/images/{kvm_machine_name}.img',
            'disk_size': 4
        },
        'dry': False
    }
    machines_uri = f'{MIST_URL}/{MACHINES_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=machines_uri, json=create_kvm_machine_request)
    response = request.post()
    assert_response_ok(response)
    amazon_machine_name = uniquify_string('test-machine')
    amazon_machine_uri = f'{machines_uri}/{amazon_machine_name}'
    dt = datetime.now() + timedelta(hours=1)
    edit_machine_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    clone_machine_name = kvm_machine_name + '-clone'
    clone_machine_uri = f'{machines_uri}/{clone_machine_name}'
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
            'callback': partial(
                poll,
                api_token=api_token,
                uri=amazon_machine_uri,
                data={'state': 'running'},
                timeout=800,
                post_delay=10)
        },
        'reboot_machine': {
            'machine': amazon_machine_name,
            'callback': partial(
                poll,
                api_token=api_token,
                uri=amazon_machine_uri,
                data={'state': 'running'},
                timeout=800,
                post_delay=10)
        },
        'stop_machine': {
            'machine': amazon_machine_name,
            'callback': partial(
                poll,
                api_token=api_token,
                uri=amazon_machine_uri,
                timeout=800,
                data={'state': 'stopped'})
        },
        'start_machine': {
            'machine': amazon_machine_name,
            'callback': partial(
                poll,
                api_token=api_token,
                uri=amazon_machine_uri,
                data={'state': 'running'},
                timeout=800,
                post_delay=10)
        },
        'associate_key': {
            'request_body': {'key': key_name},
            'machine': amazon_machine_name,
        },
        'disassociate_key': {
            'request_body': {'key': key_name},
            'machine': amazon_machine_name,
        },
        'ssh': {'machine': amazon_machine_name},
        'resize_machine': {
            'query_string': [('size', AMAZON_SIZE)],
            'machine': amazon_machine_name
        },
        'edit_machine': {
            'machine': amazon_machine_name,
            'request_body': {
                'expiration': {
                    'date': edit_machine_date,
                    'action': 'destroy',
                    'notify': 0
                }
            }
        },
        'get_machine': {
            'machine': amazon_machine_name,
        },
        'rename_machine': {
            'machine': amazon_machine_name,
            'query_string': [('name', amazon_machine_name)],
            'callback': partial(
                poll,
                api_token=api_token,
                uri=f'{MIST_URL}/{MACHINES_ENDPOINT}/{kvm_machine_name}',
                data={'state': 'running'},
                timeout=800)
        },
        'clone_machine': {
            'machine': kvm_machine_name,
            'query_string': [
                ('name', clone_machine_name),
                ('run_async', False)],
            'callback': partial(
                poll,
                api_token=api_token,
                uri=clone_machine_uri,
                timeout=800)
        },
        'suspend_machine': {
            'machine': clone_machine_name,
            'callback': partial(
                poll,
                api_token=api_token,
                uri=clone_machine_uri,
                data={'state': 'suspended'},
                timeout=800)
        },
        'resume_machine': {
            'machine': clone_machine_name,
            'callback': partial(
                poll,
                api_token=api_token,
                uri=clone_machine_uri,
                data={'state': 'running'},
                timeout=800,
                post_delay=10)
        },
        'destroy_machine': {
            'machine': clone_machine_name,
            'callback': partial(
                poll,
                api_token=api_token,
                uri=clone_machine_uri,
                data={'state': 'terminated'},
                timeout=800,
                post_delay=10)
        },
        'console': {'machine': clone_machine_name},
        'undefine_machine': {'machine': clone_machine_name}
    }
    setup_data = dict(**test_args,
                      amazon_cloud=amazon_cloud_name,
                      kvm_cloud=kvm_cloud_name,
                      kvm_machine=kvm_machine_name,
                      key=key_name)
    return setup_data


def teardown(api_token, setup_data):
    # Destroy amazon machine
    machine_name = setup_data['create_machine']['request_body']['name']
    uri = (f'{MIST_URL}/{MACHINES_ENDPOINT}'
           f'/{machine_name}/actions/destroy')
    request = MistRequests(api_token=api_token, uri=uri)
    request.post()
    # Destroy kvm machine
    machine_name = setup_data['kvm_machine']
    uri = (f'{MIST_URL}/{MACHINES_ENDPOINT}'
           f'/{machine_name}/actions/destroy')
    request = MistRequests(api_token=api_token, uri=uri)
    response = request.post()
    if response.status_code == codes.ok:
        machine_uri = f'{MIST_URL}/{MACHINES_ENDPOINT}/{machine_name}'
        poll(api_token=api_token,
             uri=machine_uri,
             data={'state': 'terminated'})
    # Undefine kvm machine
    uri = (f'{MIST_URL}/{MACHINES_ENDPOINT}'
           f'/{machine_name}/actions/undefine')
    request = MistRequests(api_token=api_token, uri=uri)
    request.post()
    # Delete key
    key_name = setup_data['key']
    uri = f'{MIST_URL}/{KEYS_ENDPOINT}/{key_name}'
    request = MistRequests(api_token=api_token, uri=uri)
    request.delete()
    # Remove amazon cloud
    amazon_cloud_name = setup_data['amazon_cloud']
    uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}/{amazon_cloud_name}'
    request = MistRequests(api_token=api_token, uri=uri)
    request.delete()
    # Remove amazon cloud
    kvm_cloud_name = setup_data['kvm_cloud']
    uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}/{kvm_cloud_name}'
    request = MistRequests(api_token=api_token, uri=uri)
    request.delete()
