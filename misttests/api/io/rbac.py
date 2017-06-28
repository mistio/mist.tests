from misttests.api.helpers import *

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################


# def test_create_org_missing_parameter(pretty_print, mist_core, owner_api_token):
#     response = mist_core.create_org(api_token=owner_api_token).post()
#     assert_response_bad_request(response)
#     print "Success!!!"
#
#
# def test_create_org_no_api_token(pretty_print, mist_core):
#     response = mist_core.create_org(api_token='', name='test_org').post()
#     assert_response_forbidden(response)
#     print "Success!!!"
#
#
# def test_create_org_wrong_api_token(pretty_print, mist_core, owner_api_token):
#     response = mist_core.create_org(api_token='00' + owner_api_token[:-2],
#                                     name='test_org').post()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_add_team_wrong_api_token(pretty_print, mist_core, owner_api_token):
#     response = mist_core.add_team(api_token='00' + owner_api_token[:-2],
#                                   name='test_team', org_id='dummy').post()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_add_team_no_api_token(pretty_print, mist_core):
#     response = mist_core.add_team(api_token='',
#                                   name='test_org', org_id='dummy').post()
#     assert_response_forbidden(response)
#     print "Success!!!"
#
#
# def test_edit_team_no_api_token(pretty_print, mist_core):
#     response = mist_core.edit_team(api_token='', team_id= 'dummy',
#                                    name='test_org', org_id='dummy').put()
#     assert_response_forbidden(response)
#     print "Success!!!"
#
#
# def test_edit_team_wrong_api_token(pretty_print, mist_core, owner_api_token):
#     response = mist_core.edit_team(api_token='00' + owner_api_token[:-2],
#                                    name='test_team', org_id='dummy', team_id='dummy').put()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_edit_team_wrong_org_id(pretty_print, mist_core, owner_api_token):
#     response = mist_core.edit_team(api_token=owner_api_token,
#                                    name='test_team', org_id='dummy', team_id='dummy').put()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_show_team_no_api_token(pretty_print, mist_core):
#     response = mist_core.show_team(api_token='', team_id= 'dummy',
#                                    org_id='dummy').get()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_show_team_wrong_api_token(pretty_print, mist_core, owner_api_token):
#     response = mist_core.show_team(api_token='00' + owner_api_token[:-2],
#                                    org_id='dummy', team_id='dummy').get()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_show_team_wrong_org_id(pretty_print, mist_core, owner_api_token):
#     response = mist_core.show_team(api_token=owner_api_token,
#                                    org_id='dummy', team_id='dummy').get()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_delete_team_no_api_token(pretty_print, mist_core):
#     response = mist_core.delete_team(api_token='', team_id= 'dummy',
#                                      org_id='dummy').delete()
#     assert_response_forbidden(response)
#     print "Success!!!"
#
#
# def test_delete_team_wrong_api_token(pretty_print, mist_core, owner_api_token):
#     response = mist_core.delete_team(api_token='00' + owner_api_token[:-2],
#                                      org_id='dummy', team_id='dummy').delete()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_delete_team_wrong_org_id(pretty_print, mist_core, owner_api_token):
#     response = mist_core.delete_team(api_token=owner_api_token,
#                                      org_id='dummy', team_id='dummy').delete()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_list_orgs_no_api_token(pretty_print, mist_core):
#     response = mist_core.list_orgs(api_token='').get()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_list_orgs_wrong_api_token(pretty_print, mist_core, owner_api_token):
#     response = mist_core.list_orgs(api_token='00' + owner_api_token[:-2]).get()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_list_teams_no_api_token(pretty_print, mist_core):
#     response = mist_core.list_teams(api_token='', org_id='dummy').get()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_list_teams_wrong_api_token(pretty_print, mist_core, owner_api_token):
#     response = mist_core.list_teams(api_token='00' + owner_api_token[:-2], org_id='dummy').get()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_list_teams_wrong_org_id(pretty_print, mist_core, owner_api_token):
#     response = mist_core.list_teams(api_token=owner_api_token, org_id='dummy').get()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_show_user_org_wrong_api_token(pretty_print, mist_core, owner_api_token):
#     response = mist_core.show_user_org(api_token='00' + owner_api_token[:-2]).get()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_show_user_org_no_api_token(pretty_print, mist_core):
#     response = mist_core.show_user_org(api_token='').get()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_invite_member_no_api_token(pretty_print, mist_core):
#     response = mist_core.invite_member_to_team(api_token='', org_id='dummy',
#                                                team_id='dummy', email='').post()
#     assert_response_forbidden(response)
#     print "Success!!!"
#
#
# def test_invite_member_wrong_api_token(pretty_print, mist_core, owner_api_token):
#     response = mist_core.invite_member_to_team(api_token='00' + owner_api_token[:-2], org_id='dummy',
#                                                team_id='dummy', email='').post()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_invite_member_wrong_org_id(pretty_print, mist_core, owner_api_token):
#     response = mist_core.invite_member_to_team(api_token=owner_api_token, org_id='dummy',
#                                                team_id='dummy', email='').post()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_show_pending_invitations_no_api_token(pretty_print, mist_core):
#     response = mist_core.show_user_invitations(api_token='').get()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_show_pending_invitations_wrong_api_token(pretty_print, mist_core, owner_api_token):
#     response = mist_core.show_user_invitations(api_token='00' + owner_api_token[:-2]).get()
#     assert_response_unauthorized(response)
#     print "Success!!!"

############################################################################
#                          Functional Testing                              #
############################################################################

@pytest.mark.incremental
class TestRbacFunctionality:

    def test_initialize_members(pretty_print, initialize_members):
        print "Success!!!"

    def test_list_orgs(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.list_orgs(api_token=owner_api_token).get()
        assert len(response.json()) == 1, "User should belong to 1 orgs, but instead belongs to %s" % len(response.json())
        assert_response_ok(response)
        print "Success!!!"

    def test_show_user_org(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.show_user_org(api_token=owner_api_token).get()
        assert response.json()['members_count'] == 1, "The brand new org has more than 1 members!!!"
        assert len(response.json()['teams']) == 1, "The brand new org has more than 1 teams!!!"
        assert response.json()['teams'][0]['name'] == 'Owners', "The default team was not owners!!!"
        cache.set('default_org_id',response.json()['id'])
        print "Success!!!"

    def test_list_teams(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.list_teams(api_token=owner_api_token, org_id=cache.get('default_org_id', '')).get()
        assert_response_ok(response)
        assert len(response.json()) == 1, "The brand new org has more than 1 teams!!!"
        print "Success!!!"

    def test_add_team(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.add_team(api_token=owner_api_token,
                                      org_id=cache.get('default_org_id', '')).post()
        assert_response_bad_request(response)
        response = mist_core.add_team(api_token=owner_api_token,
                                      name='test_team', org_id=cache.get('default_org_id', '')).post()
        cache.set('team_id', response.json()['id'])
        assert response.json()['visible'], "Team added is non-visible by default!!!"
        assert_response_ok(response)
        response = mist_core.list_teams(api_token=owner_api_token, org_id=cache.get('default_org_id', '')).get()
        assert_response_ok(response)
        assert len(response.json()) == 2, "Although a new team was added, it is not visible in list_teams request!!!"
        print "Success!!!"

    def test_edit_team_wrong_team_id(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.edit_team(api_token=owner_api_token,org_id=cache.get('default_org_id', ''),
                                       name='dummy', team_id= 'dummy').put()
        assert_response_not_found(response)
        print "Success!!!"

    def test_edit_team(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.edit_team(api_token=owner_api_token,org_id=cache.get('default_org_id', ''),
                                       name='Renamed team', team_id=cache.get('team_id', '')).put()
        assert_response_ok(response)
        print "Success!!!"

    def test_show_team_wrong_team_id(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.show_team(api_token=owner_api_token,org_id=cache.get('default_org_id', ''),
                                       team_id='dummy').get()
        assert_response_not_found(response)
        print "Success!!!"

    def test_show_team(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.show_team(api_token=owner_api_token,org_id=cache.get('default_org_id', ''),
                                       team_id=cache.get('team_id', '')).get()
        assert_response_ok(response)
        assert response.json()['name'] == 'Renamed team', "Although team was renamed above, the name has not changed"
        print "Success!!!"

    def test_delete_team_wrong_team_id(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.delete_team(api_token=owner_api_token,org_id=cache.get('default_org_id', ''),
                                         team_id='dummy').delete()
        assert_response_not_found(response)
        print "Success!!!"

    def test_invite_member_wrong_team_id(self, pretty_print, mist_core, owner_api_token, cache, member1_email):
        response = mist_core.invite_member_to_team(api_token=owner_api_token, org_id=cache.get('default_org_id',''),
                                                   team_id='dummy', email=member1_email).post()
        assert_response_not_found(response)
        print "Success!!!"

    def test_invite_member(self, pretty_print, mist_core, owner_api_token, cache, member1_email):
        response = mist_core.invite_member_to_team(api_token=owner_api_token, org_id=cache.get('default_org_id',''),
                                                   team_id=cache.get('team_id', ''), email=member1_email).post()
        assert_response_ok(response)
        print "Success!!!"

    # def test_delete_team(self, pretty_print, mist_core, owner_api_token, cache):
    #     response = mist_core.delete_team(api_token=owner_api_token,org_id=cache.get('default_org_id', ''),
    #                                      team_id=cache.get('team_id', '')).delete()
    #     assert_response_ok(response)
    #     response = mist_core.list_teams(api_token=owner_api_token, org_id=cache.get('default_org_id', '')).get()
    #     assert_response_ok(response)
    #     assert len(response.json()) == 1, "Although team was deleted, it is still visible in list_teams"
    #     print "Success!!!"

    def test_create_org(self, pretty_print, mist_core, owner_api_token, cache):
        name = 'test_org_%d' % random.randint(1, 2000)
        response = mist_core.create_org(api_token=owner_api_token, name=name).post()
        cache.set('org_id', response.json()['id'])
        assert_response_ok(response)
        response = mist_core.create_org(api_token=owner_api_token, name=name).post()
        assert_response_conflict(response)
        print "Success!!!"

    def test_show_pending_invitations(self, pretty_print, mist_core, member1_api_token, cache):
        response = mist_core.show_user_invitations(api_token=member1_api_token).get()
        assert_response_ok(response)
        cache.set('invitation_token', response.json()[0]['token'])
        assert len(response.json()) == 1, "Although member has been invited, there are no pending invitations!!!"
        print "Success"

    def test_confirm_invitation_invalid_token(self, pretty_print, mist_core, member1_api_token, cache):
        response = mist_core.confirm_invitation(api_token=member1_api_token, invitoken= '00' + cache.get('invitation_token','')[:-2]).get()
        assert_response_not_found(response)
        print "Success!!!"

    def test_list_orgs_member1(self, pretty_print, mist_core, member1_api_token, cache):
        response = mist_core.list_orgs(api_token=member1_api_token).get()
        # verify that member1 belongs only to his own org since he has not confirmed invitation
        assert len(response.json()) == 1, "User should belong to 1 orgs, but instead belongs to %s" % len(response.json())
        assert_response_ok(response)
        print "Success!!!"

# list teams --> only rename team available

# list_orgs --> 2 members?

# for member verify that he cannot see non-visible team

# delete member

# delete team / teams

# non-owner invites, should fail
