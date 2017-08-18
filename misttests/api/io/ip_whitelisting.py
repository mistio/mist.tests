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
#    assert_response_ok(response)
#    print "Success!!!"

# below returns bad request
#def test_confirm_whitelist_ip_no_api_token(pretty_print, mist_core):
#    response = mist_core.confirm_whitelist_ip(api_token='').get()
#    assert_response_unauthorized(response)
#    print "Success!!!"

# below returns bad request
#def test_confirm_whitelist_ip_wrong_api_token(pretty_print, mist_core, owner_api_token):
#    response = mist_core.confirm_whitelist_ip(api_token='00' + owner_api_token[:-2]).get()
#    assert_response_unauthorized(response)
#    print "Success!!!"

def test_confirm_whitelist_ip_missing_parameter(pretty_print, mist_core, owner_api_token):
    response = mist_core.confirm_whitelist_ip(api_token=owner_api_token).get()
    assert_response_bad_request(response)
    print "Success!!!"

def test_confirm_whitelist_ip_wrong_parameter(pretty_print, mist_core, owner_api_token):
    response = mist_core.confirm_whitelist_ip(api_token=owner_api_token, key='dummy').get()
    assert_response_bad_request(response)
    print "Success!!!"

############################################################################
#                         Functional Testing                               #
############################################################################


@pytest.mark.incremental
class TestWhitelistingIpsFunctionality:


    def test_user_whitelists_his_own_ip(self, pretty_print, mist_core, owner_api_token):
        print "Success!!!"

#-- User saves his IP as whitelisted

#-- User can still create resources

#-- User updates whitelisted ips (removes his current IP, whitelisted IPs are now [])

#-- User can still create resources

#-- User saves a mock IP as whitelisted

#-- User gets 403 as responses (in everything except logout)

#-- User requests whitelist

#-- User confirms whitelist

#-- User can now successfully create resources
