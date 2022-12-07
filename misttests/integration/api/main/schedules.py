from misttests.integration.api.helpers import *
from misttests.config import safe_get_var, DEFAULT_IMAGE_NAME
from misttests import config
from time import sleep

import pytest
import datetime

############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_schedules(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.list_schedules(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print("Success!!!")


def test_list_schedules_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.list_schedules(api_token='').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_list_schedules_wrong_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.list_schedules(api_token='dummy').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_add_schedule_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.add_schedule(api_token='', name='dummy',
                                      schedule_type='one=off',
                                      selectors=[]).post()
    assert_response_forbidden(response)
    print("Success!!!")


def test_add_schedule_wrong_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.add_schedule(api_token='dummy', name='dummy',
                                      schedule_type='one=off',
                                      selectors=[]).post()
    assert_response_unauthorized(response)
    print("Success!!!")


# def test_add_schedule_missing_parameter(pretty_print, mist_api_v1, owner_api_token):
#     response = mist_api_v1.add_schedule(api_token=owner_api_token, name='dummy').post()
#     assert_response_bad_request(response)
#     print "Success!!!"


def test_delete_schedule_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.delete_schedule(api_token='', schedule_id='dummy').delete()
    assert_response_forbidden(response)
    print("Success!!!")


def test_delete_schedule_wrong_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.delete_schedule(api_token='dummy', schedule_id='dummy').delete()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_delete_schedule_wrong_schedule_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.delete_schedule(api_token=owner_api_token, schedule_id='dummy').delete()
    assert_response_not_found(response)
    print("Success!!!")


def test_edit_schedule_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.edit_schedule(api_token='', schedule_id='dummy').patch()
    assert_response_forbidden(response)
    print("Success!!!")


def test_edit_schedule_wrong_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.edit_schedule(api_token='dummy', schedule_id='dummy').patch()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_edit_schedule_wrong_schedule_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.edit_schedule(api_token=owner_api_token, schedule_id='dummy').patch()
    assert_response_not_found(response)
    print("Success!!!")


def test_show_schedule_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.show_schedule(api_token='', schedule_id='dummy').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_show_schedule_wrong_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.show_schedule(api_token='dummy', schedule_id='dummy').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_show_schedule_wrong_schedule_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.show_schedule(api_token=owner_api_token, schedule_id='dummy').get()
    assert_response_not_found(response)
    print("Success!!!")

############################################################################
#                         Functional Testing                               #
############################################################################

@pytest.mark.incremental
class TestSchedulesFunctionality:

    def test_create_resources(self, pretty_print, mist_api_v1, owner_api_token, cache):
        if config.LOCAL:
            response = mist_api_v1.add_cloud(name='Docker', provider='docker', api_token=owner_api_token,
                                       docker_host=config.LOCAL_DOCKER,
                                       docker_port='2375').post()
        else:
            response = mist_api_v1.add_cloud(name='Docker', provider='docker', api_token=owner_api_token,
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
        cache.set('docker_id', response.json()['id'])

        response = mist_api_v1.list_images(cloud_id=cache.get('docker_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        for image in response.json():
            if DEFAULT_IMAGE_NAME in image['name']:
                cache.set('image_id', image['id'])
                break

        for i in range(1,4):
            name = 'api_test_machine_%d' % random.randint(1, 10000000)
            cache.set('machine_%d_name' %i, name)
            response = mist_api_v1.create_machine(cloud_id=cache.get('docker_id', ''), api_token=owner_api_token,
                                                key_id='', name=name, provider='', location='',
                                                image=cache.get('image_id', ''), size='').post()
            assert_response_ok(response)

        sleep(10)
        response = mist_api_v1.list_machines(cloud_id=cache.get('docker_id', ''), api_token=owner_api_token).get()

        for machine in response.json():
            if cache.get('machine_1_name','') in machine['name']:
                cache.set('machine_1_id', machine['id'])
                assert machine['state'] == 'running',\
                    "Machine's state is not running in the beginning of the tests"
            if cache.get('machine_2_name','') in machine['name']:
                cache.set('machine_2_id', machine['id'])
                assert machine['state'] == 'running',\
                    "Machine's state is not running in the beginning of the tests"
                # response = mist_api_v1.set_machine_tags(api_token=owner_api_token,
                #                                       cloud_id=cache.get('docker_id', ''),
                #                                       machine_id=machine['uuid'],
                #                                       tags={'key': 'schedule_test', 'value': ''}).post()
                # assert_response_ok(response)
            if cache.get('machine_3_name','') in machine['name']:
                cache.set('machine_3_id', machine['id'])
                assert machine['state'] == 'running',\
                    "Machine's state is not running in the beginning of the tests"

        print("Success!!!")

    def test_add_one_off_schedule_missing_schedule_entry(self, pretty_print, mist_api_v1, owner_api_token, cache):
        machine_ids = []
        machine_ids.append(cache.get('machine_1_id', ''))
        selectors = [{"type": "machines", "ids": machine_ids}]
        response = mist_api_v1.add_schedule(api_token=owner_api_token,
                                          name='TestSchedule1',
                                          action='stop',
                                          schedule_type='one_off',
                                          selectors=selectors).post()
        assert_response_bad_request(response)
        print("Success!!!")

    def test_add_interval_schedule_run_immediately_ok(self, pretty_print, mist_api_v1, owner_api_token, cache):
        response = mist_api_v1.list_machines(cloud_id=cache.get('docker_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        machine_ids = []
        machine_ids.append(cache.get('machine_1_id', ''))
        selectors = [{"type":"machines","ids":machine_ids}]
        response = mist_api_v1.add_schedule(api_token=owner_api_token, name='TestSchedule1',
                                          action='stop', schedule_type='interval',
                                          selectors=selectors,
                                          run_immediately=True,
                                          schedule_entry={'every': 10, 'period':'hours'}).post()

        assert_response_ok(response)
        response = mist_api_v1.list_schedules(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 1
        print("Success")

    # # TODO: check above tagged machine
    # def test_add_interval_schedule_tags_ok(self, pretty_print, mist_api_v1, owner_api_token):
    #     selectors = [{"type":"tags","include":{'schedule_test': ''}}]
    #     response = mist_api_v1.add_schedule(api_token=owner_api_token, name='TestSchedule2',
    #                                       action='stop', schedule_type='interval',
    #                                       selectors=selectors,
    #                                       run_immediately=True,
    #                                       schedule_entry={'every': 20, 'period': 'minutes'}).post()
    #     assert_response_ok(response)
    #     response = mist_api_v1.list_schedules(api_token=owner_api_token).get()
    #     assert_response_ok(response)
    #     assert len(response.json()) == 2
    #     print "Success"

    def test_add_one_off_schedule_ok(self, pretty_print, mist_api_v1,
                                     cache, owner_api_token):
        date_now = datetime.datetime.now().replace(microsecond=0)
        scheduled_date = date_now + datetime.timedelta(seconds=10)
        machine_ids = []
        assert cache.get('machine_2_id', '') != ''
        machine_ids.append(cache.get('machine_2_id', ''))
        selectors = [{"type": "machines", "ids": machine_ids}]

        response = mist_api_v1.add_schedule(api_token=owner_api_token,
                                          name='TestSchedule3',
                                          action='stop',
                                          schedule_type='one_off',
                                          selectors=selectors,
                                          schedule_entry=str(scheduled_date)
                                          ).post()
        assert_response_ok(response)
        response = mist_api_v1.list_schedules(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 2
        print("Success")

    def test_add_crontab_schedule_ok(self, pretty_print, mist_api_v1,
                                     cache, owner_api_token):
        machine_ids = []
        machine_ids.append(cache.get('machine_3_id', ''))
        selectors = [{"type": "machines", "ids": machine_ids}]

        response = mist_api_v1.add_schedule(api_token=owner_api_token,
                                          name='CrontabSchedule',
                                          action='start', schedule_type='crontab',
                                          selectors=selectors,
                                          schedule_entry={'minute': '*',
                                                          'hour': '*',
                                                          'day_of_week': '*',
                                                          'day_of_month': '*',
                                                          'month_of_year': '*'}
                                          ).post()
        assert_response_ok(response)
        cache.set('crontab_schedule_id', response.json()['id'])
        response = mist_api_v1.list_schedules(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 3
        print("Success")

    def test_edit_crontab_schedule_ok(self, pretty_print, mist_api_v1,
                                      cache, owner_api_token):
        response = mist_api_v1.edit_schedule(api_token=owner_api_token,
                                           schedule_id=cache.get(
                                               'crontab_schedule_id', ''),
                                                data=json.dumps({
                                                    'action': 'stop',
                                                    'schedule_type': 'crontab',
                                                    'schedule_entry':{
                                                        'minute': '*',
                                                        'hour': '*',
                                                        'day_of_week': '*',
                                                        'day_of_month': '*',
                                                        'month_of_year': '*'
                                                    }
                                                })
                                            ).patch()
        assert_response_ok(response)
        print("Success!!!")

# TODO: below does not apply to any machines yet
    def test_add_one_off_schedule_tags_ok(self, pretty_print, mist_api_v1, owner_api_token, cache):
        date_now = datetime.datetime.now().replace(microsecond=0)
        scheduled_date = date_now + datetime.timedelta(seconds=10)
        selectors = [{"type": "tags", "include": {'schedule_test': ''}}]
        response = mist_api_v1.add_schedule(api_token=owner_api_token, name='TestSchedule4',
                                          action='stop', schedule_type='one_off',
                                          selectors=selectors,
                                          run_immediately=True,
                                          schedule_entry=str(scheduled_date)).post()
        assert_response_ok(response)
        cache.set('schedule_id', response.json()['id'])
        response = mist_api_v1.list_schedules(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 4
        print("Success")

    def test_add_schedule_dup_name(self, pretty_print, mist_api_v1,
                                   owner_api_token, cache):
        machine_ids = []
        machine_ids.append(cache.get('machine_1_id', ''))
        selectors = [{"type": "machines", "ids": machine_ids}]

        now = datetime.datetime.now()
        response = mist_api_v1.add_schedule(api_token=owner_api_token,
                                          name='TestSchedule1',
                                          action='stop',
                                          schedule_type='one_off',
                                          selectors=selectors,
                                          schedule_entry=str(now)).post()
        assert_response_conflict(response)
        print("Success!!!")

    def test_add_one_off_schedule_wrong_date(self, pretty_print, mist_api_v1,
                                             owner_api_token, cache):
        machine_ids = []
        machine_ids.append(cache.get('machine_1_id', ''))
        date_now = datetime.datetime.now().replace(microsecond=0)
        selectors = [{"type": "machines", "ids": machine_ids}]
        response = mist_api_v1.add_schedule(api_token=owner_api_token,
                                          name='TestSchedule5',
                                          action='stop',
                                          schedule_type='one_off',
                                          selectors=selectors,
                                          schedule_entry=str(date_now)).post()
        assert_response_bad_request(response)
        past_date = date_now - datetime.timedelta(seconds=10)
        response = mist_api_v1.add_schedule(api_token=owner_api_token,
                                          name='TestSchedule5',
                                          action='stop',
                                          schedule_type='one_off',
                                          selectors=selectors,
                                          schedule_entry=str(past_date)).post()
        assert_response_bad_request(response)
        print("Success!!!")

    def test_add_disabled_schedule(self, pretty_print, mist_api_v1,
                                   owner_api_token, cache):
        machine_ids = []
        machine_ids.append(cache.get('machine_1_id', ''))
        selectors = [{"type": "machines", "ids": machine_ids}]
        response = mist_api_v1.add_schedule(api_token=owner_api_token,
                                          name='DisabledSchedule',
                                          action='stop',
                                          schedule_type='interval',
                                          task_enabled=False,
                                          run_immediately=True,
                                          selectors=selectors,
                                          schedule_entry=
                                          {'every': 2, 'period': 'minutes'}
                                          ).post()

        assert_response_ok(response)
        cache.set('disabled_schedule_id', response.json()['id'])
        print("Success")

    def test_delete_schedule_ok(self, pretty_print, mist_api_v1, owner_api_token, cache):
        response = mist_api_v1.delete_schedule(api_token=owner_api_token,
                                             schedule_id=cache.get('schedule_id', '')).delete()
        assert_response_ok(response)
        response = mist_api_v1.delete_schedule(api_token=owner_api_token,
                                             schedule_id=cache.get('schedule_id', '')).delete()
        assert_response_not_found(response)
        print("Success!!!")

    def test_total_run_counts_disabled_schedule(self, pretty_print, mist_api_v1, owner_api_token, cache):
        response = mist_api_v1.show_schedule(api_token=owner_api_token,
                                           schedule_id=cache.get('disabled_schedule_id', '')).get()
        assert_response_ok(response)
        assert response.json()['total_run_count'] == 0, "Schedule run although it was disabled!!!"
        print("Success!!!")

    def test_check_schedules(self, pretty_print, mist_api_v1, owner_api_token, cache, schedules_cleanup):
        print("Sleeping to check state of machines...")
        sleep(120)
        response = mist_api_v1.list_machines(cloud_id=cache.get('docker_id', ''), api_token=owner_api_token).get()
        for machine in response.json():
            if cache.get('machine_1_name', '') in machine['name']:
                assert machine['state'] == 'stopped', "Machine'state is not stopped although schedule was supposed to run immediately"
            if cache.get('machine_2_name', '') in machine['name']:
                assert machine['state'] == 'stopped', "Machine'state is not stopped although schedule was supposed to run after 10 secs"
            if cache.get('machine_3_name', '') in machine['name']:
                assert machine['state'] == 'stopped', "Machine'state is not stopped although schedule was supposed to run after 1 min"
        print("Success")
