import pytest

from misttests.integration.api.helpers import *


def test_list_secrets(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_secrets(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print "Success!!!"


def test_delete_secret_wrong_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_secret(secret_id='dummy',api_token=owner_api_token).delete()
    assert_response_not_found(response)
    print "Success!!!"


def test_delete_secret_wrong_api_token(pretty_print, mist_core):
    response = mist_core.delete_secret(secret_id='dummy',api_token='dummy').delete()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_create_secret_no_name(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_secret(name='', secret={'a': 'b'},
                                       api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_create_secret_no_secret(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_secret(name='dummy', secret={},
                                       api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_get_secret_wrong_id(pretty_print, cache, mist_core,
                             owner_api_token):
    response = mist_core.get_secret('dummy', api_token=owner_api_token).get()
    assert_response_not_found(response)
    print "Success!!!"
