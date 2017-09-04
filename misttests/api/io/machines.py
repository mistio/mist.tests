from misttests.api.helpers import *
from misttests.config import safe_get_var
from misttests import config

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_machines_no_api_token(pretty_print, mist_core):
    response = mist_core.list_machines(cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_list_machines_wrong_api_token(pretty_print, mist_core):
    response = mist_core.list_machines(cloud_id='dummy', api_token='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_list_machines_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_machines(cloud_id='dummy', api_token=owner_api_token).get()
    assert_response_not_found(response)
    print "Success!!!"


def test_create_machine_wrong_api_token(pretty_print, mist_core):
    response = mist_core.create_machine(cloud_id='dummy', api_token='dummy',
                                        key_id='', name='', provider='', location='',
                                        image='dummy', size='',).post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_create_machine_no_api_token(pretty_print, mist_core):
    response = mist_core.create_machine(cloud_id='dummy', key_id='',
                                        name='', provider='', location='',
                                        image='dummy', size='',).post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_create_machine_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_machine(cloud_id='dummy', key_id='', api_token=owner_api_token,
                                        name='', provider='', location='',
                                        image='dummy', size='',).post()
    assert_response_not_found(response)
    print "Success!!!"


def test_create_machine_missing_parameter(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_machine(cloud_id='dummy', key_id='', api_token=owner_api_token,
                                        name='', provider='', location='',
                                        image='', size='',).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_destroy_machine_wrong_api_token(pretty_print, mist_core):
    response = mist_core.destroy_machine(cloud_id='dummy', api_token='dummy',
                                         machine_id='dummy',).post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_destroy_machine_no_api_token(pretty_print, mist_core):
    response = mist_core.destroy_machine(cloud_id='dummy',
                                         machine_id='dummy',).post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_destroy_machine_wrong_ids(pretty_print, mist_core, owner_api_token):
    response = mist_core.destroy_machine(cloud_id='dummy',api_token=owner_api_token,
                                         machine_id='dummy',).post()
    assert_response_not_found(response)
    print "Success!!!"


def test_machine_action_wrong_api_token(pretty_print, mist_core):
    response = mist_core.machine_action(cloud_id='dummy', api_token='dummy',
                                        machine_id='dummy',).post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_machine_action_no_api_token(pretty_print, mist_core):
    response = mist_core.machine_action(cloud_id='dummy',
                                         machine_id='dummy',).post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_machine_action_wrong_ids(pretty_print, mist_core, owner_api_token):
    response = mist_core.machine_action(cloud_id='dummy',api_token=owner_api_token,
                                        machine_id='dummy',).post()
    assert_response_not_found(response)
    print "Success!!!"


def test_associate_key_wrong_api_token(pretty_print, mist_core):
    response = mist_core.associate_key(cloud_id='dummy', api_token='dummy',
                                       machine_id='dummy',key_id='dummy').put()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_associate_key_no_api_token(pretty_print, mist_core):
    response = mist_core.associate_key(cloud_id='dummy', api_token='',
                                       machine_id='dummy',key_id='dummy').put()
    assert_response_forbidden(response)
    print "Success!!!"


def test_associate_key_wrong_ids(pretty_print, mist_core, owner_api_token):
    response = mist_core.associate_key(cloud_id='dummy', machine_id='dummy',
                                       key_id='dummy',
                                       api_token=owner_api_token).put()
    assert_response_not_found(response)
    print "Success!!!"

############################################################################
#                         Functional Testing                               #
############################################################################


@pytest.mark.incremental
class TestMachinesFunctionality:

    def test_list_machines(self, pretty_print, mist_core, cache, owner_api_token):
        if config.LOCAL:
            response = mist_core.add_cloud(title='Docker', provider='docker', api_token=owner_api_token,
                                       docker_host=config.MIST_URL,
                                       docker_port='2375').post()
        else:
            response = mist_core.add_cloud(title='Docker', provider='docker', api_token=owner_api_token,
                                       docker_host=safe_get_var('dockerhosts/godzilla', 'host',
                                                                config.CREDENTIALS['DOCKER']['host']),
                                       docker_port=safe_get_var('dockerhosts/godzilla', 'port',
                                                                config.CREDENTIALS['DOCKER']['port']),
                                       authentication=safe_get_var('dockerhosts/godzilla', 'authentication',
                                                                   config.CREDENTIALS['DOCKER']['authentication']),
                                       ca_cert_file=safe_get_var('dockerhosts/godzilla', 'ca',
                                                                 config.CREDENTIALS['DOCKER']['ca']),
                                       key_file=safe_get_var('dockerhosts/godzilla', 'key',
                                                             config.CREDENTIALS['DOCKER']['key']),
                                       cert_file=safe_get_var('dockerhosts/godzilla', 'cert',
                                                              config.CREDENTIALS['DOCKER']['cert']), show_all=True).post()
        assert_response_ok(response)
        cache.set('cloud_id', response.json()['id'])
        response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List machines did not return any machines"
        print "Success!!!"

    def test_create_machine(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.list_images(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).post()
        assert_response_ok(response)
        for image in response.json():
            if 'Ubuntu 14.04' in image['name']:
                cache.set('image_id', image['id'])
                break;
        name = 'api_test_machine_%d' % random.randint(1,200)
        cache.set('machine_name', name)
        response = mist_core.create_machine(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token,
                                            key_id='', name=name, provider='', location='',
                                            image=cache.get('image_id', ''), size='').post()
        assert_response_ok(response)
        cache.set('machine_id', response.json()['id'])
        response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        found = False
        for machine in response.json():
            if machine['name'] == cache.get('machine_name', ''):
                found = True
                print "Success!!!"
                break
        if not found:
            assert False, "The machine that was added above is not present in list_machines"

    def test_machine_wrong_machine_id(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.machine_action(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token,
                                            machine_id='dummy').post()
        assert_response_not_found(response)
        print "Success!!!"

    def test_machine_wrong_action(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.machine_action(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token,
                                            machine_id=cache.get('machine_id', '')).post()
        assert_response_bad_request(response)
        print "Success!!!"

    def test_machine_stop_machine(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.machine_action(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token,
                                            machine_id=cache.get('machine_id', ''), action='stop').post()
        assert_response_ok(response)
        for machine in response.json():
            if machine['name'] == cache.get('machine_name', ''):
                assert machine['state'] == 'stopped', "Machine's state is not stopped!"
                print "Success!!!"
                break

    # def test_machine_monitoring_wrong_action(self, pretty_print, mist_core, cache, owner_api_token):
    #     response = mist_core.machine_monitoring(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token,
    #                                             machine_id=cache.get('machine_id', '')).post()
    #     assert_response_bad_request(response)
    #     print "Success!!!"
    #
    # def test_machine_enable_monitoring(self, pretty_print, mist_core, cache, owner_api_token):
    #     response = mist_core.machine_action(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token,
    #                                         machine_id=cache.get('machine_id', ''), action='start').post()
    #     assert_response_ok(response)
    #     for machine in response.json():
    #         if machine['name'] == cache.get('machine_name', ''):
    #             assert machine['state'] == 'running', "Machine's state is not running!"
    #             break
    #     response = mist_core.machine_monitoring(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token,
    #                                             machine_id=cache.get('machine_id', ''), action='enable').post()
    #     assert_response_ok(response)
    #     print "Success!!!"

    # def test_associate_key(self, pretty_print, mist_core, cache, private_key, owner_api_token):
    #     response = mist_core.add_key(
    #         name='TestKey',
    #         private=private_key,
    #         api_token=owner_api_token).put()
    #     assert_response_ok(response)
    #     cache.set('key_id', response.json()['id'])
    #     response = mist_core.associate_key(cloud_id=cache.get('cloud_id', ''), machine_id=cache.get('machine_id', ''),
    #                                        key_id=cache.get('key_id', ''), api_token=owner_api_token).put()
    #     assert_response_ok(response)
    #     print "Success!!!"

    def test_destroy_machine(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.destroy_machine(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token,
                                             machine_id='dummy', ).post()
        assert_response_not_found(response)
        response = mist_core.destroy_machine(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token,
                                             machine_id=cache.get('machine_id', ''), ).post()
        assert_response_ok(response)
        response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        for machine in response.json():
            if machine['name'] == cache.get('machine_name', ''):
                assert False, "Machine was not destroyed!!!"
        print "Success!!!"
