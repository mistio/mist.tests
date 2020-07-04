from misttests.integration.api.utils import assert_response_ok, assert_list_not_empty
from misttests.integration.api.utils import assert_response_unauthorized
from misttests.integration.api.utils import assert_response_not_found
from misttests.integration.api.utils import assert_response_bad_request
from misttests.integration.api.utils import assert_is_instance
from misttests.integration.api.utils import assert_list_empty
from misttests.config import safe_get_var
from misttests import config

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################

def test_add_vsphere_cloud(pretty_print, mist_core, cache, owner_api_token, name='VSphere'):
    response = mist_core.add_cloud(name, provider='vsphere', api_token=owner_api_token,
                                   host=safe_get_var('clouds/vsphere-7', 'host'),
                                   username=safe_get_var('clouds/vsphere-7', 'username'),
                                   password=safe_get_var('clouds/vsphere-7', 'password'),
                                   ca_cert_file=safe_get_var('clouds/vsphere-7', 'ca')
                                   ).post()
    assert_response_ok(response)
    cache.set('vsphere_cloud_id', response.json()['id'])
    print("Success, VSphere cloud added!")

def test_add_kubevirt_cloud(pretty_print, mist_core, cache, owner_api_token, name="Kubevirt"):
    response = mist_core.add_cloud(name, provider='kubevirt', api_token=owner_api_token,
                                   host=safe_get_var('clouds/kubevirt', 'host'),
                                   authentication='tokenbearer',
                                   token=safe_get_var('clouds/kubevirt', 'token'),
                                   ca_cert_file=safe_get_var('clouds/kubevirt', 'ca')
                                   ).post()
    assert_response_ok(response)
    cache.set('kubevirt_cloud_id', response.json()['id'])
    print("Success, Kubevirt added!")

def test_add_packet_cloud(pretty_print, mist_core, cache, owner_api_token, name="Packet"):
    response = mist_core.add_cloud(name, provider='packet', api_token=owner_api_token,
                                   apikey=safe_get_var('clouds/packet', 'api_key')
                                   ).post()
    assert_response_ok(response)
    cache.set('packet_cloud_id', response.json()['id'])
    print("Success, Packet added!")

def test_add_kvm_cloud(pretty_print, mist_core, cache, owner_api_token, name="KVM"):
    response = mist_core.add_cloud(name, provider='libvirt', api_token=owner_api_token,
                                   machine_hostname=safe_get_var('clouds/other_server', 'host'),
                                   machine_user="root",
                                   machine_key=safe_get_var('clouds/other_server', 'key'),
                                   images_location='/var/lib/libvirt/images',
                                   ssh_port=22).post()
    assert_response_ok(response)
    cache.set('kvm_cloud_id', response.json()['id'])
    print("Success, KVM added!")

# Proper
def test_list_datastores(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = cache.get('vsphere_cloud_id', '')
    print("YOO here!!", cloud_id)
    response = mist_core.list_datastores(cloud_id=cloud_id, api_token=owner_api_token)
    print("YOO there!!", response)
    assert_response_ok(response)
    assert_list_not_empty(response.json())
    print("Success, list_datastores functions just fine.")

def test_list_datastores_wrong_token(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = cache.get('vsphere_cloud_id', '')
    response = mist_core.list_datastores(cloud_id=cloud_id, api_token="123Boom!")
    assert_response_unauthorized(response)
    print('Success')

def test_list_datastores_wrong_cloud(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = cache.get('kubevirt_cloud_id', '')
    response = mist_core.list_datastores(cloud_id=cloud_id, api_token=owner_api_token)
    assert_response_not_found(response)
    print('Success')

def test_list_datastores_inexistent_cloud(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = "not_a_cloud"
    response = mist_core.list_datastores(cloud_id=cloud_id, api_token=owner_api_token)
    assert_response_bad_request(response)
    print('Success')

def test_list_folders(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = cache.get('vsphere_cloud_id', '')
    response = mist_core.list_folders(cloud_id=cloud_id, api_token=owner_api_token)
    assert_response_ok(response)
    assert_list_not_empty(response.json())
    print("Success, list_folders functions just fine.")

def test_list_folders_wrong_token(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = cache.get('vsphere_cloud_id', '')
    response = mist_core.list_folders(cloud_id=cloud_id, api_token="123Boom!")
    assert_response_unauthorized(response)
    print('Success')

def test_list_folders_wrong_cloud(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = cache.get('kubevirt_cloud_id', '')
    response = mist_core.list_folders(cloud_id=cloud_id, api_token=owner_api_token)
    assert_response_not_found(response)
    print('Success')

def test_list_folders_inexistent_cloud(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = "not_a_cloud"
    response = mist_core.list_folders(cloud_id=cloud_id, api_token=owner_api_token)
    assert_response_bad_request(response)
    print('Success')

def test_list_storage_classes(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = cache.get('kubevirt_cloud_id', '')
    response = mist_core.list_storage_classes(cloud_id=cloud_id, api_token=owner_api_token)
    assert_response_ok(response)
    assert_is_instance(response.json(), list)
    print('Success, list_storage_classes is working')

def test_list_storage_classes_wrong_token(pretty_print, mist_core,
                                          owner_api_token, cache):
    cloud_id = cache.get('kubevirt_cloud_id', '')
    response = mist_core.list_storage_classes(cloud_id=cloud_id, api_token="123Boom!")
    assert_response_unauthorized(response)
    print('Success')

def test_list_storage_classes_wrong_cloud(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = cache.get('vsphere_cloud_id', '')
    response = mist_core.list_storage_classes(cloud_id=cloud_id, api_token=owner_api_token)
    assert_response_not_found(response)
    print('Success')

def test_list_storage_classes_inexistent_cloud(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = "not_a_cloud"
    response = mist_core.list_storage_classes(cloud_id=cloud_id, api_token=owner_api_token)
    assert_response_bad_request(response)
    print('Success')

def test_list_projects(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = cache.get('packet_cloud_id', '')
    response = mist_core.list_projects(cloud_id=cloud_id, api_token=owner_api_token)
    assert_list_not_empty(response.json())
    print('Success')

def test_list_projects_wrong_token(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = cache.get('packet_cloud_id', '')
    response = mist_core.list_projects(cloud_id=cloud_id, api_token="123Boom!")
    assert_response_unauthorized(response)
    print('Success')

def test_list_projects_wrong_cloud(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = cache.get('kubevirt_cloud_id', '')
    response = mist_core.list_projects(cloud_id=cloud_id, api_token=owner_api_token)
    assert_list_empty(response)
    print('Success')

def test_list_projects_inexistent_cloud(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = "not_a_cloud"
    response = mist_core.list_projects(cloud_id=cloud_id, api_token=owner_api_token)
    assert_response_bad_request(response)
    print('Success')

def test_list_vnfs(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = cache.get('kvm_cloud_id', "")
    response = mist_core.list_vnfs(cloud_id=cloud_id, api_token=owner_api_token)
    assert_is_instance(response.json(), list)
    print('Success')
