from misttests.integration.api.helpers import *
from misttests import config

import pytest
import socket

############################################################################
#                             Unit Testing                                 #
############################################################################


def test_whitelist_ips_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.whitelist_ips(api_token='').post()
    assert_response_forbidden(response)
    print("Success!!!")

def test_whitelist_ips_wrong_api_token(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.whitelist_ips(api_token='00' + owner_api_token[:-2]).post()
    assert_response_unauthorized(response)
    print("Success!!!")

def test_whitelist_ips_missing_parameter(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.whitelist_ips(api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print("Success!!!")

def test_request_whitelist_ip_no_api_token(pretty_print, owner_email, mist_api_v1):
    response = mist_api_v1.request_whitelist_ip(owner_email, api_token='').post()
    assert_response_forbidden(response)
    print("Success!!!")

#def test_request_whitelist_ip_wrong_api_token(pretty_print, owner_email, mist_api_v1, owner_api_token):
#    response = mist_api_v1.request_whitelist_ip(owner_email, api_token='00' + owner_api_token[:-2]).post()
#    assert_response_ok(response)
#    print "Success!!!"

# def test_confirm_whitelist_ip_no_api_token(pretty_print, mist_api_v1):
#     response = mist_api_v1.confirm_whitelist_ip(api_token='').get()
#     assert_response_ok(response)
#     print "Success!!!"

# def test_confirm_whitelist_ip_wrong_api_token(pretty_print, mist_api_v1, owner_api_token):
#     response = mist_api_v1.confirm_whitelist_ip(api_token='00' + owner_api_token[:-2]).get()
#     assert_response_unauthorized(response)
#     print "Success!!!"

def test_confirm_whitelist_ip_missing_parameter(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.confirm_whitelist_ip(api_token=owner_api_token).get()
    assert_response_bad_request(response)
    print("Success!!!")

def test_confirm_whitelist_ip_wrong_parameter(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.confirm_whitelist_ip(api_token=owner_api_token, key='dummy').get()
    assert_response_bad_request(response)
    print("Success!!!")

############################################################################
#                         Functional Testing                               #
############################################################################


@pytest.mark.incremental
class TestWhitelistingIpsFunctionality:

    def test_user_whitelists_empty_ip(self, pretty_print, mist_api_v1, owner_api_token):
        response = mist_api_v1.whitelist_ips(owner_api_token, ips=[]).post()
        assert_response_ok(response)
        print("Success!!!")

    def test_user_can_create_resources(self, pretty_print, cache, mist_api_v1,
                                       owner_api_token):
        script_data = {'location_type':'inline','exec_type':'executable', 'name': 'Script1'}
        response = mist_api_v1.add_script(api_token=owner_api_token, script_data=script_data,
                                        script=bash_script).post()
        assert_response_ok(response)
        print("Success!!!")

    def test_whitelist_dummy_ip(self, pretty_print, mist_api_v1, owner_api_token):
        response = mist_api_v1.whitelist_ips(owner_api_token, ips=[{'cidr':'1.2.3.4','description':'dummy'}]).post()
        assert_response_ok(response)
        print("Success!!!")

    def test_user_cannot_create_resources(self, pretty_print, cache, mist_api_v1,
                                owner_api_token, private_key):
        response = mist_api_v1.add_key(
            name='TestKey3',
            private=private_key,
            api_token=owner_api_token).put()
        assert_response_forbidden(response)
        print("Success!!!")

    def test_request_whitelist_ip(self, pretty_print, mist_api_v1, owner_email, owner_api_token):
        response = mist_api_v1.request_whitelist_ip(owner_email, api_token=owner_api_token).post()
        assert_response_forbidden(response)
        print("Success!!!")
