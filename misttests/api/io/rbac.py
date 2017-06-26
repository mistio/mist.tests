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


def test_add_team_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.add_team(api_token='00' + owner_api_token[:-2],
                                  name='test_team', org_id='dummy').post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_add_team_no_api_token(pretty_print, mist_core):
    response = mist_core.add_team(api_token='',
                                  name='test_org', org_id='dummy').post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_list_orgs_no_api_token(pretty_print, mist_core):
    response = mist_core.list_orgs(api_token='').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_list_orgs_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_orgs(api_token='00' + owner_api_token[:-2]).get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_show_user_org_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.show_user_org(api_token='00' + owner_api_token[:-2]).get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_show_user_org_no_api_token(pretty_print, mist_core):
    response = mist_core.show_user_org(api_token='').get()
    assert_response_unauthorized(response)
    print "Success!!!"

# def test_add_team_missing_parameter(pretty_print, mist_core, owner_api_token):
#     response = mist_core.add_team(api_token=owner_api_token, name='test_team', org_id='dummy').post()
#     assert_response_bad_request(response)
#     print "Success!!!"

############################################################################
#                          Functional Testing                              #
############################################################################

@pytest.mark.incremental
class TestRbacFunctionality:

    def test_list_orgs(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.list_orgs(api_token=owner_api_token).get()
        assert len(response.json()) == 1, "User should belong to 1 orgs, but instead belongs to %s" % len(response.json())
        assert_response_ok(response)
        print "Success!!!"

    def test_show_user_org(self, pretty_print, mist_core, owner_api_token):
        response = mist_core.show_user_org(api_token=owner_api_token).get()
        import ipdb;ipdb.set_trace()
        assert response.json()['members_count'] == 1, "The brand new org has more than 1 members!!!"
        assert len(response.json()['teams']) == 1, "The brand new org has more than 1 teams!!!"
        assert response.json()['teams'][0]['name'] == 'Owners'
         
        print "Success!!!"

    def test_create_org(self, pretty_print, mist_core, owner_api_token, cache):
        name = 'test_org_%d' % random.randint(1, 2000)
        response = mist_core.create_org(api_token=owner_api_token, name=name).post()
        cache.set('org_id', response.json()['id'])
        assert_response_ok(response)
        response = mist_core.create_org(api_token=owner_api_token, name=name).post()
        assert_response_conflict(response)
        print "Success!!!"

    # def test_add_team(self, pretty_print, mist_core, owner_api_token, cache):
    #     response = mist_core.add_team(api_token=owner_api_token,
    #                                   name='test_team', org_id=cache.get('org_id', '')).post()
    #     import ipdb;ipdb.set_trace()





# show_user_invitations

# switch between orgs?

# add team
# list teams
# show team
# edit team
# delete team

# invite member
# delete member
