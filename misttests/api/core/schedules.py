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
        response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()

        for machine in response.json():
            if 'api_test_machine_1' in machine['name']:
                cache.set('machine_id', machine['uuid'])
                break
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
        machines_uuids = []
        machines_uuids.append(cache.get('machine_id', ''))
        response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule1',
                                          action='stop', schedule_type='interval',
                                          machines_uuids=machines_uuids, run_immediately=True,
                                          schedule_entry={'every':2, 'period':'minutes'}).post()
        assert_response_ok(response)
        response = mist_core.list_schedules(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 1
        print "Success"

    def test_add_schedule_dup_name(self, pretty_print, mist_core, owner_api_token, cache):
        machines_uuids = []
        machines_uuids.append(cache.get('machine_id', ''))
        now = datetime.datetime.now()
        response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule1',
                                          action='stop', schedule_type='one_off',
                                          machines_uuids=machines_uuids, schedule_entry=str(now)).post()
        assert_response_conflict(response)
        print "Success!!!"

    def test_add_schedule_wrong_date(self, pretty_print, mist_core, owner_api_token, cache):
        machines_uuids = []
        machines_uuids.append(cache.get('machine_id', ''))
        date_now = str(datetime.datetime.now())
        response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule2',
                                          action='stop', schedule_type='one_off',
                                          machines_uuids=machines_uuids, schedule_entry=date_now).post()
        assert_response_bad_request(response)
        print "Success!!!"

    # def test_add_schedule_wrong_date(self, pretty_print, mist_core, owner_api_token, cache):
    #     machines_uuids = []
    #     machines_uuids.append(cache.get('machine_id', ''))
    #     now = datetime.datetime.now()
    #     delta = datetime.timedelta(hours=12)
    #     sched_time = ((datetime.datetime.combine(datetime.date(1, 1, 1), now.time()) + delta).time())
    #     response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule2',
    #                                       action='stop', schedule_type='one_off',
    #                                       machines_uuids=machines_uuids, schedule_entry=sched_time).post()
    #     assert_response_bad_request(response)
    #     print "Success!!!"

    def test_add_schedule_tagged_machine(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()

        for machine in response.json():
            if 'api_test_machine_2' in machine['name']:
                cache.set('tagged_machine_id', machine['uuid'])
                break
        machines_uuids = []
        machines_uuids.append(cache.get('tagged_machine_id', ''))
        tags = ['api_test']
        mist_core.set_machine_tags(tags=tags, api_token=owner_api_token,cloud_id=cache.get('cloud_id', ''),
                                   machine_id=cache.get('tagged_machine_id', '')).post()
        import ipdb;ipdb.set_trace()
        response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule1',
                                          action='stop', schedule_type='one_off',
                                          machines_uuids=machines_uuids).post()
        assert_response_bad_request(response)
        print "Success!!!"


# tag machine in last test
# add one-off for tagged machine
# add disabled schedule (make sure it won't run)
# add schedule and run immediately
# delete schedule (response OK)
# add one-off schedule with past date
# destroy resources created during the tests
