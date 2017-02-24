from misttests.api.helpers import *
from misttests import config
from time import sleep

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
                # need this check for test below
                assert machine['state'] == 'running', "Machine'state is not running in he beginning of the tests"
            if 'api_test_machine_2' in machine['name']:
                response = mist_core.set_machine_tags(api_token=owner_api_token, cloud_id=cache.get('cloud_id', ''),
                                                      machine_id=machine['uuid'],
                                                      tags={'key': 'schedule_test', 'value': ''}).post()
                assert_response_ok(response)
        machines_uuids = []
        machines_uuids.append(cache.get('machine_id',''))
        response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule1',
                                          action='stop', schedule_type='one_off',
                                          machines_uuids = machines_uuids).post()
        assert_response_bad_request(response)
        print "Success!!!"

    # def test_add_one_off_schedule_run_immediately_ok(self, pretty_print, mist_core, owner_api_token, cache):
    #     machines_uuids = []
    #     machines_uuids.append(cache.get('machine_id', ''))
    #     date_now = datetime.datetime.now().replace(microsecond=0)
    #     scheduled_date = date_now + datetime.timedelta(seconds=3)
    #
    #     response = mist_core.add_schedule(api_token=owner_api_token, name='RunImmediatelySchedule',
    #                                       action='stop', schedule_type='one_off',
    #                                       machines_uuids=machines_uuids,
    #                                       run_immediately=True,
    #                                       schedule_entry=str(scheduled_date)).post()
    #     import ipdb
    #     ipdb.set_trace()
    #     assert_response_ok(response)
    #     cache.set('schedule_id', response.json()['id'])
    #     sleep(5)
    #     response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()
    #     for machine in response.json():
    #         if 'api_test_machine_1' in machine['name']:
    #             import ipdb
    #             ipdb.set_trace()
    #             assert machine['state'] == 'stopped', "Machine'state is not running in he beginning of the tests"
    #             break
    #     print "Success"

    def test_add_interval_schedule_ok(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        machines_uuids = []
        machines_uuids.append(cache.get('machine_id', ''))
        response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule1',
                                          action='stop', schedule_type='interval',
                                          machines_uuids=machines_uuids, run_immediately=True,
                                          schedule_entry={'every': 2, 'period':'minutes'}).post()
        assert_response_ok(response)
        cache.set('schedule_id', response.json()['id'])
        response = mist_core.list_schedules(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 1
        print "Success"

    def test_add_interval_schedule_tags_ok(self, pretty_print, mist_core, owner_api_token):
        response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule2',
                                          action='stop', schedule_type='interval',
                                          machines_tags={'schedule_test': ''},
                                          run_immediately=True,
                                          schedule_entry={'every': 2, 'period':'minutes'}).post()
        assert_response_ok(response)
        response = mist_core.list_schedules(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 2
        print "Success"

    def test_add_one_off_schedule_tags_ok(self, pretty_print, mist_core, owner_api_token):
        date_now = datetime.datetime.now().replace(microsecond=0)
        scheduled_date = date_now + datetime.timedelta(seconds=10)
        response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule3',
                                          action='stop', schedule_type='one_off',
                                          machines_tags={'schedule_test': ''},
                                          run_immediately=True,
                                          schedule_entry=str(scheduled_date)).post()
        assert_response_ok(response)
        response = mist_core.list_schedules(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 3
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

    def test_add_one_off_schedule_wrong_date(self, pretty_print, mist_core, owner_api_token, cache):
        machines_uuids = []
        machines_uuids.append(cache.get('machine_id', ''))
        date_now = datetime.datetime.now().replace(microsecond=0)
        response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule4',
                                          action='stop', schedule_type='one_off',
                                          machines_uuids=machines_uuids, schedule_entry=str(date_now)).post()
        assert_response_bad_request(response)
        past_date = date_now - datetime.timedelta(seconds=10)
        response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule4',
                                          action='stop', schedule_type='one_off',
                                          machines_uuids=machines_uuids, schedule_entry=str(past_date)).post()
        assert_response_bad_request(response)
        print "Success!!!"

    def test_add_disabled_schedule(self, pretty_print, mist_core, owner_api_token, cache):
        machines_uuids = []
        machines_uuids.append(cache.get('machine_id', ''))
        response = mist_core.add_schedule(api_token=owner_api_token, name='DisabledSchedule',
                                          action='stop', schedule_type='interval', task_enabled=False,
                                          machines_uuids=machines_uuids, run_immediately=True,
                                          schedule_entry={'every': 2, 'period': 'minutes'}).post()
        assert_response_ok(response)
        cache.set('disabled_schedule_id', response.json()['id'])
        print "Success"

    def test_delete_schedule_ok(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.delete_schedule(api_token=owner_api_token, schedule_id=cache.get('schedule_id', '')).delete()
        assert_response_ok(response)
        response = mist_core.delete_schedule(api_token=owner_api_token, schedule_id=cache.get('schedule_id', '')).delete()
        assert_response_not_found(response)
        print "Success!!!"

    def test_total_run_counts(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.show_schedule(api_token=owner_api_token, schedule_id=cache.get('disabled_schedule_id', '')).get()
        assert_response_ok(response)
        assert response.json()['total_run_count'] == 0, "Schedule run although it was disabled!!!"
        print "Success!!!"


# add schedule and run immediately (sto telos...make machine start..)

# destroy resources created during the tests

# Add script, and then add a schedule with the script to run in a machine
# Edit a schedule (make it stop--> start and check that the machine is running)
# Check that actions were performed and scripts run
# Make sure that the machines are in the proper state after the tests'execution
