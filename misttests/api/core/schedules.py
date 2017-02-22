from misttests.api.helpers import *
from misttests import config

import pytest
import datetime

############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_schedules(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_schedules(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print "Success!!!"


def test_list_schedules_no_api_token(pretty_print, mist_core):
    response = mist_core.list_schedules(api_token='').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_list_schedules_wrong_api_token(pretty_print, mist_core):
    response = mist_core.list_schedules(api_token='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_add_schedule_no_api_token(pretty_print, mist_core):
    response = mist_core.add_schedule(api_token='', name='dummy',
                                      schedule_type='one=off').post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_add_schedule_wrong_api_token(pretty_print, mist_core):
    response = mist_core.add_schedule(api_token='dummy', name='dummy',
                                      schedule_type='one=off').post()
    assert_response_unauthorized(response)
    print "Success!!!"


# def test_add_schedule_missing_parameter(pretty_print, mist_core, owner_api_token):
#     response = mist_core.add_schedule(api_token=owner_api_token, name='dummy').post()
#     assert_response_bad_request(response)
#     print "Success!!!"


def test_delete_schedule_no_api_token(pretty_print, mist_core):
    response = mist_core.delete_schedule(api_token='', schedule_id='dummy').delete()
    assert_response_forbidden(response)
    print "Success!!!"


def test_delete_schedule_wrong_api_token(pretty_print, mist_core):
    response = mist_core.delete_schedule(api_token='dummy', schedule_id='dummy').delete()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_delete_schedule_wrong_schedule_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_schedule(api_token=owner_api_token, schedule_id='dummy').delete()
    assert_response_not_found(response)
    print "Success!!!"


def test_edit_schedule_no_api_token(pretty_print, mist_core):
    response = mist_core.edit_schedule(api_token='', schedule_id='dummy').patch()
    assert_response_forbidden(response)
    print "Success!!!"


def test_edit_schedule_wrong_api_token(pretty_print, mist_core):
    response = mist_core.edit_schedule(api_token='dummy', schedule_id='dummy').patch()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_edit_schedule_wrong_schedule_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.edit_schedule(api_token=owner_api_token, schedule_id='dummy').patch()
    assert_response_not_found(response)
    print "Success!!!"


def test_show_schedule_no_api_token(pretty_print, mist_core):
    response = mist_core.show_schedule(api_token='', schedule_id='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_show_schedule_wrong_api_token(pretty_print, mist_core):
    response = mist_core.show_schedule(api_token='dummy', schedule_id='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_show_schedule_wrong_schedule_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.show_schedule(api_token=owner_api_token, schedule_id='').get()
    assert_response_not_found(response)
    print "Success!!!"


############################################################################
#                         Functional Testing                               #
############################################################################


@pytest.mark.incremental
class TestSchedulesFunctionality:

    # def test_add_schedule_one_off__missing_schedule_entry(self, pretty_print, mist_core, owner_api_token, cache):
    #     response = mist_core.add_cloud(title='Openstack', provider= 'openstack', api_token=owner_api_token,
    #                                    username=config.CREDENTIALS['OPENSTACK']['username'],
    #                                    password=config.CREDENTIALS['OPENSTACK']['password'],
    #                                    auth_url=config.CREDENTIALS['OPENSTACK']['auth_url'],
    #                                    tenant_name=config.CREDENTIALS['OPENSTACK']['tenant']).post()
    #     assert_response_ok(response)
    #     import ipdb;ipdb.set_trace()
    #     cache.set('cloud_id', response.json()['id'])
    #     response = mist_core.list_images(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).post()
    #     assert_response_ok(response)
    #     for image in response.json():
    #         if 'CoreOS' in image['name']:
    #             cache.set('image_id', image['id'])
    #             break;
    #     name = 'api_test_machine_%d' % random.randint(1, 200)
    #     cache.set('machine_name', name)
    #     response = mist_core.create_machine(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token,
    #                                         key_id='', name=name, provider='', location='',
    #                                         image=cache.get('image_id', ''), size='').post()
    #     assert_response_ok(response)
    #     cache.set('machine_id', response.json()['id'])

    def test_add_schedule_one_off__missing_schedule_entry(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.add_cloud(title='Docker', provider= 'docker', api_token=owner_api_token,
                                       docker_host=config.CREDENTIALS['DOCKER']['host'],
                                       docker_port=config.CREDENTIALS['DOCKER']['port'],
                                       authentication=config.CREDENTIALS['DOCKER']['authentication'],
                                       ca_cert_file=config.CREDENTIALS['DOCKER']['ca'],
                                       key_file=config.CREDENTIALS['DOCKER']['key'],
                                       cert_file=config.CREDENTIALS['DOCKER']['cert']).post()
        assert_response_ok(response)
        cache.set('cloud_id', response.json()['id'])
        response = mist_core.list_images(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).post()
        assert_response_ok(response)
        for image in response.json():
            if 'Ubuntu 14.04' in image['name']:
                cache.set('image_id', image['id'])
                break;
        name = 'api_test_machine_%d' % random.randint(1, 200)

        cache.set('machine_name', name)
        response = mist_core.create_machine(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token,
                                            key_id='', name=name, provider='', location='',
                                            image=cache.get('image_id', ''), size='').post()
        assert_response_ok(response)
        response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()
        cache.set('machine_id', response.json()['id'])
        # for
        machines_uuids = []
        machines_uuids.append(cache.get('machine_id',''))
        response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule1',
                                          action='stop', schedule_type='one_off',
                                          machines_uuids = machines_uuids).post()
        assert_response_bad_request(response)
        print "Success!!!"

    def test_add_schedule_interval_ok(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        for machine in response.json():
            if machine['id'] == cache.get('machine_id', ''):
                import ipdb;
                ipdb.set_trace()
                print machine['state']
                break

        machines_uuids = []
        machines_uuids.append(cache.get('machine_id', ''))
        response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule1',
                                          action='stop', schedule_type='interval',
                                          machines_uuids=machines_uuids, run_immediately=True,
                                          schedule_entry={'every':2, 'period':'minutes'}).post()
        assert_response_ok(response)

    # def test_add_schedule_one_off_wrong_date(self, pretty_print, mist_core, owner_api_token, cache):
    #     machines_uuids = []
    #     machines_uuids.append(cache.get('machine_id', ''))
    #     response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule1',
    #                                       action='stop', schedule_type='one_off',
    #                                       machines_uuids=machines_uuids, schedule_entry='2016-02-21 14:59:00').post()
    #     assert_response_bad_request(response)
    #     response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule1',
    #                                       action='stop', schedule_type='one_off',
    #                                       machines_uuids=machines_uuids, schedule_entry='dummy').post()
    #     assert_response_bad_request(response)
    #     print "Success!!!"

    # def test_add_schedule_one_off_ok(self, pretty_print, mist_core, owner_api_token, cache):
    #     machines_uuids = []
    #     machines_uuids.append(cache.get('machine_id', ''))
    #     now = datetime.datetime.now()
    #     import ipdb;ipdb.set_trace()
    #     response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule1',
    #                                       action='stop', schedule_type='one_off',
    #                                       machines_uuids=machines_uuids, schedule_entry=str(now)).post()
    #     assert_response_ok(response)
    #     print "Success!!!"






# create 2nd machine and tag

# delete schedule

# add schedule for tagged_machine

# add schedule_script_date

# edit-make it start, and check

# destroy_resources
