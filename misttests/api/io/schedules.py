from misttests.api.helpers import *
from misttests import config
from time import sleep

import pytest
import datetime

############################################################################
#                             Unit Testing                                 #
############################################################################

#
# def test_list_schedules(pretty_print, mist_core, owner_api_token):
#     response = mist_core.list_schedules(api_token=owner_api_token).get()
#     assert_response_ok(response)
#     assert len(response.json()) == 0
#     print "Success!!!"
#
#
# def test_list_schedules_no_api_token(pretty_print, mist_core):
#     response = mist_core.list_schedules(api_token='').get()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_list_schedules_wrong_api_token(pretty_print, mist_core):
#     response = mist_core.list_schedules(api_token='dummy').get()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_add_schedule_no_api_token(pretty_print, mist_core):
#     response = mist_core.add_schedule(api_token='', name='dummy',
#                                       schedule_type='one=off').post()
#     assert_response_forbidden(response)
#     print "Success!!!"
#
#
# def test_add_schedule_wrong_api_token(pretty_print, mist_core):
#     response = mist_core.add_schedule(api_token='dummy', name='dummy',
#                                       schedule_type='one=off').post()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# # def test_add_schedule_missing_parameter(pretty_print, mist_core, owner_api_token):
# #     response = mist_core.add_schedule(api_token=owner_api_token, name='dummy').post()
# #     assert_response_bad_request(response)
# #     print "Success!!!"
#
#
# def test_delete_schedule_no_api_token(pretty_print, mist_core):
#     response = mist_core.delete_schedule(api_token='', schedule_id='dummy').delete()
#     assert_response_forbidden(response)
#     print "Success!!!"
#
#
# def test_delete_schedule_wrong_api_token(pretty_print, mist_core):
#     response = mist_core.delete_schedule(api_token='dummy', schedule_id='dummy').delete()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_delete_schedule_wrong_schedule_id(pretty_print, mist_core, owner_api_token):
#     response = mist_core.delete_schedule(api_token=owner_api_token, schedule_id='dummy').delete()
#     assert_response_not_found(response)
#     print "Success!!!"
#
#
# def test_edit_schedule_no_api_token(pretty_print, mist_core):
#     response = mist_core.edit_schedule(api_token='', schedule_id='dummy').patch()
#     assert_response_forbidden(response)
#     print "Success!!!"
#
#
# def test_edit_schedule_wrong_api_token(pretty_print, mist_core):
#     response = mist_core.edit_schedule(api_token='dummy', schedule_id='dummy').patch()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_edit_schedule_wrong_schedule_id(pretty_print, mist_core, owner_api_token):
#     response = mist_core.edit_schedule(api_token=owner_api_token, schedule_id='dummy').patch()
#     assert_response_not_found(response)
#     print "Success!!!"
#
#
# def test_show_schedule_no_api_token(pretty_print, mist_core):
#     response = mist_core.show_schedule(api_token='', schedule_id='dummy').get()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_show_schedule_wrong_api_token(pretty_print, mist_core):
#     response = mist_core.show_schedule(api_token='dummy', schedule_id='dummy').get()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_show_schedule_wrong_schedule_id(pretty_print, mist_core, owner_api_token):
#     response = mist_core.show_schedule(api_token=owner_api_token, schedule_id='').get()
#     assert_response_not_found(response)
#     print "Success!!!"

############################################################################
#                         Functional Testing                               #
############################################################################

@pytest.mark.incremental
class TestSchedulesFunctionality:

    def test_check_machines_state(self, pretty_print, mist_core, owner_api_token, cache):
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

        for i in range(1,3):
            name = 'api_test_machine_%d' % random.randint(1, 200)
            cache.set('machine_name', name)

            response = mist_core.create_machine(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token,
                                                key_id='', name=name, provider='', location='',
                                                image=cache.get('image_id', ''), size='').post()
            assert_response_ok(response)
            cache.set('machine_%d_id' %i, response.json()['id'])
            import ipdb;ipdb.set_trace()





        response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()

        for machine in response.json():
            if cache.get('machine_name','') in machine['name']:
                cache.set('machine_1_id', machine['uuid'])
                assert machine['state'] == 'running',\
                    "Machine's state is not running in the beginning of the tests"
        #     if 'api_test_machine_2' in machine['name']:
        #         cache.set('machine2_id', machine['uuid'])
        #         assert machine['state'] == 'running',\
        #             "Machine's state is not running in the beginning of the tests"
        #         response = mist_core.set_machine_tags(api_token=owner_api_token,
        #                                               cloud_id=cache.get('cloud_id', ''),
        #                                               machine_id=machine['uuid'],
        #                                               tags={'key': 'schedule_test', 'value': ''}).post()
        #         assert_response_ok(response)
        #     if 'api_test_machine_3' in machine['name']:
        #         cache.set('machine3_id', machine['uuid'])
        #         assert machine['state'] == 'running',\
        #             "Machine's state is not running in the beginning of the tests"

        print "Success!!!"

#     def test_add_one_off_schedule_missing_schedule_entry(self, pretty_print, mist_core, owner_api_token, cache):
#         machines_uuids = []
#         machines_uuids.append(cache.get('machine_1_id',''))
#         response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule1',
#                                           action='stop', schedule_type='one_off',
#                                           machines_uuids = machines_uuids).post()
#         assert_response_bad_request(response)
#         print "Success!!!"
#
# # below test should write to a file...
#     def test_add_interval_schedule_ok(self, pretty_print, mist_core, owner_api_token, cache):
#         response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()
#         assert_response_ok(response)
#         machines_uuids = []
#         machines_uuids.append(cache.get('machine_1_id', ''))
#         response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule1',
#                                           action='stop', schedule_type='interval',
#                                           machines_uuids=machines_uuids, run_immediately=True,
#                                           schedule_entry={'every': 10, 'period':'hours'}).post()
#         assert_response_ok(response)
#         cache.set('schedule_id', response.json()['id'])
#         response = mist_core.list_schedules(api_token=owner_api_token).get()
#         assert_response_ok(response)
#         assert len(response.json()) == 1
#         print "Success"
#
#     def test_add_interval_schedule_tags_ok(self, pretty_print, mist_core, owner_api_token):
#         response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule2',
#                                           action='stop', schedule_type='interval',
#                                           machines_tags={'schedule_test': ''},
#                                           run_immediately=True,
#                                           schedule_entry={'every': 20, 'period': 'minutes'}).post()
#         assert_response_ok(response)
#         response = mist_core.list_schedules(api_token=owner_api_token).get()
#         assert_response_ok(response)
#         assert len(response.json()) == 2
#         print "Success"
#
#     def test_add_one_off_schedule_ok(self, pretty_print, mist_core, cache, owner_api_token):
#         date_now = datetime.datetime.now().replace(microsecond=0)
#         scheduled_date = date_now + datetime.timedelta(seconds=10)
#         machines_uuids = []
#         machines_uuids.append(cache.get('machine_1_id', ''))
#         response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule3',
#                                           action='stop', schedule_type='one_off',
#                                           machines_uuids=machines_uuids,
#                                           schedule_entry=str(scheduled_date)).post()
#         assert_response_ok(response)
#         response = mist_core.list_schedules(api_token=owner_api_token).get()
#         assert_response_ok(response)
#         assert len(response.json()) == 3
#         print "Success"
#
#     def test_add_schedule_run_immediately_ok(self, pretty_print, mist_core, owner_api_token, cache):
#         machines_uuids = []
#         machines_uuids.append(cache.get('machine3_id', ''))
#         response = mist_core.add_schedule(api_token=owner_api_token, name='RunImmediatelySchedule',
#                                           action='stop', schedule_type='interval',
#                                           machines_uuids=machines_uuids,
#                                           run_immediately=True,
#                                           schedule_entry={'every': 20, 'period': 'minutes'}).post()
#         assert_response_ok(response)
#         print "Success"
#
#     def test_add_crontab_schedule_ok(self, pretty_print, mist_core, cache, owner_api_token):
#         machines_uuids = []
#         machines_uuids.append(cache.get('machine2_id', ''))
#         response = mist_core.add_schedule(api_token=owner_api_token, name='CrontabSchedule',
#                                           action='start', schedule_type='crontab',
#                                           machines_uuids=machines_uuids,
#                                           schedule_entry={'minute': '*', 'hour': '*', 'day_of_week': '*',
#                                                           'day_of_month': '*', 'month_of_year': '*'}).post()
#         assert_response_ok(response)
#         cache.set('crontab_schedule_id', response.json()['id'])
#         response = mist_core.list_schedules(api_token=owner_api_token).get()
#         assert_response_ok(response)
#         assert len(response.json()) == 5
#         print "Success"
#
#     def test_edit_crontab_schedule_ok(self, pretty_print, mist_core, cache, owner_api_token):
#         response = mist_core.edit_schedule(api_token=owner_api_token, schedule_id=cache.get('crontab_schedule_id', ''),
#                                            data={'action': 'stop'}).patch()
#         assert_response_ok(response)
#         print "Success!!!"
#
#     def test_add_one_off_schedule_tags_ok(self, pretty_print, mist_core, owner_api_token):
#         date_now = datetime.datetime.now().replace(microsecond=0)
#         scheduled_date = date_now + datetime.timedelta(seconds=10)
#         response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule4',
#                                           action='stop', schedule_type='one_off',
#                                           machines_tags={'schedule_test': ''},
#                                           run_immediately=True,
#                                           schedule_entry=str(scheduled_date)).post()
#         assert_response_ok(response)
#         response = mist_core.list_schedules(api_token=owner_api_token).get()
#         assert_response_ok(response)
#         assert len(response.json()) == 6
#         print "Success"
#
#     def test_add_schedule_dup_name(self, pretty_print, mist_core, owner_api_token, cache):
#         machines_uuids = []
#         machines_uuids.append(cache.get('machine_1_id', ''))
#         now = datetime.datetime.now()
#         response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule1',
#                                           action='stop', schedule_type='one_off',
#                                           machines_uuids=machines_uuids, schedule_entry=str(now)).post()
#         assert_response_conflict(response)
#         print "Success!!!"
#
#     def test_add_one_off_schedule_wrong_date(self, pretty_print, mist_core, owner_api_token, cache):
#         machines_uuids = []
#         machines_uuids.append(cache.get('machine_1_id', ''))
#         date_now = datetime.datetime.now().replace(microsecond=0)
#         response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule5',
#                                           action='stop', schedule_type='one_off',
#                                           machines_uuids=machines_uuids, schedule_entry=str(date_now)).post()
#         assert_response_bad_request(response)
#         past_date = date_now - datetime.timedelta(seconds=10)
#         response = mist_core.add_schedule(api_token=owner_api_token, name='TestSchedule5',
#                                           action='stop', schedule_type='one_off',
#                                           machines_uuids=machines_uuids, schedule_entry=str(past_date)).post()
#         assert_response_bad_request(response)
#         print "Success!!!"
#
#     def test_add_disabled_schedule(self, pretty_print, mist_core, owner_api_token, cache):
#         machines_uuids = []
#         machines_uuids.append(cache.get('machine_1_id', ''))
#         response = mist_core.add_schedule(api_token=owner_api_token, name='DisabledSchedule',
#                                           action='stop', schedule_type='interval', task_enabled=False,
#                                           machines_uuids=machines_uuids, run_immediately=True,
#                                           schedule_entry={'every': 2, 'period': 'minutes'}).post()
#         assert_response_ok(response)
#         cache.set('disabled_schedule_id', response.json()['id'])
#         print "Success"
#
#     def test_delete_schedule_ok(self, pretty_print, mist_core, owner_api_token, cache):
#         response = mist_core.delete_schedule(api_token=owner_api_token,
#                                              schedule_id=cache.get('schedule_id', '')).delete()
#         assert_response_ok(response)
#         response = mist_core.delete_schedule(api_token=owner_api_token,
#                                              schedule_id=cache.get('schedule_id', '')).delete()
#         assert_response_not_found(response)
#         print "Success!!!"
#
#     def test_total_run_counts_disabled_schedule(self, pretty_print, mist_core, owner_api_token, cache):
#         response = mist_core.show_schedule(api_token=owner_api_token,
#                                            schedule_id=cache.get('disabled_schedule_id', '')).get()
#         assert_response_ok(response)
#         assert response.json()['total_run_count'] == 0, "Schedule run although it was disabled!!!"
#         print "Success!!!"
#
#     def test_check_schedules(self, pretty_print, mist_core, owner_api_token, cache, schedules_cleanup):
#         sleep(60)
#         response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()
#         for machine in response.json():
#             if 'api_test_machine' in machine['name']:
#                 assert machine['state'] == 'stopped', "Machine'state is not stopped after schedule run"
#         print "Success"
