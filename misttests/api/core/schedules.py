from misttests.api.helpers import *

import pytest


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
    response = mist_core.add_schedule(api_token='', name='dummy').post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_add_schedule_wrong_api_token(pretty_print, mist_core):
    response = mist_core.add_schedule(api_token='dummy', name='dummy').post()
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


# add_expired_date
# add_wrong_cronjob_entry


############################################################################
#                         Functional Testing                               #
############################################################################


# @pytest.mark.incremental
# class TestSchedulesFunctionality:


# fix add_schedule_core.py
# create_machine_docker
# add schedule_ok_ stop
# create 2nd machine and tag
# add schedule_start_run_immediately
# add schedule for tagged_machine
# add schedule_script_date
