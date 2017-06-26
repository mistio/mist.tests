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
    response = mist_core.create_org(api_token='00' + owner_api_token[:-2],
                                    name='test_org').post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_add_org_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.add_team(api_token='00' + owner_api_token[:-2],
                                  name='test_team', org_id='dummy').post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_add_team_no_api_token(pretty_print, mist_core):
    response = mist_core.add_team(api_token='',
                                  name='test_org', org_id='dummy').post()
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
        cache.set('org_id', response.json()['id'])
        import ipdb;ipdb.set_trace()
        assert_response_ok(response)
        response = mist_core.create_org(api_token=owner_api_token, name=name).post()
        assert_response_conflict(response)
        print "Success!!!"

    def test_list_orgs(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.list_orgs(api_token=owner_api_token).get()
        import ipdb;
        ipdb.set_trace()

    # def test_show_user_org(self, pretty_print, mist_core, owner_api_token):
    #     response = mist_core.show_user_org(api_token=owner_api_token).get()
    #     import ipdb;ipdb.set_trace()


    # def test_add_team(self, pretty_print, mist_core, owner_api_token, cache):
    #     response = mist_core.add_team(api_token=owner_api_token,
    #                                   name='test_team', org_id=cache.get('org_id', '')).post()
    #     import ipdb;ipdb.set_trace()


# show_org
# show_user_org

# show_user_invitations

# add team
# list teams
# show team
# edit team
# delete team

# invite member
# delete member
