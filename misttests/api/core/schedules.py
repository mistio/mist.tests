from misttests.api.helpers import *


############################################################################
#                             Unit Testing                                 #
############################################################################

# add schedule
# show schedule
# edit schedule


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


def test_delete_schedule_no_api_token(pretty_print, mist_core):
    response = mist_core.delete_schedule(api_token='', schedule_id='dummy').delete()
    assert_response_forbidden(response)
    print "Success!!!"


def test_delete_schedule_wrong_api_token(pretty_print, mist_core):
    response = mist_core.delete_schedule(api_token='dummy', schedule_id='dummy').delete()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_delete_schedule_no_schedule_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_schedule(api_token=owner_api_token, schedule_id='dummy').delete()
    assert_response_not_found(response)
    print "Success!!!"
