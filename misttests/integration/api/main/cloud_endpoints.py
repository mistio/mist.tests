from misttests.integration.api.utils import assert_response_ok
from misttests.config import safe_get_var
from misttests import config

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################
def test_add_vsphere_cloud(pretty_print, mist_core, cache, owner_api_token, name='VSphere'):
    response = mist_core.add_cloud(name, provider='vsphere', api_token=owner_api_token,
                                   machine_hostname=safe_get_var('clouds/vsphere-7', 'host'),
                                   machine_user=safe_get_var('clouds/vsphere-7', 'username'),
                                   password=safe_get_var('clouds/vsphere-7', 'password'),
                                   ca_cert_file=safe_get_var('clouds/vsphere-7', 'ca'),
                                   show_all=True).post()
    assert_response_ok(response)
    cache.set('vsphere_cloud_id', response.json()['id'])
    print("VSphere cloud added successfully")

# Proper
def test_list_datastores(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = cache.get('vsphere_cloud_id')
    response = mist_core.list_datastores(cloud_id=cloud_id, api_token=owner_api_token)
    assert_response_ok(response)
    assert (type(response.json() is list), "Did not get a list as a response!"
    assert (len(response.json) > 0), "The datastore list is empty!"
    print("list_datastores functions just fine.")

def test_list_folders(pretty_print, mist_core, owner_api_token, cache):
    cloud_id = cache.get('vsphere_cloud_id')
    response = mist_core.list_folders(cloud_id=cloud_id, api_token=owner_api_token)
    assert_response_ok(response)
    assert (type(response.json() is list), "Did not get a list as a response!"
    assert (len(response.json) > 0), "The folders list is empty!"
    print("list_folders functions just fine.")