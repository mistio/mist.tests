import time
from misttests.integration.api.utils import assert_response_ok
from misttests.integration.api.utils import assert_list_not_empty
from misttests.integration.api.utils import assert_response_unauthorized
from misttests.integration.api.utils import assert_response_not_found
from misttests.integration.api.utils import assert_response_bad_request
from misttests.integration.api.utils import assert_is_instance
from misttests.integration.api.utils import assert_list_empty
from misttests.integration.api.utils import assert_response_not_found
from misttests.integration.api.utils import assert_equal, assert_not_equal
from misttests.config import safe_get_var
from misttests import config

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################

###### Adding clouds #############
def test_add_vsphere_cloud(pretty_print, mist_api_v1, cache, owner_api_token, name='VSphere'):
    response = mist_api_v1.add_cloud(name, provider='vsphere', api_token=owner_api_token,
                                   host=safe_get_var('clouds/vsphere', 'host'),
                                   username=safe_get_var('clouds/vsphere', 'username'),
                                   password=safe_get_var('clouds/vsphere', 'password'),
                                   ca_cert_file=safe_get_var('clouds/vsphere', 'ca_cert_file')
                                   ).post()
    assert_response_ok(response)
    cache.set('vsphere_cloud_id', response.json()['id'])
    print("Success, VSphere cloud added!")

def test_add_kubevirt_cloud(pretty_print, mist_api_v1, cache, owner_api_token, name="Kubevirt"):
    response = mist_api_v1.add_cloud(name, provider='kubevirt', api_token=owner_api_token,
                                   host=safe_get_var('clouds/kubevirt', 'host'),
                                   authentication='tokenbearer',
                                   token=safe_get_var('clouds/kubevirt', 'token'),
                                   ca_cert_file=safe_get_var('clouds/kubevirt', 'tlsCaCert')
                                   ).post()
    assert_response_ok(response)
    cache.set('kubevirt_cloud_id', response.json()['id'])
    print("Success, Kubevirt added!")

def test_add_equinix_cloud(pretty_print, mist_api_v1, cache, owner_api_token, name="Equinix Metal"):
    response = mist_api_v1.add_cloud(name, provider='equinixmetal', api_token=owner_api_token,
                                   apikey=safe_get_var('clouds/packet', 'apikey')
                                   ).post()
    assert_response_ok(response)
    cache.set('equinix_metal_cloud_id', response.json()['id'])
    print("Success, Equinix Metal added!")

def test_add_azure_arm_cloud(pretty_print, mist_api_v1, cache, owner_api_token, name="Azure"):
    response = mist_api_v1.add_cloud(name, provider='azure_arm', api_token=owner_api_token,
                                   tenant_id=safe_get_var('clouds/azure_arm', 'tenant_id'),
                                   subscription_id=safe_get_var('clouds/azure_arm', 'subscription_id'),
                                   key=safe_get_var('clouds/azure_arm', 'client_key'),
                                   secret=safe_get_var('clouds/azure_arm', 'client_secret')
                                   ).post()
    assert_response_ok(response)
    cache.set('azure_cloud_id', response.json()['id'])
    print("Success, Azure added!")

def test_add_lxd_cloud(pretty_print, mist_api_v1, cache, owner_api_token, name="LXD"):
    response = mist_api_v1.add_cloud(name, provider='lxd', api_token=owner_api_token,
                                   host=safe_get_var('clouds/lxd', 'host'),
                                   key_file=safe_get_var('clouds/lxd', 'tlsKey'),
                                   cert_file=safe_get_var('clouds/lxd', 'tlsCert'),
                                   port=8443
                                   ).post()
    assert_response_ok(response)
    cache.set('lxd_cloud_id', response.json()['id'])
    print("Success, LXD added!")

########## Testing endpoints ###########

  ##### VSphere endpoints #####
def test_list_datastores(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = cache.get('vsphere_cloud_id', '')
    response = mist_api_v1.list_datastores(cloud_id=cloud_id, api_token=owner_api_token).get()
    assert_response_ok(response)
    assert_list_not_empty(response.json())
    print("Success, list_datastores functions just fine.")

def test_list_datastores_wrong_token(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = cache.get('vsphere_cloud_id', '')
    response = mist_api_v1.list_datastores(cloud_id=cloud_id, api_token="123Boom!").get()
    assert_response_unauthorized(response)
    print('Success')

def test_list_datastores_wrong_cloud(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = cache.get('kubevirt_cloud_id', '')
    response = mist_api_v1.list_datastores(cloud_id=cloud_id, api_token=owner_api_token).get()
    assert_response_bad_request(response)
    print('Success')

def test_list_datastores_inexistent_cloud(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = "not_a_cloud"
    response = mist_api_v1.list_datastores(cloud_id=cloud_id, api_token=owner_api_token).get()
    assert_response_not_found(response)
    print('Success')

def test_list_folders(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = cache.get('vsphere_cloud_id', '')
    response = mist_api_v1.list_folders(cloud_id=cloud_id, api_token=owner_api_token).get()
    assert_response_ok(response)
    assert_list_not_empty(response.json())
    print("Success, list_folders functions just fine.")

def test_list_folders_wrong_token(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = cache.get('vsphere_cloud_id', '')
    response = mist_api_v1.list_folders(cloud_id=cloud_id, api_token="123Boom!").get()
    assert_response_unauthorized(response)
    print('Success')

def test_list_folders_wrong_cloud(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = cache.get('kubevirt_cloud_id', '')
    response = mist_api_v1.list_folders(cloud_id=cloud_id, api_token=owner_api_token).get()
    assert_response_bad_request(response)
    print('Success')

def test_list_folders_inexistent_cloud(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = "not_a_cloud"
    response = mist_api_v1.list_folders(cloud_id=cloud_id, api_token=owner_api_token).get()
    assert_response_not_found(response)
    print('Success')

  ##### Kubevirt endpoints #####
def test_list_storage_classes(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = cache.get('kubevirt_cloud_id', '')
    response = mist_api_v1.list_storage_classes(cloud_id=cloud_id, api_token=owner_api_token).get()
    assert_response_ok(response)
    assert_is_instance(response.json(), list)
    print('Success, list_storage_classes is working')

def test_list_storage_classes_wrong_token(pretty_print, mist_api_v1,
                                          owner_api_token, cache):
    cloud_id = cache.get('kubevirt_cloud_id', '')
    response = mist_api_v1.list_storage_classes(cloud_id=cloud_id, api_token="123Boom!").get()
    assert_response_unauthorized(response)
    print('Success')

def test_list_storage_classes_wrong_cloud(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = cache.get('vsphere_cloud_id', '')
    response = mist_api_v1.list_storage_classes(cloud_id=cloud_id, api_token=owner_api_token).get()
    assert_response_bad_request(response)
    print('Success')

def test_list_storage_classes_inexistent_cloud(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = "not_a_cloud"
    response = mist_api_v1.list_storage_classes(cloud_id=cloud_id, api_token=owner_api_token).get()
    assert_response_not_found(response)
    print('Success')

  ##### Equinix Metal endpoints #####
def test_list_projects(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = cache.get('equinix_metal_cloud_id', '')
    response = mist_api_v1.list_projects(cloud_id=cloud_id, api_token=owner_api_token).get()
    assert_list_not_empty(response.json())
    print('Success')

def test_list_projects_wrong_token(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = cache.get('equinix_metal_cloud_id', '')
    response = mist_api_v1.list_projects(cloud_id=cloud_id, api_token="123Boom!").get()
    assert_response_unauthorized(response)
    print('Success')

def test_list_projects_wrong_cloud(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = cache.get('kubevirt_cloud_id', '')
    response = mist_api_v1.list_projects(cloud_id=cloud_id, api_token=owner_api_token).get()
    assert_list_empty(response.json())
    print('Success')

def test_list_projects_inexistent_cloud(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = "not_a_cloud"
    response = mist_api_v1.list_projects(cloud_id=cloud_id, api_token=owner_api_token).get()
    assert_response_not_found(response)
    print('Success')

  ##### Azure ARM endpoints #####
def test_list_resource_groups(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = cache.get('azure_cloud_id', "")
    response = mist_api_v1.list_resource_groups(cloud_id=cloud_id, api_token=owner_api_token).get()
    assert_list_not_empty(response.json())
    print('Success')

def test_list_storage_accounts(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = cache.get('azure_cloud_id', "")
    locations_response = mist_api_v1.list_locations(cloud_id=cloud_id, api_token=owner_api_token).get()
    # Need to have locations in the database
    assert_list_not_empty(locations_response.json())
    response = mist_api_v1.list_storage_accounts(cloud_id=cloud_id, api_token=owner_api_token).get()
    assert_list_not_empty(response.json())
    print('Success')

  ##### LXD endpoints #####
def test_list_storage_pools(pretty_print, mist_api_v1, owner_api_token, cache):
    cloud_id = cache.get('lxd_cloud_id', "")
    response = mist_api_v1.list_storage_pools(cloud_id=cloud_id, api_token=owner_api_token).get()
    assert_list_not_empty(response.json())
    print('Success')

############################################################################
#                         Functional Testing                               #
############################################################################

class TestKVMfunctionality:

    def test_add_kvm_cloud(pretty_print, mist_api_v1, cache, owner_api_token, name="KVM"):
        # first we need the key to exist, maybe change this in the api?
        response = mist_api_v1.add_key('kvm_key', private=safe_get_var('clouds/other_server', 'key'),
                                    api_token=owner_api_token).put()
        assert_response_ok(response)
        key_id = response.json()['id']
        response = mist_api_v1.add_cloud(name, provider='libvirt', api_token=owner_api_token,
                                    hosts=[{
                                    'machine_name': "KVM_machine",
                                    'machine_hostname': safe_get_var('clouds/other_server', 'hostname'),
                                    'machine_user': 'root',
                                    'machine_key': key_id,
                                    'images_location': '/var/lib/libvirt/images',
                                    'ssh_port': 22}]).post()
        assert_response_ok(response)
        cache.set('kvm_cloud_id', response.json()['id'])
        print("Success, KVM added!")

    def test_list_vnfs(pretty_print, mist_api_v1, owner_api_token, cache):
        cloud_id = cache.get('kvm_cloud_id', "")
        response = mist_api_v1.list_vnfs(cloud_id=cloud_id, api_token=owner_api_token).get()
        assert_is_instance(response.json(), list)
        print('Success')

    def test_list_machines(pretty_print, mist_api_v1, owner_api_token, cache):
        cloud_id = cache.get('kvm_cloud_id', "")
        response = mist_api_v1.list_machines(cloud_id=cloud_id, api_token=owner_api_token).get()
        assert_is_instance(response.json(), list)
        print('Success')

    def test_list_sizes(pretty_print, mist_api_v1, owner_api_token, cache):
        cloud_id = cache.get('kvm_cloud_id', "")
        response = mist_api_v1.list_sizes(cloud_id=cloud_id, api_token=owner_api_token).get()
        assert_is_instance(response.json(), list)
        print('Success!')

    def test_list_images(pretty_print, mist_api_v1, owner_api_token, cache):
        cloud_id = cache.get('kvm_cloud_id', "")
        response = mist_api_v1.list_images(cloud_id=cloud_id, api_token=owner_api_token).get()
        assert_list_not_empty(response.json(), list)
        cache.set('kvm_image_id', response.json()[0].get('id'))
        print('Success!')

    def test_list_locations(pretty_print, mist_api_v1, owner_api_token, cache):
        cloud_id = cache.get('kvm_cloud_id', "")
        response = mist_api_v1.list_locations(cloud_id=cloud_id, api_token=owner_api_token).get()
        assert_list_not_empty(response.json(), list)
        cache.set("kvm_location_id", response.json()[0].get('id'))
        print('Success!')

    def test_create_machine(pretty_print, mist_api_v1, owner_api_token, cache):
        cloud_id = cache.get('kvm_cloud_id', "")
        response = mist_api_v1.create_machine(cloud_id=cloud_id, key_id="",
                                            name="api_test_machine",
                                            provider='libvirt',
                                            location=cache.get(
                                                'kvm_location_id', ''),
                                            image=cache.get(
                                                'kvm_image_id', ''),
                                            size={'ram':1024, 'cpu':1},
                                            disk=4, api_token=owner_api_token
                                            ).post()
        assert_response_ok(response)
        time.sleep(250) # Wait for the machine to be created
        print('Success!')

    def test_list_machines(pretty_print, mist_api_v1, owner_api_token, cache):
        cloud_id = cache.get('kvm_cloud_id', "")
        response = mist_api_v1.list_machines(cloud_id=cloud_id, api_token=owner_api_token
                                            ).get()
        machines = response.json()
        assert_list_not_empty(machines)
        for machine in machines:
            if "api_test_machine" in machine.get('name'):
                cache.set('kvm_machine_id', machine.get('id'))
                cache.set('kvm_machine_provider_id',
                           machine.get('machine_id'))
        if not cache.get('kvm_machine_id', ''):
            raise AssertionError("Machine was not created!!")
        print('Success!')

    def test_stop_machine(pretty_print, mist_api_v1, owner_api_token,
                                cache):
        cloud_id = cache.get('kvm_cloud_id', "")
        machine_id = cache.get('kvm_machine_provider_id', '')
        stop_response = mist_api_v1.machine_action(cloud_id=cloud_id,
                                                  machine_id=machine_id,
                                                  api_token=owner_api_token,
                                                  action='stop').post()
        assert_response_ok(stop_response)
        time.sleep(250)  # Make sure the machine will stop
        #force list machines to update status
        response = mist_api_v1.list_machines(cloud_id=cloud_id, api_token=owner_api_token
                                            ).get()
        for machine in response.json():
            if machine.get('machine_id') == machine_id:
                assert_equal(machine.get(
                    'state'), 'terminated', "Machine did not stop!!")
        print("Success!")

    def test_start_machine(pretty_print, mist_api_v1, owner_api_token,
                           cache):
        cloud_id = cache.get('kvm_cloud_id', "")
        machine_id = cache.get('kvm_machine_provider_id', '')
        start_response = mist_api_v1.machine_action(cloud_id=cloud_id,
                                                  machine_id=machine_id,
                                                  api_token=owner_api_token,
                                                  action='start').post()
        assert_response_ok(start_response)
        time.sleep(60)  # Make sure the machine will start
        #force list machines to update status
        response = mist_api_v1.list_machines(cloud_id=cloud_id, api_token=owner_api_token
                                            ).get()
        for machine in response.json():
            if machine.get('machine_id') == machine_id:
                assert_equal(machine.get(
                    'state'), 'running', "Machine did not start!!")
        print("Success!")

    def test_destroy_machine(pretty_print, mist_api_v1, owner_api_token, cache):
        cloud_id = cache.get('kvm_cloud_id', "")
        machine_id = cache.get('kvm_machine_provider_id', '')
        response = mist_api_v1.machine_action(cloud_id=cloud_id,
                                                  machine_id=machine_id,
                                                  api_token=owner_api_token,
                                                  action='destroy').post()
        assert_response_ok(response)
        time.sleep(60)  # Make sure the machine will shutdown
        #force list machines to update status
        response = mist_api_v1.list_machines(cloud_id=cloud_id, api_token=owner_api_token
                                            ).get()
        for machine in response.json():
            if machine.get('machine_id') == machine_id:
                assert_equal(machine.get(
                    'state'), 'terminated', "Machine is not terminated!")
        print("Success!")

    def test_undefine_machine(pretty_print, mist_api_v1,
                              owner_api_token, cache):
        cloud_id = cache.get('kvm_cloud_id', "")
        machine_id = cache.get('kvm_machine_provider_id', '')
        response = mist_api_v1.undefine_machine(cloud_id=cloud_id,
                                                  machine_id=machine_id,
                                                  api_token=owner_api_token,
                                                  delete_image=True).post()
        assert_response_ok(response)
        time.sleep(30)  # Make sure the machine will be deleted
        response = mist_api_v1.list_machines(cloud_id=cloud_id, api_token=owner_api_token
                                            ).get()
        msg="Machine still found in list!"
        for machine in response.json():
            assert_not_equal(machine.get('machine_id'), machine_id, msg=msg)
        print("Success!")
