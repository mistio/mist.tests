from misttests.integration.api.helpers import *
from misttests.config import safe_get_var
from misttests import config

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_clouds(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print("Success!!!")


def test_add_cloud_missing_parameter(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.add_cloud("Openstack", 'openstack',
                                   api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print("Success!!!")


def test_add_cloud_wrong_api_token(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.add_cloud("Openstack", 'openstack',
                                   api_token='00' + owner_api_token[:-2]).post()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_add_cloud_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.add_cloud("Openstack", 'openstack').post()
    assert_response_forbidden(response)
    print("Success!!!")


def test_add_cloud_ok(pretty_print, mist_api_v1, owner_api_token, name='Docker'):
    if config.LOCAL:
        response = mist_api_v1.add_cloud(name, provider='docker', api_token=owner_api_token,
                                   docker_host=config.LOCAL_DOCKER,
                                   docker_port='2375').post()
    else:
        response = mist_api_v1.add_cloud(name, provider='docker', api_token=owner_api_token,
                                   docker_host=safe_get_var('clouds/dockerhost', 'host',
                                                            config.CREDENTIALS['DOCKER']['host']),
                                   docker_port=int(safe_get_var('clouds/dockerhost', 'port',
                                                            config.CREDENTIALS['DOCKER']['port'])),
                                   authentication=safe_get_var('clouds/dockerhost', 'authentication',
                                                               config.CREDENTIALS['DOCKER']['authentication']),
                                   ca_cert_file=safe_get_var('clouds/dockerhost', 'tlsCaCert',
                                                             config.CREDENTIALS['DOCKER']['tlsCaCert']),
                                   key_file=safe_get_var('clouds/dockerhost', 'tlsKey',
                                                         config.CREDENTIALS['DOCKER']['tlsKey']),
                                   cert_file=safe_get_var('clouds/dockerhost', 'tlsCert',
                                                          config.CREDENTIALS['DOCKER']['tlsCert']), show_all=True).post()
    assert_response_ok(response)
    print("Success!!!")


def test_add_cloud_from_secret(pretty_print, mist_api_v1, owner_api_token, name='Docker3'):
    if config.LOCAL:
        response = mist_api_v1.add_cloud(name, provider='docker', api_token=owner_api_token,
                                       docker_host=config.LOCAL_DOCKER,
                                       docker_port='2375').post()
    else:
        response = mist_api_v1.add_cloud(name, provider='docker', api_token=owner_api_token,
                                       docker_host=safe_get_var('clouds/dockerhost', 'host',
                                                                config.CREDENTIALS['DOCKER']['host']),
                                       docker_port=int(safe_get_var('clouds/dockerhost', 'port',
                                                                    config.CREDENTIALS['DOCKER']['port'])),
                                       authentication=safe_get_var('clouds/dockerhost', 'authentication',
                                                                   config.CREDENTIALS['DOCKER']['authentication']),
                                       ca_cert_file='secret(mist/clouds/Docker:ca_cert_file)',
                                       key_file='secret(mist/clouds/Docker:key_file)',
                                       cert_file='secret(mist/clouds/Docker:cert_file)',
                                       show_all=True).post()
    assert_response_ok(response)
    print("Success!!!")


def test_rename_cloud_wrong_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.rename_cloud(cloud_id='dummy', new_name='test',
                                      api_token=owner_api_token).put()
    assert_response_not_found(response)
    print("Success!!!")


def test_rename_cloud_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.rename_cloud(cloud_id='dummy', new_name='test').put()
    assert_response_forbidden(response)
    print("Success!!!")


def test_rename_cloud_wrong_api_token(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.rename_cloud(cloud_id='dummy', new_name='test',
                                      api_token='00' + owner_api_token[:-2]).put()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_rename_cloud_missing_parameter(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.rename_cloud(cloud_id='dummy', new_name='',
                                      api_token=owner_api_token).put()
    assert_response_not_found(response)
    print("Success!!!")


def test_remove_cloud_wrong_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.remove_cloud(cloud_id='dummy',api_token=owner_api_token).delete()
    assert_response_not_found(response)
    print("Success")


def test_remove_cloud_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.remove_cloud(cloud_id='dummy').delete()
    assert_response_forbidden(response)
    print("Success!!!")


def test_remove_cloud_wrong_api_token(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.remove_cloud(cloud_id='dummy', api_token='00' + owner_api_token[:-2]).delete()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_toggle_cloud_wrong_api_token(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.toggle_cloud(cloud_id='dummy', api_token='00' + owner_api_token[:-2]).post()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_toggle_cloud_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.toggle_cloud(cloud_id='dummy').post()
    assert_response_forbidden(response)
    print("Success!!!")


def test_toggle_cloud_wrong_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.toggle_cloud(cloud_id='dummy',api_token=owner_api_token).post()
    assert_response_not_found(response)
    print("Success")


############################################################################
#                         Functional Testing                               #
############################################################################


@pytest.mark.incremental
class TestCloudsFunctionality:

    def test_list_clouds(self, pretty_print, mist_api_v1, owner_api_token):
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 2
        print("Success!!!")

    def test_add_multiple_clouds(self, pretty_print, mist_api_v1, owner_api_token):
        test_add_cloud_ok(pretty_print, mist_api_v1, owner_api_token, name='Docker2')
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 3
        print("Success!!!")

    def test_add_cloud_failures(self, pretty_print, mist_api_v1, owner_api_token):
        test_add_cloud_missing_parameter(pretty_print, mist_api_v1, owner_api_token)
        test_add_cloud_no_api_token(pretty_print, mist_api_v1)
        test_add_cloud_wrong_api_token(pretty_print, mist_api_v1, owner_api_token)
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 3
        print("Success!!!")

    def test_remove_cloud(self, pretty_print, mist_api_v1, owner_api_token):
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        linode_id = response.json()[0]['id']
        response = mist_api_v1.remove_cloud(cloud_id=linode_id, api_token=owner_api_token).delete()
        assert_response_ok(response)
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 2
        response = mist_api_v1.remove_cloud(cloud_id=linode_id, api_token=owner_api_token).delete()
        assert_response_not_found(response)
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 2
        print("Success!!!")

    def test_remove_cloud_failures(self, pretty_print, mist_api_v1, owner_api_token):
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        linode_id = response.json()[0]['id']
        response = mist_api_v1.remove_cloud(cloud_id=linode_id+'d', api_token=owner_api_token).delete()
        assert_response_not_found(response)
        print("Success!!!")
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 2
        test_remove_cloud_no_api_token(pretty_print, mist_api_v1)
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 2
        print("Success!!!")

    def test_rename_cloud(self, pretty_print, mist_api_v1, owner_api_token):
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        cloud_id = response.json()[0]['id']
        response = mist_api_v1.rename_cloud(cloud_id=cloud_id, new_name='Renamed', api_token=owner_api_token).put()
        assert_response_ok(response)
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        for cloud in response.json():
            if cloud['name'] == 'Renamed':
                print("Success!!!")
                return
        assert False, "Renaming cloud did not work!!!"

    def test_toggle_cloud(self, pretty_print, mist_api_v1, owner_api_token):
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        assert response.json()[0]['enabled'] == True, "Cloud is not enabled by default!!!"
        cloud_id = response.json()[0]['id']
        test_toggle_cloud_wrong_id(pretty_print, mist_api_v1, owner_api_token)
        test_toggle_cloud_no_api_token(pretty_print, mist_api_v1)
        response = mist_api_v1.toggle_cloud(cloud_id=cloud_id, api_token=owner_api_token).post()
        assert_response_bad_request(response)
        response = mist_api_v1.toggle_cloud(cloud_id=cloud_id,new_state=0, api_token=owner_api_token).post()
        assert_response_ok(response)
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        assert response.json()[0]['enabled'] == False, "Cloud toggling did not work!!!"
        test_toggle_cloud_wrong_api_token(pretty_print, mist_api_v1, owner_api_token)
        response = mist_api_v1.toggle_cloud(cloud_id=cloud_id,new_state=3, api_token=owner_api_token).post()
        assert_response_bad_request(response)
        response = mist_api_v1.toggle_cloud(cloud_id=cloud_id, new_state=0, api_token=owner_api_token).post()
        assert_response_ok(response)
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        assert response.json()[0]['enabled'] == False, "Cloud toggling did not work!!!"
        response = mist_api_v1.toggle_cloud(cloud_id=cloud_id, new_state=1, api_token=owner_api_token).post()
        assert_response_ok(response)
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        assert response.json()[0]['enabled'] == True, "Cloud toggling did not work!!!"
        response = mist_api_v1.toggle_cloud(cloud_id=cloud_id, new_state='dummy_new_state', api_token=owner_api_token).post()
        assert_response_bad_request(response)

    def test_toggle_cloud_mini_stress_test(self, pretty_print, mist_api_v1, owner_api_token):
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        cloud_id = response.json()[0]['id']
        for i in range(1,21):
            if i % 2 == 0:
                response = mist_api_v1.toggle_cloud(cloud_id=cloud_id, new_state=1, api_token=owner_api_token).post()
                assert_response_ok(response)
            else:
                response = mist_api_v1.toggle_cloud(cloud_id=cloud_id, new_state=0, api_token=owner_api_token).post()
                assert_response_ok(response)
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        assert response.json()[0]['enabled'] == True, "Cloud toggling did not work!!!"
