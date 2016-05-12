import sys
import json
import pprint
import pytest

from mist.io.tests.api.utils import *


def test_001_get_list_cronjobs_without_token(pretty_print, mist_core):
    print "\n>>> GETing /cronjobs to get a list of all cronjobs without token"
    response = mist_core.list_cronjobs_entries(api_token='').get()
    assert_response_unauthorized(response)
    print "Success!!!!"


def test_002_get_list_cronjobs_with_token(pretty_print, mist_core,
                                          valid_api_token):
    print "\n>>> GETing /cronjobs to get a list of all Cronjobs"
    response = mist_core.list_cronjobs_entries(api_token=valid_api_token).get()
    assert_response_ok(response)
    print "Got a list of cronjobs: \n"
    pprint.pprint(response.json(), indent=3, stream=sys.stdout)
    print "Success!!!!"


def test_003_check_add_cronjob_entry_no_name(pretty_print,
                                             mist_core,
                                             random_bash_script,
                                             expires,
                                             machines_per_cloud,
                                             valid_api_token):
    print "\n>>> POSTing /cronjobs to add a cronjob without name"
    entry = {"every": 5, "period": "minutes"}

    response = mist_core.add_cronjob_entry(name='',
                                           script_id=random_bash_script[
                                               'script_id'],
                                           machines_per_cloud=machines_per_cloud,
                                           enabled=True,
                                           expires=expires,
                                           cronjob_type='interval',
                                           cronjob_entry=json.dumps(entry),
                                           api_token=valid_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_004_check_add_cronjob_entry_no_cronjob_type(pretty_print,
                                                     mist_core,
                                                     random_bash_script,
                                                     expires,
                                                     machines_per_cloud,
                                                     valid_api_token):
    print "\n>>> POSTing /cronjobs to add a cronjob without cronjob_type"
    entry = {"every": 5, "period": "minutes"}

    response = mist_core.add_cronjob_entry(name='check_failure',
                                           script_id=random_bash_script[
                                               'script_id'],
                                           machines_per_cloud=machines_per_cloud,
                                           enabled=True,
                                           expires=expires,
                                           cronjob_type='',
                                           cronjob_entry=json.dumps(entry),
                                           api_token=valid_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_005_check_add_cronjob_entry_with_expired_date(pretty_print,
                                                       mist_core,
                                                       random_bash_script,
                                                       expired,
                                                       machines_per_cloud,
                                                       valid_api_token):
    print "\n>>> POSTing /cronjobs to add a cronjob with expired expiration" \
          " date"

    response = mist_core.add_cronjob_entry(name='check_failure',
                                           script_id=random_bash_script[
                                               'script_id'],
                                           machines_per_cloud=machines_per_cloud,
                                           enabled=True,
                                           cronjob_type='one_off',
                                           cronjob_entry=expired,
                                           api_token=valid_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_006_check_add_cronjob_entry_wrong_cronjob_entry(pretty_print,
                                                         mist_core,
                                                         random_bash_script,
                                                         expired,
                                                         machines_per_cloud,
                                                         valid_api_token):
    print "\n>>> POSTing /cronjobs to add a cronjob with wrong cronjob entry"

    response = mist_core.add_cronjob_entry(name='check_failure',
                                           script_id=random_bash_script[
                                               'script_id'],
                                           machines_per_cloud=machines_per_cloud,
                                           enabled=True,
                                           cronjob_type='one_off',
                                           cronjob_entry='bla',
                                           api_token=valid_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_007_check_add_cronjob_entry_wrong_script_id(pretty_print,
                                                     mist_core,
                                                     random_bash_script,
                                                     expired,
                                                     machines_per_cloud,
                                                     valid_api_token):
    print "\n>>> POSTing /cronjobs to add a cronjob with wrong script_id"

    response = mist_core.add_cronjob_entry(name='check_failure',
                                           script_id=random_bash_script[
                                                         'script_id'],
                                           machines_per_cloud=machines_per_cloud,
                                           enabled=True,
                                           cronjob_type='one_off',
                                           cronjob_entry='bla',
                                           api_token=valid_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_008_check_add_cronjob_entry_with_wrong_api_token(pretty_print,
                                                          mist_core,
                                                          random_bash_script,
                                                          expired,
                                                          machines_per_cloud,
                                                          valid_api_token):
    print "\n>>> POSTing /cronjobs to add a cronjob with wrong script_id"

    response = mist_core.add_cronjob_entry(name='check_failure',
                                           script_id=random_bash_script[
                                                         'script_id'],
                                           machines_per_cloud=machines_per_cloud,
                                           enabled=True,
                                           cronjob_type='one_off',
                                           cronjob_entry='bla',
                                           api_token=valid_api_token[:-1]).post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_009_show_cronjob_entry_wrong_api_token(pretty_print, mist_core,
                                                valid_api_token):
    print "\n>>>  GETing /cronjobs to show a cronjob with wrong api token"
    response = mist_core.show_cronjobs_entry(
        cronjob_id='',
        api_token=valid_api_token[:-1]).get()
    assert_response_not_found(response)
    print "Success!!!!"


def test_010_show_cronjob_entry_cronjob_id(pretty_print, mist_core,
                                           valid_api_token):
    print "\n>>>  GETing /cronjobs to show a cronjob with wrong cronjob id"
    response = mist_core.show_cronjobs_entry(
        cronjob_id='bla',
        api_token=valid_api_token).get()
    assert_response_not_found(response)
    print "Success!!!!"


@pytest.mark.incremental
class TestSimpleUserCronjobCycle:

    def test_add_cronjob_entry_interval(self, pretty_print, cache,
                                        mist_core,
                                        random_bash_script,
                                        expires,
                                        machines_per_cloud,
                                        valid_api_token):
        print "\n>>> POSTing /cronjobs to add a cronjob with correct params, " \
              "type interval"
        entry = {"every": 5, "period": "minutes"}

        response = mist_core.add_cronjob_entry(name='check_add_interval',
                                               script_id=random_bash_script[
                                                   'script_id'],
                                               machines_per_cloud=machines_per_cloud,
                                               enabled=True,
                                               expires=expires,
                                               cronjob_type='interval',
                                               cronjob_entry=json.dumps(entry),
                                               api_token=valid_api_token).post()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        assert_is_not_none(rjson.get('id'),
                           "Did not get an id back in the response")
        cache.set('cronjob/cronjob_id_interval', rjson['id'])
        print "Success!!!"

    def test_add_cronjob_entry_crontab(self, pretty_print, cache,
                                       mist_core,
                                       random_bash_script,
                                       expires,
                                       machines_per_cloud,
                                       valid_api_token):
        print "\n>>> POSTing /cronjobs to add a cronjob with correct params, " \
              "type crontab"
        entry = {'minute': '*/10'}

        response = mist_core.add_cronjob_entry(name='check_add_cron',
                                               script_id=random_bash_script[
                                                   'script_id'],
                                               machines_per_cloud=machines_per_cloud,
                                               enabled=True,
                                               expires=expires,
                                               cronjob_type='crontab',
                                               cronjob_entry=json.dumps(entry),
                                               api_token=valid_api_token).post()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        assert_is_not_none(rjson.get('id'),
                           "Did not get an id back in the response")
        cache.set('cronjob/cronjob_id_crontab', rjson['id'])
        print "Success!!!"

    def test_add_cronjob_entry_one_off(self, pretty_print, cache,
                                       mist_core,
                                       random_bash_script,
                                       expires,
                                       machines_per_cloud,
                                       valid_api_token):
        print "\n>>> POSTing /cronjobs to add a cronjob with correct params, " \
              "type one-off"
        response = mist_core.add_cronjob_entry(name='check_add_one_off',
                                               script_id=random_bash_script[
                                                   'script_id'],
                                               machines_per_cloud=machines_per_cloud,
                                               enabled=True,
                                               expires=expires,
                                               cronjob_type='one_off',
                                               cronjob_entry=expires,
                                               api_token=valid_api_token).post()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        assert_is_not_none(rjson.get('id'),
                           "Did not get an id back in the response")
        cache.set('cronjob/cronjob_id_one_off', rjson['id'])
        print "Success!!!"

    def test_add_cronjob_entry_action(self, pretty_print, cache,
                                      mist_core,
                                      random_bash_script,
                                      expires,
                                      machines_per_cloud,
                                      valid_api_token):
        print "\n>>> POSTing /cronjobs to add a cronjob with correct params, " \
              "for an action"
        response = mist_core.add_cronjob_entry(name='check_add_action',
                                               action='reboot',
                                               machines_per_cloud=machines_per_cloud,
                                               enabled=True,
                                               cronjob_type='one_off',
                                               cronjob_entry=expires,
                                               api_token=valid_api_token).post()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        assert_is_not_none(rjson.get('id'),
                           "Did not get an id back in the response")
        cache.set('cronjob/cronjob_id_action', rjson['id'])
        print "Success!!!"

    def test_edit_cronjob_entry_crontab_expired_date(self, pretty_print,
                                                     mist_core,
                                                     machines_per_cloud,
                                                     random_bash_script,
                                                     cache,
                                                     expired,
                                                     valid_api_token):

        print "\n>>>  PUTing /cronjobs to edit a cronjob, with expired " \
              "expiration date"
        entry = {'minute': '*/10', 'hour': '*/11'}

        cronjob_id = cache.get('cronjob/cronjob_id_crontab', '')
        response = mist_core.edit_cronjob_entry(name='check_edit_to cron',
                                                script_id=random_bash_script[
                                                    'script_id'],
                                                machines_per_cloud=machines_per_cloud,
                                                enabled=True,
                                                expires=expired,
                                                cronjob_type='crontab',
                                                cronjob_entry=json.dumps(entry),
                                                cronjob_id=cronjob_id,
                                                api_token=valid_api_token).put()
        assert_response_bad_request(response)
        print "Success!!!"

    def test_edit_cronjob_entry_crontab_wrong_script_id(self, pretty_print,
                                                        mist_core,
                                                        machines_per_cloud,
                                                        random_bash_script,
                                                        cache,
                                                        expired,
                                                        valid_api_token):

        print "\n>>>  PUTing /cronjobs to edit a cronjob, with wrong script " \
              "id date"
        entry = {'minute': '*/10', 'hour': '*/11'}

        cronjob_id = cache.get('cronjob/cronjob_id_crontab', '')
        response = mist_core.edit_cronjob_entry(name='check_edit_to cron',
                                                script_id=random_bash_script[
                                                              'script_id'][:-1],
                                                machines_per_cloud=machines_per_cloud,
                                                enabled=True,
                                                expires=expired,
                                                cronjob_type='crontab',
                                                cronjob_entry=json.dumps(entry),
                                                cronjob_id=cronjob_id,
                                                api_token=valid_api_token).put()
        assert_response_not_found(response)
        print "Success!!!"

    def test_edit_cronjob_entry_wrong_cronjob(self, pretty_print, mist_core,
                                              machines_per_cloud,
                                              random_bash_script,
                                              cache,
                                              expired,
                                              valid_api_token):

        print "\n>>>  PUTing /cronjobs to edit a cronjob, with wrong cronjob" \
              " entry"
        entry = {'minute': '*/10/of bla', 'hour': '*/11'}

        cronjob_id = cache.get('cronjob/cronjob_id_crontab', '')
        response = mist_core.edit_cronjob_entry(name='check_edit_to cron',
                                                script_id=random_bash_script[
                                                    'script_id'],
                                                machines_per_cloud=machines_per_cloud,
                                                enabled=True,
                                                expires=expired,
                                                cronjob_type='crontab',
                                                cronjob_entry=json.dumps(entry),
                                                cronjob_id=cronjob_id,
                                                api_token=valid_api_token).put()
        assert_response_bad_request(response)
        print "Success!!!"

    def test_edit_cronjob_entry_interval_to_crontab(self, pretty_print,
                                                    mist_core,
                                                    machines_per_cloud,
                                                    random_bash_script,
                                                    cache,
                                                    expires,
                                                    valid_api_token):

        print "\n>>>  PUTing /cronjobs to edit a cronjob, interval --> crontab"
        entry = {'minute': '*/10', 'hour': '*/11'}

        cronjob_id = cache.get('cronjob/cronjob_id_crontab', '')
        response = mist_core.edit_cronjob_entry(name='check_edit_to cron',
                                                script_id=random_bash_script[
                                                    'script_id'],
                                                machines_per_cloud=machines_per_cloud,
                                                enabled=True,
                                                expires=expires,
                                                cronjob_type='crontab',
                                                cronjob_entry=json.dumps(entry),
                                                cronjob_id=cronjob_id,
                                                api_token=valid_api_token).put()
        assert_response_ok(response)
        print "Success!!!"

    def test_edit_cronjob_entry_crontab_to_one_off(self, pretty_print,
                                                   mist_core,
                                                   random_bash_script, cache,
                                                   expires,
                                                   valid_api_token,
                                                   machines_per_cloud):

        print "\n>>>  PUTing /cronjobs to edit a cronjob, crontab--> one_off"
        cronjob_id = cache.get('cronjob/cronjob_id_crontab', '')
        response = mist_core.edit_cronjob_entry(name='check_edit_one_off',
                                                script_id=random_bash_script[
                                                    'script_id'],
                                                machines_per_cloud=machines_per_cloud,
                                                enabled=True,
                                                cronjob_type='one_off',
                                                cronjob_entry=expires,
                                                cronjob_id=cronjob_id,
                                                api_token=valid_api_token).put()
        assert_response_ok(response)
        print "Success!!!"

    def test_018_check_edit_cronjob_entry(self, pretty_print, mist_core,
                                          machines_per_cloud,
                                          random_bash_script,
                                          expires, cache,
                                          valid_api_token):
        print "\n>>>  PUTing /cronjobs to edit a cronjob, action--> script"
        cronjob_id = cache.get('cronjob/cronjob_id_action', '')
        response = mist_core.edit_cronjob_entry(name='check_edit_script',
                                                script_id=random_bash_script[
                                                    'script_id'],
                                                machines_per_cloud=
                                                machines_per_cloud,
                                                enabled=True,
                                                cronjob_type='one_off',
                                                cronjob_entry=expires,
                                                cronjob_id=cronjob_id,
                                                api_token=valid_api_token).put()
        assert_response_bad_request(response)
        print "Success!!!"

    def test_show_cronjob_entry(self, pretty_print, mist_core,
                                cache, valid_api_token):

        print "\n>>>  GETing /cronjobs to show a cronjob with correct id"
        response = mist_core.show_cronjobs_entry(
            cronjob_id=cache.get('cronjob/cronjob_id_interval', ''),
            api_token=valid_api_token).get()
        assert_response_ok(response)
        print "Success!!!!"

    def test_check_delete_cronjob_entry(self, pretty_print, mist_core,
                                        cache, valid_api_token):

        print "\n>>>  DELETEing /cronjobs to delete a cronjob with correct _id"

        response = mist_core.delete_cronjob(
            cronjob_id=cache.get('cronjob/cronjob_id_interval', ''),
            api_token=valid_api_token).delete()
        assert_response_ok(response)

        response = mist_core.delete_cronjob(cronjob_id=
        cache.get(
            'cronjob/cronjob_id_crontab',
            ''),
            api_token=valid_api_token).delete()
        assert_response_ok(response)

        response = mist_core.delete_cronjob(cronjob_id=
        cache.get(
            'cronjob/cronjob_id_one_off',
            ''),
            api_token=valid_api_token).delete()
        assert_response_ok(response)

        response = mist_core.delete_cronjob(cronjob_id=
        cache.get(
            'cronjob/cronjob_id_action',
            ''),
            api_token=valid_api_token).delete()
        assert_response_ok(response)

        print "Success!!!!"
