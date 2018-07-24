from misttests.integration.api.helpers import *
from misttests import config
from misttests.config import safe_get_var
import pytest

############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_volumes_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_volumes(api_token=owner_api_token,
                                      cloud_id='dummy').get()
    assert_response_not_found(response)
    print "Success!!!"


def test_list_volumes_wrong_api_token(pretty_print, mist_core):
    response = mist_core.list_volumes(api_token='dummy',
                                      cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_list_volumes_no_api_token(pretty_print, mist_core):
    response = mist_core.list_volumes(api_token='',
                                      cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_create_volume_missing_parameter(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_volumes(api_token=owner_api_token,
                                        cloud_id='dummy').post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_create_volumes_wrong_api_token(pretty_print, mist_core):
    response = mist_core.create_volume(api_token='dummy',
                                       cloud_id='dummy').post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_create_volume_no_api_token(pretty_print, mist_core):
    response = mist_core.create_volume(api_token='', cloud_id='dummy').post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_delete_volume_no_api_token(pretty_print, mist_core):
    response = mist_core.delete_volume(api_token='', volume_id='dummy',
                                       cloud_id='dummy').delete()
    assert_response_forbidden(response)
    print "Success!!!"


def test_delete_volume_wrong_api_token(pretty_print, mist_core):
    response = mist_core.delete_volume(api_token='dummy', volume_id='dummy',
                                       cloud_id='dummy').delete()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_delete_volume_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_volume(api_token=owner_api_token,
                                       cloud_id='dummy', volume_id='dummy').delete()
    assert_response_not_found(response)
    print "Success!!!"
