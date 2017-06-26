from misttests.api.helpers import *

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_create_org_missing_parameter(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_org(api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_create_org_no_api_token(pretty_print, mist_core):
    response = mist_core.create_org(api_token='', name='test_org').post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_create_org_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_org(api_token='00' + owner_api_token[:-2], name='test_org').post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_add_org_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.add_team(api_token='00' + owner_api_token[:-2], name='test_team', org_id='dummy').post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_add_team_no_api_token(pretty_print, mist_core):
    response = mist_core.add_team(api_token='', name='test_org', org_id='dummy').post()
    assert_response_forbidden(response)
    print "Success!!!"


# def test_add_team_missing_parameter(pretty_print, mist_core, owner_api_token):
#     response = mist_core.add_team(api_token=owner_api_token, name='test_team', org_id='dummy').post()
#     assert_response_bad_request(response)
#     print "Success!!!"


# def test_show_org_wrong_id(pretty_print, mist_core, owner_api_token):
#     response = mist_core.show_org(api_token=owner_api_token, org_id='dummy').get()
#     assert_response_not_found(response)
#     print "Success!!!"


# def test_show_org_wrong_id(pretty_print, mist_core, owner_api_token):
#     response = mist_core.show_org(api_token=owner_api_token, org_id='dummy').post()
#     assert_response_ok(response)
#     print "Success!!!"


############################################################################
#                          Functional Testing                              #
############################################################################

@pytest.mark.incremental
class TestRbacFunctionality:

    def test_create_org(self, pretty_print, mist_core, owner_api_token, cache):
        name = 'test_org_%d' % random.randint(1, 2000)
        response = mist_core.create_org(api_token=owner_api_token, name=name).post()
        # cache.set('template_id', response.json()['id'])
        import ipdb;ipdb.set_trace()
        assert_response_ok(response)
        print "Success!!!"
