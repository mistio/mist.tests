from datetime import datetime, timedelta
from time import sleep
from time import time
from misttests import config
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import uniquify_string
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

KVM_PROVIDER = 'kvm'
KVM_IMAGE = 'cirros-0.5.1-x86_64-disk.img'
V2_ENDPOINT = 'api/v2'
CLOUDS_ENDPOINT = f'{V2_ENDPOINT}/clouds'
KEYS_ENDPOINT = f'{V2_ENDPOINT}/keys'
IMAGES_ENDPOINT = f'{V2_ENDPOINT}/images'
MACHINES_ENDPOINT = f'{V2_ENDPOINT}/machines'


def setup(api_token):
    amazon_cloud_name = uniquify_string('test-cloud')
    kvm_cloud_name = uniquify_string('test-cloud')
    add_amazon_cloud_request = {
        'name': amazon_cloud_name,
        'provider': 'amazon',
        'credentials': {
            'apikey': None,
            'apisecret': None,
            'region': None
        },
    }
    kvm_host = config.safe_get_var(
        f'clouds_new/{KVM_PROVIDER}', 'hostname')
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
    clouds_uri = f'{config.MIST_URL}/{CLOUDS_ENDPOINT}'
    # Add amazon cloud
    config.inject_vault_credentials(add_amazon_cloud_request)
    request = MistRequests(
        api_token=api_token, uri=clouds_uri, json=add_amazon_cloud_request)
    response = request.post()
    assert_response_ok(response)
    # Add kvm cloud
    kvm_private_key = config.safe_get_var(
        f'clouds_new/{KVM_PROVIDER}', 'key')
    key_name = uniquify_string('test-key')
    add_key_request = {
        'name': key_name,
        'private': kvm_private_key
    }
    keys_uri = f'{config.MIST_URL}/{KEYS_ENDPOINT}'
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
    # Wait until kvm image is available
    image_uri = f'{config.MIST_URL}/{IMAGES_ENDPOINT}'
    request = MistRequests(
        api_token=api_token,
        uri=image_uri,
        params=[('cloud', kvm_cloud_name)])
    minutes = 5
    t_end = time() + 60 * minutes

    def find_value(data, key, value):
        for d in data:
            if d[key] == value:
                return True
        return False
    while time() < t_end:
        response = request.get()
        assert_response_ok(response)
        data, key, value = response.json()['data'], 'name', KVM_IMAGE
        if find_value(data, key, value):
            break
        sleep(5)
    # Create kvm machine
    kvm_machine_name = uniquify_string('test-machine')
    create_kvm_machine_request = {
        'name': kvm_machine_name,
        'provider': KVM_PROVIDER,
        'cloud': kvm_cloud_name,
        'key': key_name,
        'image': KVM_IMAGE,
        'size': {
            'ram': 256,
            'cpus': 1
        },
        'disks': {
            'disk_path': f'/var/lib/libvirt/images/{kvm_machine_name}.img',
            'disk_size': 4
        },
        'dry': False
    }
    machines_uri = f'{config.MIST_URL}/{MACHINES_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=machines_uri, json=create_kvm_machine_request)
    response = request.post()
    assert_response_ok(response)
    sleep(60)
    amazon_machine_name = uniquify_string('test-machine')
    create_machine = {
        'request_body': {
            'name': amazon_machine_name,
            'provider': 'amazon',
            'cloud': amazon_cloud_name,
            'image': 'ubuntu',
            'size': 'micro',
            'dry': False
        },
        'sleep': 60
    }
    reboot_machine = stop_machine = start_machine = {
        'machine': amazon_machine_name,
        'sleep': 60
    }
    associate_key = disassociate_key = {
        'request_body': {'key': key_name},
        'machine': amazon_machine_name,
    }
    ssh = {'machine': amazon_machine_name}
    resize_machine = {
        'query_string': [('size', 'micro')],
        'machine': amazon_machine_name
    }
    dt = datetime.now() + timedelta(hours=1)
    edit_machine = {
        'machine': amazon_machine_name,
        'request_body': {
            'expiration': {
                'date': dt.strftime('%Y-%m-%d %H:%M:%S'),
                'action': 'destroy',
                'notify': 0
            }
        }
    }
    rename_machine = {
        'machine': amazon_machine_name,
        'query_string': [('name', amazon_machine_name)],
    }
    return dict(create_machine=create_machine,
                reboot_machine=reboot_machine,
                stop_machine=stop_machine,
                resize_machine=resize_machine,
                start_machine=start_machine,
                associate_key=associate_key,
                ssh=ssh,
                disassociate_key=disassociate_key,
                edit_machine=edit_machine,
                rename_machine=rename_machine,
                amazon_cloud=amazon_cloud_name,
                kvm_cloud=kvm_cloud_name,
                machine=kvm_machine_name,
                key=key_name)


def teardown(api_token, setup_data):
    # Destroy machine
    machine_name = setup_data['create_machine']['request_body']['name']
    uri = (f'{config.MIST_URL}/{MACHINES_ENDPOINT}'
           f'/{machine_name}/actions/destroy')
    request = MistRequests(api_token=api_token, uri=uri)
    request.post()
    # Delete key
    key_name = setup_data['key']
    uri = f'{config.MIST_URL}/{KEYS_ENDPOINT}/{key_name}'
    request = MistRequests(api_token=api_token, uri=uri)
    request.delete()
    # Remove amazon cloud
    amazon_cloud_name = setup_data['amazon_cloud']
    uri = f'{config.MIST_URL}/{CLOUDS_ENDPOINT}/{amazon_cloud_name}'
    request = MistRequests(api_token=api_token, uri=uri)
    request.delete()
    # Remove amazon cloud
    kvm_cloud_name = setup_data['kvm_cloud']
    uri = f'{config.MIST_URL}/{CLOUDS_ENDPOINT}/{kvm_cloud_name}'
    request = MistRequests(api_token=api_token, uri=uri)
    request.delete()
