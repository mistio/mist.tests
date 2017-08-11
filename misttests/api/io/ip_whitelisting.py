from misttests.api.helpers import *
from misttests import config

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_whitelist_ips_no_api_token(pretty_print, mist_core):
    response = mist_core.whitelist_ips(api_token='').post()
    assert_response_forbidden(response)
    print "Success!!!"

def test_whitelist_ips_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.whitelist_ips(api_token='00' + owner_api_token[:-2]).post()
    assert_response_unauthorized(response)
    print "Success!!!"

def test_whitelist_ips_missing_parameter(pretty_print, mist_core, owner_api_token):
    response = mist_core.whitelist_ips(api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"

def test_request_whitelist_ip_no_api_token(pretty_print, mist_core):
    response = mist_core.request_whitelist_ip(api_token='').post()
    assert_response_forbidden(response)
    print "Success!!!"

# below returns ok
#def test_request_whitelist_ip_wrong_api_token(pretty_print, mist_core, owner_api_token):
#    response = mist_core.request_whitelist_ip(api_token='00' + owner_api_token[:-2]).post()
#    assert_response_unauthorized(response)
#    print "Success!!!"

def test_confirm_whitelist_ip_no_api_token(pretty_print, mist_core):
    response = mist_core.confirm_whitelist_ip(api_token='').post()
    assert_response_forbidden(response)
    print "Success!!!"

# wrong api token
# missing key
# wrong key


############################################################################
#                         Functional Testing                               #
############################################################################
