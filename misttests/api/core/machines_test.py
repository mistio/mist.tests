from misttests.api.helpers import *
from misttests import config

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################

# should get forbidden?
def test_list_machines_no_api_token(pretty_print, mist_core):
    response = mist_core.list_machines(cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_list_machines_wrong_api_token(pretty_print, mist_core):
    response = mist_core.list_machines(cloud_id='dummy', api_token='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"

# internal server error? wtf????
# def test_list_machines_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
#     response = mist_core.list_machines(cloud_id='dummy', api_token=owner_api_token).get()
#     assert_response_not_found(response)
#     print "Success!!!"


# ask below, if image == '', then not found...
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

# internal server error? wtf????
# def test_create_machine_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
#     response = mist_core.create_machine(cloud_id='dummy', key_id='', api_token=owner_api_token,
#                                         name='', provider='', location='',
#                                         image='dummy', size='',).post()
#     assert_response_not_found(response)
#     print "Success!!!"


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


# below gets internal server error...
# def test_associate_key_no_wrong_ids(pretty_print, mist_core, owner_api_token):
#     response = mist_core.associate_key(cloud_id='dummy', api_token=owner_api_token,
#                                        machine_id='dummy',key_id='dummy').put()
#     assert_response_not_found(response)
#     print "Success!!!"

############################################################################
#                         Functional Testing                               #
############################################################################


@pytest.mark.incremental
class TestMachinesFunctionality:

    def test_list_machines(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.add_cloud(title='Docker', provider= 'docker', api_token=owner_api_token,
                                       docker_host=config.CREDENTIALS['DOCKER']['host'],
                                       docker_port=config.CREDENTIALS['DOCKER']['port'],
                                       authentication=config.CREDENTIALS['DOCKER']['authentication'],
                                       ca_cert_file=config.CREDENTIALS['DOCKER']['ca'],
                                       key_file=config.CREDENTIALS['DOCKER']['key'],
                                       cert_file=config.CREDENTIALS['DOCKER']['cert']).post()
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
        response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        import ipdb;ipdb.set_trace()
        for machine in response.json():

            print "Success!!!"

# destroy_machine
# wrong action
# stop , start machine
# associate key
