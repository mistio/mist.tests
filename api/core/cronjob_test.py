import sys
import json
import pprint
import pytest

from tests.api.utils import *


def test_001_get_list_schedules_without_token(pretty_print, mist_core,
                                              owner_api_token):
    print ("\n>>> GETing /schedules to get a list of "
           "all schedules without token")
    response = mist_core.list_schedules_entries(api_token='').get()
    assert_response_unauthorized(response)
    print "Success!!!!"


def test_002_get_list_schedules_with_token(pretty_print, mist_core,
                                           owner_api_token):
    print "\n>>> GETing /schedules to get a list of all schedules"
    response = mist_core.list_schedules_entries(api_token=
                                                owner_api_token).get()
    assert_response_ok(response)
    print "Got a list of schedules: \n"
    pprint.pprint(response.json(), indent=3, stream=sys.stdout)
    print "Success!!!!"


def test_003_check_add_schedule_entry_no_name(pretty_print,
                                             mist_core,
                                             random_bash_script,
                                             expires,
                                             scheduled_machines,
                                             owner_api_token):
    print "\n>>> POSTing /schedules to add a schedule without name"
    entry = {"every": 5, "period": "minutes"}

    response = mist_core.add_schedule_entry(name='',
                                            script_id=random_bash_script['id'],
                                            scheduled_machines=
                                            scheduled_machines,
                                            enabled=True,
                                            expires=expires,
                                            schedule_type='interval',
                                            schedule_entry=json.dumps(entry),
                                            api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_004_check_add_schedule_entry_no_schedule_type(pretty_print,
                                                      mist_core,
                                                      random_bash_script,
                                                      expires,
                                                      scheduled_machines,
                                                      owner_api_token):
    print "\n>>> POSTing /schedules to add a schedule without schedule_type"
    entry = {"every": 5, "period": "minutes"}

    response = mist_core.add_schedule_entry(name='check_failure',
                                            script_id=random_bash_script['id'],
                                            scheduled_machines=
                                            scheduled_machines,
                                            enabled=True,
                                            expires=expires,
                                            schedule_type='',
                                            schedule_entry=json.dumps(entry),
                                            api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_005_check_add_schedule_entry_with_expired_date(pretty_print,
                                                        mist_core,
                                                        random_bash_script,
                                                        expired,
                                                        scheduled_machines,
                                                        owner_api_token):
    print ("\n>>> POSTing /schedules to add a "
           "schedule with expired expiration date")

    response = mist_core.add_schedule_entry(name='check_failure',
                                            script_id=random_bash_script['id'],
                                            scheduled_machines=
                                            scheduled_machines,
                                            enabled=True,
                                            schedule_type='one_off',
                                            schedule_entry=expired,
                                            api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_006_check_add_schedule_entry_wrong_schedule_entry(pretty_print,
                                                           mist_core,
                                                           random_bash_script,
                                                           expired,
                                                           scheduled_machines,
                                                           owner_api_token):
    print ("\n>>> POSTing /schedules to add a schedule "
           "with wrong schedule entry")

    response = mist_core.add_schedule_entry(name='check_failure',
                                            script_id=random_bash_script['id'],
                                            scheduled_machines=
                                            scheduled_machines,
                                            enabled=True,
                                            schedule_type='one_off',
                                            schedule_entry='bla',
                                            api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_007_check_add_schedule_entry_wrong_script_id(pretty_print,
                                                      mist_core,
                                                      random_bash_script,
                                                      expired,
                                                      scheduled_machines,
                                                      owner_api_token):
    print "\n>>> POSTing /schedules to add a schedule with wrong script_id"

    response = mist_core.add_schedule_entry(name='check_failure',
                                            script_id=random_bash_script['id'],
                                            scheduled_machines=
                                            scheduled_machines,
                                            enabled=True,
                                            schedule_type='one_off',
                                            schedule_entry='bla',
                                            api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_008_check_add_schedule_entry_with_wrong_api_token(pretty_print,
                                                           mist_core,
                                                           random_bash_script,
                                                           expired,
                                                           scheduled_machines,
                                                           owner_api_token):
    print "\n>>> POSTing /schedules to add a schedule with wrong script_id"

    response = mist_core.add_schedule_entry(name='check_failure',
                                            script_id=random_bash_script['id'],
                                            scheduled_machines=
                                            scheduled_machines,
                                            enabled=True,
                                            schedule_type='one_off',
                                            schedule_entry='bla',
                                            api_token=
                                            owner_api_token[:-1]).post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_009_show_schedule_entry_wrong_api_token(pretty_print, mist_core,
                                                owner_api_token):
    print "\n>>>  GETing /schedules to show a schedule with wrong api token"
    response = mist_core.show_schedules_entry(
        schedule_id='',
        api_token=owner_api_token[:-1]).get()
    assert_response_not_found(response)
    print "Success!!!!"


def test_010_show_schedule_entry_schedule_id(pretty_print, mist_core,
                                             owner_api_token):
    print "\n>>>  GETing /schedules to show a schedule with wrong schedule id"
    response = mist_core.show_schedules_entry(
        schedule_id='bla',
        api_token=owner_api_token).get()
    assert_response_not_found(response)
    print "Success!!!!"


@pytest.mark.incremental
class TestSimpleUserscheduleCycle:

    def test_add_schedule_entry_interval(self, pretty_print, cache,
                                         mist_core,
                                         random_bash_script,
                                         expires,
                                         scheduled_machines,
                                         owner_api_token):
        print ("\n>>> POSTing /schedules to add a schedule "
               "with correct params, type interval")
        entry = {"every": 5, "period": "minutes"}

        response = mist_core.add_schedule_entry(name='check_add_interval',
                                                script_id=
                                                random_bash_script['id'],
                                                scheduled_machines=
                                                scheduled_machines,
                                                enabled=True,
                                                expires=expires,
                                                schedule_type='interval',
                                                schedule_entry=
                                                json.dumps(entry),
                                                api_token=
                                                owner_api_token).post()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        assert_is_not_none(rjson.get('id'),
                           "Did not get an id back in the response")
        cache.set('schedule/schedule_id_interval', rjson['id'])
        print "Success!!!"

    def test_add_schedule_entry_crontab(self, pretty_print, cache,
                                        mist_core,
                                        random_bash_script,
                                        expires,
                                        scheduled_machines,
                                        owner_api_token):
        print ("\n>>> POSTing /schedules to add a schedule "
               "with correct params, type crontab")
        entry = {'minute': '*/10'}

        response = mist_core.add_schedule_entry(name='check_add_cron',
                                                script_id=
                                                random_bash_script['id'],
                                                scheduled_machines=
                                                scheduled_machines,
                                                enabled=True,
                                                expires=expires,
                                                schedule_type='crontab',
                                                schedule_entry=
                                                json.dumps(entry),
                                                api_token=
                                                owner_api_token).post()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        assert_is_not_none(rjson.get('id'),
                           "Did not get an id back in the response")
        cache.set('schedule/schedule_id_crontab', rjson['id'])
        print "Success!!!"

    def test_add_schedule_entry_one_off(self, pretty_print, cache,
                                       mist_core,
                                       random_bash_script,
                                       expires,
                                       scheduled_machines,
                                       owner_api_token):
        print ("\n>>> POSTing /schedules to add a "
               "schedule with correct params,  type one-off")
        response = mist_core.add_schedule_entry(name='check_add_one_off',
                                                script_id=
                                                random_bash_script['id'],
                                                scheduled_machines=
                                                scheduled_machines,
                                                enabled=True,
                                                expires=expires,
                                                schedule_type='one_off',
                                                schedule_entry=expires,
                                                api_token=
                                                owner_api_token).post()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        assert_is_not_none(rjson.get('id'),
                           "Did not get an id back in the response")
        cache.set('schedule/schedule_id_one_off', rjson['id'])
        print "Success!!!"

    def test_add_schedule_entry_action(self, pretty_print, cache,
                                       mist_core,
                                       random_bash_script,
                                       expires,
                                       scheduled_machines,
                                       owner_api_token):
        print "\n>>> POSTing /schedules to add a schedule " \
              "with correct params, for an action"
        response = mist_core.add_schedule_entry(name='check_add_action',
                                                action='reboot',
                                                scheduled_machines=
                                                scheduled_machines,
                                                enabled=True,
                                                schedule_type='one_off',
                                                schedule_entry=expires,
                                                api_token=
                                                owner_api_token).post()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        assert_is_not_none(rjson.get('id'),
                           "Did not get an id back in the response")
        cache.set('schedule/schedule_id_action', rjson['id'])
        print "Success!!!"

    def test_edit_schedule_entry_crontab_expired_date(self, pretty_print,
                                                      mist_core,
                                                      scheduled_machines,
                                                      random_bash_script,
                                                      cache,
                                                      expired,
                                                      owner_api_token):

        print ("\n>>>  PUTing /schedules to edit a schedule, with expired "
               "expiration date")
        entry = {'minute': '*/10', 'hour': '*/11'}

        schedule_id = cache.get('schedule/schedule_id_crontab', '')
        response = mist_core.edit_schedule_entry(name='check_edit_to cron',
                                                 script_id=
                                                 random_bash_script['id'],
                                                 scheduled_machines=
                                                 scheduled_machines,
                                                 enabled=True,
                                                 expires=expired,
                                                 schedule_type='crontab',
                                                 schedule_entry=
                                                 json.dumps(entry),
                                                 schedule_id=schedule_id,
                                                 api_token=
                                                 owner_api_token).patch()
        assert_response_bad_request(response)
        print "Success!!!"

    def test_edit_schedule_entry_crontab_wrong_script_id(self, pretty_print,
                                                         mist_core,
                                                         scheduled_machines,
                                                         random_bash_script,
                                                         cache,
                                                         expired,
                                                         owner_api_token):

        print ("\n>>>  PUTing /schedules to edit a schedule, "
               "with wrong script id date")
        entry = {'minute': '*/10', 'hour': '*/11'}

        schedule_id = cache.get('schedule/schedule_id_crontab', '')
        response = mist_core.edit_schedule_entry(name='check_edit_to cron',
                                                 script_id=
                                                 random_bash_script['id'][:-1],
                                                 scheduled_machines=
                                                 scheduled_machines,
                                                 enabled=True,
                                                 expires=expired,
                                                 schedule_type='crontab',
                                                 schedule_entry=
                                                 json.dumps(entry),
                                                 schedule_id=schedule_id,
                                                 api_token=
                                                 owner_api_token).patch()
        assert_response_not_found(response)
        print "Success!!!"

    def test_edit_schedule_entry_wrong_schedule(self, pretty_print, mist_core,
                                                scheduled_machines,
                                                random_bash_script,
                                                cache,
                                                expired,
                                                owner_api_token):

        print ("\n>>>  PUTing /schedules to edit a schedule, "
               "with wrong schedule entry")
        entry = {'minute': '*/10/of bla', 'hour': '*/11'}

        schedule_id = cache.get('schedule/schedule_id_crontab', '')
        response = mist_core.edit_schedule_entry(name='check_edit_to cron',
                                                 script_id=
                                                 random_bash_script['id'],
                                                 scheduled_machines=
                                                 scheduled_machines,
                                                 enabled=True,
                                                 expires=expired,
                                                 schedule_type='crontab',
                                                 schedule_entry=
                                                 json.dumps(entry),
                                                 schedule_id=
                                                 schedule_id,
                                                 api_token=
                                                 owner_api_token).patch()
        assert_response_bad_request(response)
        print "Success!!!"

    def test_edit_schedule_entry_interval_to_crontab(self, pretty_print,
                                                     mist_core,
                                                     scheduled_machines,
                                                     random_bash_script,
                                                     cache,
                                                     expires,
                                                     owner_api_token):

        print ("\n>>>  PUTing /schedules to edit a schedule, "
               "interval --> crontab")
        entry = {'minute': '*/10', 'hour': '*/11'}

        schedule_id = cache.get('schedule/schedule_id_crontab', '')
        response = mist_core.edit_schedule_entry(name='check_edit_to cron',
                                                 script_id=
                                                 random_bash_script['id'],
                                                 scheduled_machines=
                                                 scheduled_machines,
                                                 enabled=True,
                                                 expires=expires,
                                                 schedule_type='crontab',
                                                 schedule_entry=
                                                 json.dumps(entry),
                                                 schedule_id=schedule_id,
                                                 api_token=
                                                 owner_api_token).patch()
        assert_response_ok(response)
        print "Success!!!"

    def test_edit_schedule_entry_crontab_to_one_off(self, pretty_print,
                                                    mist_core,
                                                    random_bash_script, cache,
                                                    expires,
                                                    owner_api_token,
                                                    scheduled_machines):

        print "\n>>>  PUTing /schedules to edit a schedule, crontab--> one_off"
        schedule_id = cache.get('schedule/schedule_id_crontab', '')
        response = mist_core.edit_schedule_entry(name='check_edit_one_off',
                                                 script_id=
                                                 random_bash_script['id'],
                                                 scheduled_machines=
                                                 scheduled_machines,
                                                 enabled=True,
                                                 schedule_type='one_off',
                                                 schedule_entry=expires,
                                                 schedule_id=schedule_id,
                                                 api_token=
                                                 owner_api_token).patch()
        assert_response_ok(response)
        print "Success!!!"

    def test_018_check_edit_schedule_entry(self, pretty_print, mist_core,
                                           scheduled_machines,
                                           random_bash_script,expires, cache,
                                           owner_api_token):
        print "\n>>>  PUTing /schedules to edit a schedule, action--> script"
        schedule_id = cache.get('schedule/schedule_id_action', '')
        response = mist_core.edit_schedule_entry(name='check_edit_script',
                                                 script_id=
                                                 random_bash_script['id'],
                                                 scheduled_machines=
                                                 scheduled_machines,
                                                 enabled=True,
                                                 schedule_type='one_off',
                                                 schedule_entry=expires,
                                                 schedule_id=schedule_id,
                                                 api_token=
                                                 owner_api_token).patch()
        assert_response_bad_request(response)
        print "Success!!!"

    def test_show_schedule_entry(self, pretty_print, mist_core,
                                 cache, owner_api_token):

        print "\n>>>  GETing /schedules to show a schedule with correct id"
        response = mist_core.show_schedules_entry(
            schedule_id=cache.get('schedule/schedule_id_interval', ''),
            api_token=owner_api_token).get()
        assert_response_ok(response)
        print "Success!!!!"

    def test_check_delete_schedule_entry(self, pretty_print, mist_core,
                                         cache, owner_api_token):

        print ("\n>>>  DELETEing /schedules to delete a schedule "
               "with correct _id")

        response = mist_core.delete_schedule(
            schedule_id=cache.get('schedule/schedule_id_interval', ''),
            api_token=owner_api_token).delete()
        assert_response_ok(response)

        response = mist_core.delete_schedule(
            schedule_id=cache.get('schedule/schedule_id_crontab', ''),
            api_token=owner_api_token).delete()
        assert_response_ok(response)

        response = mist_core.delete_schedule(
            schedule_id=cache.get('schedule/schedule_id_one_off', ''),
            api_token=owner_api_token).delete()
        assert_response_ok(response)

        response = mist_core.delete_schedule(
            schedule_id=cache.get('schedule/schedule_id_action', ''),
            api_token=owner_api_token).delete()
        assert_response_ok(response)

        print "Success!!!!"
