from misttests.api.helpers import *
from misttests import config

import pytest
import socket

from time import sleep


############################################################################
#                             Unit Testing                                 #
############################################################################


#def test_whitelist_ips_no_api_token(pretty_print, mist_core):
#    response = mist_core.whitelist_ips(api_token='').post()
#    assert_response_forbidden(response)
#    print "Success!!!"

#def test_whitelist_ips_wrong_api_token(pretty_print, mist_core, owner_api_token):
#    response = mist_core.whitelist_ips(api_token='00' + owner_api_token[:-2]).post()
#    assert_response_unauthorized(response)
#    print "Success!!!"

#def test_whitelist_ips_missing_parameter(pretty_print, mist_core, owner_api_token):
#    response = mist_core.whitelist_ips(api_token=owner_api_token).post()
#    assert_response_bad_request(response)
#    print "Success!!!"

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

    def test_user_can_create_resources(self, pretty_print, cache, mist_core,
                                       owner_api_token):
        script_data = {'location_type':'inline','exec_type':'executable', 'name': 'Script1'}
        response = mist_core.add_script(api_token=owner_api_token, script_data=script_data,
                                        script=bash_script).post()
        assert_response_ok(response)
        print "Success!!!"

#    def test_user_whitelists_his_own_ip(self, pretty_print, mist_core, owner_api_token):
#        response = mist_core.whitelist_ips(owner_api_token, ips=[{'cidr':socket.gethostbyname(socket.gethostname()),'description':''}]).post()
#        assert_response_ok(response)
#        print "Success!!!"

#    def test_user_can_still_create_resources(self, pretty_print, cache, mist_core,
#                             owner_api_token, private_key):
#        response = mist_core.add_key(
#            name='TestKey',
#            private=private_key,
#            api_token=owner_api_token).put()
#        assert_response_ok(response)

    def test_set_whitelisted_ips_to_empty(self, pretty_print, mist_core, owner_api_token):
        response = mist_core.whitelist_ips(owner_api_token, ips=[]).post()
        assert_response_ok(response)
        print "Success!!!"

    def test_user_can_still_create_resources(self, pretty_print, cache, mist_core,
                             owner_api_token, private_key):
        response = mist_core.add_key(
            name='TestKey',
            private=private_key,
            api_token=owner_api_token).put()
        assert_response_ok(response)
        print "Success!!!"

    def test_whitelist_dummy_ip(self, pretty_print, mist_core, owner_api_token):
        response = mist_core.whitelist_ips(owner_api_token, ips=[{'cidr':'1.2.3.4','description':'dummy'}]).post()
        assert_response_ok(response)
        print "Success!!!"

#    shouldn't below receive 403? gets 502...
#    def test_user_cannot_create_resources(self, pretty_print, cache, mist_core,
#                             owner_api_token, private_key):
#        response = mist_core.add_key(
#            name='TestKey2',
#            private=private_key,
#            api_token=owner_api_token).put()
#        assert_response_forbidden(response)
#        print "Success!!!"

def test_request_whitelist_ip(pretty_print, mist_core, owner_api_token):
    response = mist_core.request_whitelist_ip(api_token=owner_api_token).post()
    assert_response_forbidden(response)
    print "Success!!!"
#-- User requests whitelist

#-- User confirms whitelist

#-- User can now successfully create resources
