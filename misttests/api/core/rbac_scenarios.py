import sys
import pytest

from pprint import pprint

from misttests.api.helpers import *


##############################################################################
# Scenarios
##############################################################################

# When executing these tests we are assuming that there four users available.
# The owner of an organization and two members of said organization
# and a simple user with no organization or membership


@pytest.mark.incremental
class TestRBACWithMultipleUsers:
    def test_show_user_org_for_owner(self, cache, pretty_print, mist_core,
                                     owner_api_token, org_name, owner_email,
                                     owner_password):
        print "\n>>> GETing /orgs to get a list of all user orgs and the api" \
              "token with access to that org"
        response = mist_core.list_orgs(api_token=owner_api_token).get()
        assert_response_ok(response)

        org_json = response.json()
        org_id = None
        for org in org_json:
            if org_name == org['name']:
                org_id = org['id']
                break
        assert_is_not_none(org_id)
        cache.set('rbac/org_id', org_id)

        response = mist_core.show_user_org(api_token=owner_api_token).get()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        assert_is_not_none(rjson.get('id'),
                           "Did not get an id back in the response")

        print "Show owner's org: \n"
        pprint(response.json(), indent=3, stream=sys.stdout)
        print "Success!!!!"

    def test_create_personal_tokens_for_members(self, pretty_print, mist_core,
                                                cache, member1_email,
                                                member1_password, member2_email,
                                                member2_password):
        print "\n>>> GETing / to get org of both members"

        response = mist_core.check_auth(email=member1_email,
                                        password=member1_password).post()

        assert_response_ok(response)
        api_token_id = response.json().get('id', None)
        api_token = response.json().get('token', None)

        cache.set('rbac/member1_api_token_id', api_token_id)
        cache.set('rbac/member1_api_token', api_token)

        response = mist_core.check_auth(email=member2_email,
                                        password=member2_password).post()

        assert_response_ok(response)
        api_token_id = response.json().get('id', None)
        api_token = response.json().get('token', None)

        cache.set('rbac/member2_api_token_id', api_token_id)
        cache.set('rbac/member2_api_token', api_token)

        print "Success!!!!"

    def test_add_teams(self, cache, pretty_print, mist_core, owner_api_token):
        print "\n>>> POSTing /teams to add a team to org"
        org_id = cache.get('rbac/org_id', '')
        member1_api_token = cache.get('rbac/member1_api_token', '')

        # get a random new team name
        response = mist_core.list_teams(org_id=org_id,
                                        api_token=owner_api_token).get()
        assert_response_ok(response)
        cache.set('rbac/member1_team_name',
                  get_random_team_name(json.loads(response.content)))

        # try to add a team with a random user
        response = mist_core.add_team(
            name=cache.get('rbac/member1_team_name', ''),
            description='bla',
            org_id=org_id,
            api_token=member1_api_token).post()
        assert_response_unauthorized(response)

        # add a team using the org owner
        response = mist_core.add_team(
            name=cache.get('rbac/member1_team_name', ''),
            description='bla',
            org_id=org_id,
            api_token=owner_api_token).post()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        assert_is_not_none(rjson.get('id'),
                           "Did not get an id back in the response")
        cache.set('rbac/member1_team_id', rjson['id'])

        # get another random team name and add a second team
        response = mist_core.list_teams(org_id=org_id,
                                        api_token=owner_api_token).get()
        assert_response_ok(response)
        cache.set('rbac/member2_team_name',
                  get_random_team_name(json.loads(response.content)))

        response = mist_core.add_team(
            name=cache.get('rbac/member2_team_name', ''),
            description='bla',
            org_id=org_id,
            api_token=owner_api_token).post()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        assert_is_not_none(rjson.get('id'),
                           "Did not get an id back in the response")
        cache.set('rbac/member2_team_id', rjson['id'])
        print "Success!!!"

    def test_list_teams(self, pretty_print, mist_core, cache, owner_api_token):
        print "\n>>> GETing /teams to list an org's teams"
        org_id = cache.get('rbac/org_id', '')
        member1_api_token = cache.get('rbac/member1_api_token', '')
        member2_api_token = cache.get('rbac/member2_api_token', '')

        response = mist_core.list_teams(org_id=org_id,
                                        api_token=owner_api_token).get()
        response1 = mist_core.list_teams(org_id=org_id,
                                         api_token=member1_api_token).get()
        response2 = mist_core.list_teams(org_id=org_id,
                                         api_token=member2_api_token).get()
        assert_response_ok(response)
        assert_response_unauthorized(response1)
        assert_response_unauthorized(response2)
        teams = json.loads(response.content)
        for team in teams:
            if team['name'].lower() == 'owners':
                cache.set('rbac/owners_team_id', team['id'])
                break

        print "Success!!!!"

    def test_show_team_for_owner(self, pretty_print, mist_core, cache):
        print "\n>>> GETing /teams to check each of one an org's teams"
        org_id = cache.get('rbac/org_id', '')
        teams = cache.get('rbac/teams', '')

        member1_api_token = cache.get('rbac/member1_api_token', '')
        member2_api_token = cache.get('rbac/member2_api_token', '')

        owner_api_token = cache.get('rbac/owner_api_token', '')
        response = mist_core.show_team(api_token=owner_api_token,
                                       org_id=org_id, team_id=team_id).get()
        assert_response_ok(response)

        team_id = teams[0][0]
        assert_response_unauthorized(
            mist_core.show_team(api_token=member1_api_token, org_id=org_id,
                                team_id=team_id).get())
        assert_response_unauthorized(
            mist_core.show_team(api_token=member2_api_token, org_id=org_id,
                                team_id=team_id).get())
        print "Success!!!!"

    def test_show_user_org_for_members(self, pretty_print, mist_core, cache,
                                   member1_api_token, member1_email,
                                   member1_password, member2_api_token,
                                   member2_email, member2_password):
        print "\n>>> GETing / to get org of both members"

        org_id = cache.get('rbac/org_id', '')

        response = mist_core.create_token(api_token=member1_api_token,
                                          email=member1_email,
                                          password=member1_password,
                                          org_id=org_id).post()

        assert_response_ok(response)
        api_token_id = response.json().get('id', None)
        api_token = response.json().get('token', None)

        cache.set('rbac/member1_api_token_id', api_token_id)
        cache.set('rbac/member1_api_token', api_token)

        member1_api_token = api_token

        response = mist_core.create_token(api_token=member2_api_token,
                                          email=member2_email,
                                          password=member2_password,
                                          org_id=org_id).post()

        assert_response_ok(response)
        api_token_id = response.json().get('id', None)
        api_token = response.json().get('token', None)

        cache.set('rbac/member2_api_token_id', api_token_id)
        cache.set('rbac/member2_api_token', api_token)

        member2_api_token = api_token

        response1 = mist_core.show_user_org(api_token=member1_api_token).get()
        response2 = mist_core.show_user_org(api_token=member2_api_token).get()
        assert_response_ok(response1)
        assert_response_ok(response2)
        assert_equal(cache.get('rbac/org_id', ''), response1.json().get('id'),
                     "Member's organization id does not match owner's")
        assert_equal(cache.get('rbac/org_id', ''), response2.json().get('id'),
                     "Member's organization id does not match owner's")
        print "Success!!!!"

    def test_edit_team(self, cache, pretty_print, mist_core,
                       member1_api_token):
        print "\n>>> PUTing /team to edit an org's team"
        org_id = cache.get('rbac/org_id', '')
        team_id = cache.get('rbac/member1_team_id', '')
        owner_api_token = cache.get('rbac/owner_api_token', '')

        # get another random team name to rename first team
        response = mist_core.list_teams(org_id=org_id,
                                        api_token=owner_api_token).get()
        assert_response_ok(response)
        teams_list = json.loads(response.content)

        member1_team_name = get_random_team_name(teams_list)

        # use a random user to edit team
        response = mist_core.edit_team(org_id=org_id, team_id=team_id,
                                       name='bla',
                                       description='description2',
                                       api_token=member1_api_token).put()
        assert_response_unauthorized(response)

        # edit team with the organization owner
        response = mist_core.edit_team(org_id=org_id, team_id=team_id,
                                       name=member1_team_name,
                                       description='description2',
                                       api_token=owner_api_token).put()
        assert_response_ok(response)

        # make sure that the team name has been updated
        response = mist_core.show_team(api_token=owner_api_token,
                                       org_id=org_id, team_id=team_id).get()
        assert_response_ok(response)
        assert_equal(member1_team_name, json.loads(response.content)['name'])

        # set new team name to cache
        cache.set('rbac/member1_team_name', member1_team_name)

        print "Success!!!!"

    # def test_invite_members_to_team(self, cache, pretty_print, mist_core,
    #                                  owner_api_token, org_name, owner_email,
    #                                  owner_password, member1_email, member1_password,
    #                                   member2_email, member2_password):
    #     print "\n>>> Posting / to add members to team"
    #     import ipdb
    #     ipdb.set_trace()
    #     org_id = cache.get('rbac/org_id', '')
    #     member1_api_token = cache.get('rbac/member1_api_token', '')
    #     member2_api_token = cache.get('rbac/member2_api_token', '')
    #
    #     # create an new team
    #     response = mist_core.add_team(
    #         name= "skata",                  # cache.get('rbac/member1_team_name', ''),
    #         description='',
    #         org_id=org_id,
    #         api_token=owner_api_token).post()
    #     assert_response_ok(response)
    #     rjson = json.loads(response.content)
    #     assert_is_not_none(rjson.get('id'),
    #                        "Did not get an id back in the response")
    #     cache.set('rbac/member1_team_id', rjson['id'])
    #
    #     # add member1 to new team
    #     response = mist_core.invite_member_to_team(org_id=org_id,
    #                                                team_id=cache.get(
    #                                                    'rbac/member1_team_id',
    #                                                    ''),
    #                                                email=member1_email,
    #                                                api_token=owner_api_token).post()
    #     assert_response_ok(response)
    #     member_id = json.loads(response.content)
    #     assert_is_not_none(member_id,
    #                        "Did not get an id back in the response")
    #     cache.set('rbac/member1_id', member_id)
    #
    #     response = mist_core.show_user_invitations(api_token=member1_api_token).get()
    #
    #     inv_json = response.json()
    #     org_id = None
    #     for org in inv_json:
    #         if org_name == org['name']:
    #             org_id = org['id']
    #             break
    #     assert_is_not_none(org_id)
    #     cache.set('rbac/org_id', org_id)
    #
    # def test_member_to_team(self, cache, pretty_print, mist_core,
    #                         member1_email, member2_email):
    #     print "\n>>> POSTing /team_members to invite a new member to an org's" \
    #           " team"
    #     org_id = cache.get('rbac/org_id', '')
    #     owner_api_token = cache.get('rbac/owner_api_token', '')
    #
    #     # add member1 to new team
    #     response = mist_core.invite_member_to_team(org_id=org_id,
    #                                                team_id=cache.get(
    #                                                    'rbac/member1_team_id',
    #                                                    ''),
    #                                                email=member1_email,
    #                                                api_token=owner_api_token).post()
    #     assert_response_ok(response)
    #     member_id = json.loads(response.content)
    #     assert_is_not_none(member_id,
    #                        "Did not get an id back in the response")
    #     cache.set('rbac/member1_id', member_id)
    #
    #     # add member1 to other team
    #     response = mist_core.invite_member_to_team(org_id=org_id,
    #                                                team_id=cache.get(
    #                                                    'rbac/member2_team_id',
    #                                                    ''),
    #                                                email=member1_email,
    #                                                api_token=owner_api_token).post()
    #     assert_response_ok(response)
    #     member_id = json.loads(response.content)
    #     assert_is_not_none(member_id,
    #                        "Did not get an id back in the response")
    #
    #     # add member2 to other team
    #     response = mist_core.invite_member_to_team(org_id=org_id,
    #                                                team_id=cache.get(
    #                                                    'rbac/member2_team_id',
    #                                                    ''),
    #                                                email=member2_email,
    #                                                api_token=owner_api_token).post()
    #     assert_response_ok(response)
    #     member_id = json.loads(response.content)
    #     assert_is_not_none(member_id,
    #                        "Did not get an id back in the response")
    #     cache.set('rbac/member2_id', member_id)
    #
    #     print "Success!!!!"
    #
    # def test_delete_member_from_team(self, cache, pretty_print, mist_core):
    #
    #     print "\n>>> DELETEing /team_members to remove a member from an" \
    #           " org's team"
    #     org_id = cache.get('rbac/org_id', '')
    #     team_id = cache.get('rbac/member2_team_id', '')
    #     user_id = cache.get('rbac/member1_id', '')
    #     owner_api_token = cache.get('rbac/owner_api_token', '')
    #
    #     # delete member1 from other team
    #     response = mist_core.delete_member_from_team(org_id=org_id,
    #                                                  team_id=team_id,
    #                                                  user_id=user_id,
    #                                                  api_token=owner_api_token).delete()
    #     assert_response_ok(response)
    #
    #     # re-delete member1 from other team
    #     response = mist_core.delete_member_from_team(org_id=org_id,
    #                                                  team_id=team_id,
    #                                                  user_id=user_id,
    #                                                  api_token=owner_api_token).delete()
    #     assert_response_not_found(response)
    #
    #     print "Success!!!!"
    #
    # def test_script_actions_and_policy_enforcement(self, pretty_print,
    #                                                mist_core, cache,
    #                                                member1_api_token,
    #                                                member2_api_token):
    #
    #     print "\n>>>Test Script actions with multiple users"
    #     owner_api_token = cache.get('rbac/owner_api_token', '')
    #     # owner adds a bash script
    #     response = mist_core.list_scripts(api_token=owner_api_token).get()
    #     assert_response_ok(response)
    #     _, owner_script_id = add_bash_script(mist_core,
    #                                                          owner_api_token)
    #
    #     # member1 should not be able to see the script
    #     response = mist_core.list_scripts(api_token=member1_api_token).get()
    #     assert_response_ok(response)
    #     assert_list_empty(get_scripts_with_name(owner_script_id,
    #                                             json.loads(response.content)))
    #
    #     cache.set('rbac/owner_script_id', owner_script_id)
    #
    #     org_id = cache.get('rbac/org_id', '')
    #     member1_team_id = cache.get('rbac/member1_team_id', '')
    #
    #     # try to change the member1 team default policy to ALLOW as member1.
    #     # it should fail
    #     response = mist_core.edit_team_policy_operator(org_id=org_id,
    #                                                    team_id=member1_team_id,
    #                                                    policy_operator='ALLOW',
    #                                                    api_token=member1_api_token).post()
    #     assert_response_unauthorized(response)
    #
    #     # try to change the member1 team default policy to ALLOW as owner.
    #     # it should succeed
    #     response = mist_core.edit_team_policy_operator(org_id=org_id,
    #                                                    team_id=member1_team_id,
    #                                                    policy_operator='ALLOW',
    #                                                    api_token=owner_api_token).post()
    #     assert_response_ok(response)
    #
    #     # member1 should now be able to see the script
    #     response = mist_core.list_scripts(api_token=member1_api_token).get()
    #     assert_response_ok(response)
    #     assert_list_not_empty(get_scripts_with_name(owner_script_id,
    #                                                 json.loads(
    #                                                     response.content)))
    #
    #     # change the member1 team default policy back to DENY.
    #     response = mist_core.edit_team_policy_operator(org_id=org_id,
    #                                                    team_id=member1_team_id,
    #                                                    policy_operator='DENY',
    #                                                    api_token=owner_api_token).post()
    #
    #     assert_response_ok(response)
    #
    #     # member1 should not be able to see the script again
    #     response = mist_core.list_scripts(api_token=member1_api_token).get()
    #     assert_response_ok(response)
    #     assert_list_empty(get_scripts_with_name(owner_script_id,
    #                                             json.loads(response.content)))
    #
    #     script_allow_read_policy = {'operator': 'ALLOW',
    #                                 'action': 'read',
    #                                 'rtype': 'script',
    #                                 'rid': '',
    #                                 'rtags': {}
    #                                 }
    #     # member1 adds policy in member1_team to be able to see the new script
    #     # it should fail
    #     response = mist_core.append_rule_to_policy(api_token=member1_api_token,
    #                                                org_id=org_id,
    #                                                team_id=member1_team_id,
    #                                                **script_allow_read_policy).post()
    #
    #     assert_response_unauthorized(response)
    #
    #     # owner adds policy in member1_team to be able to see the new script
    #     # it should succeed
    #     response = mist_core.append_rule_to_policy(api_token=owner_api_token,
    #                                                org_id=org_id,
    #                                                team_id=member1_team_id,
    #                                                **script_allow_read_policy).post()
    #
    #     assert_response_ok(response)
    #
    #     # member1 should be able to see the script, member2 should be unable
    #     response = mist_core.list_scripts(api_token=member1_api_token).get()
    #     assert_response_ok(response)
    #     assert_list_not_empty(get_scripts_with_name(owner_script_id,
    #                                                 json.loads(
    #                                                     response.content)))
    #
    #     response = mist_core.list_scripts(api_token=member2_api_token).get()
    #     assert_response_ok(response)
    #     assert_list_empty(get_scripts_with_name(owner_script_id,
    #                                             json.loads(response.content)))
    #
    #     # member1 tries to add a script. it should fail with forbidden
    #     member1_script_id = get_random_script_name(json.loads(response.content))
    #     response = mist_core.add_script(api_token=member1_api_token,
    #                                     name=member1_script_id,
    #                                     location_type='inline',
    #                                     exec_type='executable',
    #                                     script=bash_script).post()
    #     assert_response_forbidden(response)
    #
    #     script_allow_add_policy = {'operator': 'ALLOW',
    #                                'action': 'add',
    #                                'rtype': 'script',
    #                                'rid': '',
    #                                'rtags': {'bla': 'bla'}
    #                                }
    #     # owner adds policy in member1_team to be able to allow add script
    #     response = mist_core.append_rule_to_policy(api_token=owner_api_token,
    #                                                org_id=org_id,
    #                                                team_id=member1_team_id,
    #                                                **script_allow_add_policy).post()
    #     assert_response_ok(response)
    #
    #     # member1 should succeed in adding script, member2 should fail
    #     response = mist_core.add_script(api_token=member1_api_token,
    #                                     name=member1_script_id,
    #                                     location_type='inline',
    #                                     exec_type='executable',
    #                                     script=bash_script).post()
    #     assert_response_ok(response)
    #     response = mist_core.list_scripts(api_token=member1_api_token).get()
    #     assert_response_ok(response)
    #     script = get_scripts_with_name(
    #         member1_script_id,
    #         json.loads(response.content))
    #     assert_list_not_empty(script, "Script was added but is not visible in"
    #                                   " the list of scripts")
    #
    #     response = mist_core.add_script(api_token=member2_api_token,
    #                                     name=member1_script_id,
    #                                     location_type='inline',
    #                                     exec_type='executable',
    #                                     script=bash_script).post()
    #     assert_response_forbidden(response)
    #
    #     cache.set('rbac/member1_script_id', member1_script_id)
    #
    #     print "Success!!!!"
    #
    # def test_key_actions_and_policy_enforcement(self, pretty_print, mist_core,
    #                                             cache,
    #                                             member1_api_token,
    #                                             member2_api_token):
    #
    #     print "\n>>>Test key actions with multiple users"
    #     owner_api_token = cache.get('rbac/owner_api_token', '')
    #     # owner creates a random key name
    #     response = mist_core.list_keys(api_token=owner_api_token).get()
    #     assert_response_ok(response)
    #     owner_key_id = get_random_key_id(json.loads(response.content))
    #
    #     # owner adds the key
    #     response = mist_core.add_key(
    #         id=owner_key_id,
    #         private=config.API_TESTING_MACHINE_PRIVATE_KEY,
    #         api_token=owner_api_token).put()
    #     assert_response_ok(response)
    #
    #     # owner asserts the key is added and listed
    #     response = mist_core.list_keys(api_token=owner_api_token).get()
    #     assert_response_ok(response)
    #     keys = get_keys_with_id(owner_key_id,
    #                             json.loads(response.content))
    #     assert_list_not_empty(keys,
    #                           "Key was added through the api but is not "
    #                           "visible in the list of keys")
    #     owner_key_id = keys[0]['id']
    #
    #     cache.set('rbac/owner_key_id', owner_key_id)
    #
    #     # member1 should not be able to see the new key
    #     response = mist_core.list_keys(api_token=member1_api_token).get()
    #     assert_response_ok(response)
    #     assert_list_empty(get_keys_with_id(owner_key_id,
    #                                        json.loads(response.content)))
    #
    #     org_id = cache.get('rbac/org_id', '')
    #     member1_team_id = cache.get('rbac/member1_team_id', '')
    #
    #     key_allow_read_policy = {'operator': 'ALLOW',
    #                              'action': 'read',
    #                              'rtype': 'key',
    #                              'rid': '',
    #                              'rtags': {}
    #                              }
    #
    #     # owner adds policy in member1_team to be able to see the new key
    #     # it should succeed
    #     response = mist_core.append_rule_to_policy(api_token=owner_api_token,
    #                                                org_id=org_id,
    #                                                team_id=member1_team_id,
    #                                                **key_allow_read_policy).post()
    #     assert_response_ok(response)
    #
    #     # member1 should be able to see the script, member2 should be unable
    #     response = mist_core.list_keys(api_token=member1_api_token).get()
    #     assert_response_ok(response)
    #     assert_list_not_empty(get_keys_with_id(owner_key_id,
    #                                            json.loads(response.content)))
    #
    #     response = mist_core.list_keys(api_token=member2_api_token).get()
    #     assert_response_ok(response)
    #     assert_list_empty(get_keys_with_id(owner_key_id,
    #                                        json.loads(response.content)))
    #
    #     # member1 tries to add a key. it should fail with forbidden
    #     member1_key_id = get_random_key_id(json.loads(response.content))
    #     response = mist_core.add_key(
    #         id=member1_key_id,
    #         private=config.API_TESTING_MACHINE_PRIVATE_KEY,
    #         api_token=member1_api_token).put()
    #     assert_response_forbidden(response)
    #
    #     key_allow_add_policy = {'operator': 'ALLOW',
    #                             'action': 'add',
    #                             'rtype': 'key',
    #                             'rid': '',
    #                             'rtags': {'bla': 'bla'}
    #                             }
    #     # owner adds policy in member1_team to be able to allow add script
    #     response = mist_core.append_rule_to_policy(api_token=owner_api_token,
    #                                                org_id=org_id,
    #                                                team_id=member1_team_id,
    #                                                **key_allow_add_policy).post()
    #     assert_response_ok(response)
    #
    #     # member1 should succeed in adding key, member2 should fail
    #     response = mist_core.add_key(
    #         id=member1_key_id,
    #         private=config.API_TESTING_MACHINE_PRIVATE_KEY,
    #         api_token=member1_api_token).put()
    #     assert_response_ok(response)
    #
    #     response = mist_core.list_keys(api_token=member1_api_token).get()
    #     assert_response_ok(response)
    #     keys = get_keys_with_id(member1_key_id,
    #                             json.loads(response.content))
    #     assert_list_not_empty(keys, "Key was added but is not visible in"
    #                                 " the list of keys")
    #
    #     response = mist_core.add_key(
    #         id=member1_key_id,
    #         private=config.API_TESTING_MACHINE_PRIVATE_KEY,
    #         api_token=member2_api_token).put()
    #     assert_response_forbidden(response)
    #
    #     cache.set('rbac/member1_key_id', member1_key_id)
    #
    #     print "Success!!!!"
    #
    # def test_multiple_actions(self, mist_core, cache,
    #                           member1_api_token, member2_api_token,
    #                           cloud_name, api_test_machine_name):
    #
    #     print "\n>>>Testing cloud actions"
    #     owner_api_token = cache.get('rbac/owner_api_token', '')
    #     # owner finds the cloud that will be used
    #     response = mist_core.list_clouds(api_token=owner_api_token).get()
    #     assert_response_ok(response)
    #     cloud_id = None
    #     for cloud in json.loads(response.content):
    #         if cloud['title'] == cloud_name:
    #             cloud_id = cloud['id']
    #             break
    #     assert_is_not_none(cloud_id)
    #     cache.set('rbac/cloud_id', cloud_id)
    #
    #     # owner will find the id of the machine that will be used.
    #     # this machine id is not the one provided by mist.io but by the
    #     # cloud provider so it will only be kept temporarily
    #     response = mist_core.list_machines(api_token=owner_api_token,
    #                                        cloud_id=cloud_id).get()
    #     assert_response_ok(response)
    #     machine_id = None
    #     for machine in json.loads(response.content):
    #         if machine['name'] == api_test_machine_name:
    #             machine_id = machine['id']
    #             break
    #     assert_is_not_none(machine_id)
    #
    #     allow_script_run_policy = {'operator': 'ALLOW',
    #                                'action': 'run',
    #                                'rtype': 'script',
    #                                'rid': '',
    #                                'rtags': {'bla': 'bla'}
    #                                }
    #
    #     allow_key_read_private_policy = {'operator': 'ALLOW',
    #                                      'action': 'read_private',
    #                                      'rtype': 'key',
    #                                      'rid': '',
    #                                      'rtags': {'bla': 'bla'}
    #                                      }
    #
    #     allow_cloud_read_policy = {'operator': 'ALLOW',
    #                                'action': 'read',
    #                                'rtype': 'cloud',
    #                                'rid': '',
    #                                'rtags': {}
    #                                }
    #
    #     allow_machine_read_policy = {'operator': 'ALLOW',
    #                                  'action': 'read',
    #                                  'rtype': 'machine',
    #                                  'rid': '',
    #                                  'rtags': {}
    #                                  }
    #
    #     allow_machine_associate_key_policy = {'operator': 'ALLOW',
    #                                           'action': 'associate_key',
    #                                           'rtype': 'machine',
    #                                           'rid': '',
    #                                           'rtags': {'bla': 'bla'}
    #                                           }
    #
    #     allow_machine_run_script_policy = {'operator': 'ALLOW',
    #                                        'action': 'run_script',
    #                                        'rtype': 'machine',
    #                                        'rid': '',
    #                                        'rtags': {}
    #                                        }
    #
    #     org_id = cache.get('rbac/org_id', '')
    #     member1_team_id = cache.get('rbac/member1_team_id', '')
    #     member1_key_id = cache.get('rbac/member1_key_id', '')
    #     member1_script_id = cache.get('rbac/member1_script_id', '')
    #
    #     # owner adds policy to allow read on cloud
    #     response = mist_core.append_rule_to_policy(api_token=owner_api_token,
    #                                                org_id=org_id,
    #                                                team_id=member1_team_id,
    #                                                **allow_cloud_read_policy).post()
    #     assert_response_ok(response)
    #
    #     # member1 can list clouds
    #     response = mist_core.list_clouds(api_token=owner_api_token).get()
    #     assert_response_ok(response)
    #     found = False
    #     for cloud in json.loads(response.content):
    #         if cloud['title'] == cloud_name:
    #             found = True
    #             break
    #     assert found, 'Cloud has not been found in the list'
    #
    #     # member2 can not list clouds
    #     response = mist_core.list_clouds(api_token=member2_api_token).get()
    #     assert_response_forbidden(response)
    #
    #     # member1 tries to associate key with machine. it fails
    #     response = mist_core.associate_key(api_token=member1_api_token,
    #                                        cloud_id=cloud_id,
    #                                        machine_id=machine_id,
    #                                        key_id=member1_key_id).put()
    #     assert_response_forbidden(response)
    #
    #     # owner adds policy to allow key read private
    #     response = mist_core.append_rule_to_policy(api_token=owner_api_token,
    #                                                org_id=org_id,
    #                                                team_id=member1_team_id,
    #                                                **allow_key_read_private_policy).post()
    #     assert_response_ok(response)
    #
    #     # member1 tries to associate the key with the machine. it fails
    #     response = mist_core.associate_key(api_token=member1_api_token,
    #                                        cloud_id=cloud_id,
    #                                        machine_id=machine_id,
    #                                        key=member1_key_id).put()
    #     assert_response_forbidden(response)
    #
    #     # owner adds policy to allow associate machine on machine
    #     response = mist_core.append_rule_to_policy(api_token=owner_api_token,
    #                                                org_id=org_id,
    #                                                team_id=member1_team_id,
    #                                                **allow_machine_associate_key_policy).post()
    #     assert_response_ok(response)
    #
    #     # member1 tries to associate the key with the machine. it succeeds
    #     response = mist_core.associate_key(api_token=member1_api_token,
    #                                        cloud_id=cloud_id,
    #                                        machine_id=machine_id,
    #                                        key=member1_key_id).put()
    #     assert_response_forbidden(response)
    #
    #     # member1 still can not run script
    #     response = mist_core.run_script(api_token=member1_api_token,
    #                                     script_id=member1_script_id,
    #                                     cloud_id=cloud_id,
    #                                     machine_id=machine_id).post()
    #     assert_response_forbidden(response)
    #
    #     # member1 can not list machines
    #     response = mist_core.list_machines(api_token=owner_api_token,
    #                                        cloud_id=cloud_id).get()
    #     assert_response_forbidden(response)
    #
    #     # owner adds policy for member1 to list machines
    #     response = mist_core.append_rule_to_policy(api_token=owner_api_token,
    #                                                org_id=org_id,
    #                                                team_id=member1_team_id,
    #                                                **allow_machine_read_policy).post()
    #     assert_response_ok(response)
    #
    #     # member1 can list machines
    #     response = mist_core.list_machines(api_token=owner_api_token,
    #                                        cloud_id=cloud_id).get()
    #     assert_response_ok(response)
    #     machine_id = None
    #     for machine in json.loads(response.content):
    #         if machine['name'] == api_test_machine_name:
    #             machine_id = machine['id']
    #             break
    #     assert_is_not_none(machine_id,
    #                        "Machine was not available in the list of machines")
    #     cache.set('rbac/machine_id', machine_id)
    #
    #     # member2 can not list machines
    #     response = mist_core.list_machines(api_token=owner_api_token,
    #                                        cloud_id=cloud_id).get()
    #     assert_response_forbidden(response)
    #
    #     # member1 can not run script
    #     response = mist_core.run_script(api_token=member1_api_token,
    #                                     script_id=member1_script_id,
    #                                     cloud_id=cloud_id,
    #                                     machine_id=machine_id).post()
    #     assert_response_forbidden(response)
    #
    #     # owner adds policy to allow run script on machine
    #     response = mist_core.append_rule_to_policy(api_token=owner_api_token,
    #                                                org_id=org_id,
    #                                                team_id=member1_team_id,
    #                                                **allow_machine_run_script_policy).post()
    #     assert_response_ok(response)
    #
    #     # member1 still can't run script
    #     response = mist_core.run_script(api_token=member1_api_token,
    #                                     script_id=member1_script_id,
    #                                     cloud_id=cloud_id,
    #                                     machine_id=machine_id).post()
    #     assert_response_forbidden(response)
    #
    #     # owner adds policy in member1_team to allow script run
    #     response = mist_core.append_rule_to_policy(api_token=owner_api_token,
    #                                                org_id=org_id,
    #                                                team_id=member1_team_id,
    #                                                **allow_script_run_policy).post()
    #     assert_response_ok(response)
    #
    #     # member1 can run script
    #     response = mist_core.run_script(api_token=member1_api_token,
    #                                     script_id=member1_script_id,
    #                                     cloud_id=cloud_id,
    #                                     machine_id=machine_id).post()
    #     assert_response_ok(response)
    #
    #     # member2 can not run script
    #     response = mist_core.run_script(api_token=member2_api_token,
    #                                     script_id=member1_script_id,
    #                                     cloud_id=cloud_id,
    #                                     machine_id=machine_id).post()
    #     assert_response_forbidden(response)
    #
    #     print "Success!!!!"
    #
    # def test_delete_keys_and_scripts(self, pretty_print, mist_core, cache,
    #                                  member1_api_token,
    #                                  member2_api_token):
    #
    #     print "\n>>> Delete keys and scripts created before and check policy" \
    #           " enforcement"
    #     owner_api_token = cache.get('rbac/owner_api_token', '')
    #     script_allow_remove_policy = {'operator': 'ALLOW',
    #                                   'action': 'remove',
    #                                   'rtype': 'script',
    #                                   'rid': '',
    #                                   'rtags': {'bla': 'bla'}
    #                                   }
    #
    #     key_allow_remove_policy = {'operator': 'ALLOW',
    #                                'action': 'remove',
    #                                'rtype': 'key',
    #                                'rid': '',
    #                                'rtags': {'bla': 'bla'}
    #                                }
    #
    #     owner_key_id = cache.get('rbac/owner_key_id', '')
    #     member1_key_id = cache.get('rbac/member1_key_id', '')
    #     owner_script_id = cache.get('rbac/owner_script_id', '')
    #     member1_script_id = cache.get('rbac/member1_script_id', '')
    #
    #     org_id = cache.get('rbac/org_id', '')
    #     member1_team_id = cache.get('rbac/member1_team_id', '')
    #
    #     # Scripts section
    #
    #     # member1 tries to delete his script. should fail
    #     response = mist_core.delete_script(
    #         script_id=member1_script_id,
    #         api_token=member1_api_token).delete()
    #     assert_response_unauthorized(response)
    #
    #     # owner adds policy in member1_team to allow remove script
    #     response = mist_core.append_rule_to_policy(api_token=owner_api_token,
    #                                                org_id=org_id,
    #                                                team_id=member1_team_id,
    #                                                **script_allow_remove_policy).post()
    #     assert_response_ok(response)
    #
    #     # member2 tries to delete member1's script. should fail
    #     response = mist_core.delete_script(
    #         script_id=member1_script_id,
    #         api_token=member2_api_token).delete()
    #     assert_response_unauthorized(response)
    #
    #     # member1 tries to delete his script. should succeed
    #     response = mist_core.delete_script(
    #         script_id=member1_script_id,
    #         api_token=member1_api_token).delete()
    #     assert_response_ok(response)
    #
    #     # member1 tries to delete owner's script. should fail
    #     response = mist_core.delete_script(
    #         script_id=owner_script_id,
    #         api_token=member1_api_token).delete()
    #     assert_response_unauthorized(response)
    #
    #     # owner deletes his script. should succeed
    #     response = mist_core.delete_script(
    #         script_id=owner_script_id,
    #         api_token=owner_api_token).delete()
    #     assert_response_ok(response)
    #
    #     # Keys section
    #
    #     # member1 tries to delete his key. should fail
    #     response = mist_core.delete_key(
    #         key_id=member1_key_id,
    #         api_token=member1_api_token).delete()
    #     assert_response_forbidden(response)
    #
    #     # owner adds policy in member1_team to allow remove script
    #     response = mist_core.append_rule_to_policy(api_token=owner_api_token,
    #                                                org_id=org_id,
    #                                                team_id=member1_team_id,
    #                                                **key_allow_remove_policy).post()
    #     assert_response_ok(response)
    #
    #     # member2 tries to delete member1's key. should fail
    #     response = mist_core.delete_key(
    #         key_id=member1_key_id,
    #         api_token=member2_api_token).delete()
    #     assert_response_forbidden(response)
    #
    #     # member1 tries to delete his key. should succeed
    #     response = mist_core.delete_key(
    #         key_id=member1_key_id,
    #         api_token=member1_api_token).delete()
    #     assert_response_ok(response)
    #
    #     # member1 tries to delete owner's key. should fail
    #     response = mist_core.delete_key(
    #         key_id=owner_key_id,
    #         api_token=member1_api_token).delete()
    #     assert_response_forbidden(response)
    #
    #     # owner deletes his key. should succeed
    #     response = mist_core.delete_key(
    #         key_id=owner_key_id,
    #         api_token=owner_api_token).delete()
    #     assert_response_ok(response)
    #
    #     print "Success!!!!"
    #
    # def test_delete_teams(self, cache, pretty_print, mist_core,
    #                       member1_api_token):
    #     print "\n>>> DELETEing /team to delete an org's team"
    #     org_id = cache.get('rbac/org_id', '')
    #     owner_api_token = cache.get('rbac/owner_api_token', '')
    #     member1_team_id = cache.get('rbac/member1_team_id', '')
    #     member2_team_id = cache.get('rbac/member2_team_id', '')
    #
    #     # member1 tries to delete a team. it should fail
    #     response = mist_core.delete_team(org_id=org_id,
    #                                      team_id=member1_team_id,
    #                                      api_token=member1_api_token).delete()
    #     assert_response_unauthorized(response)
    #
    #     # owner tries to delete a team with wrong org id. it should fail
    #     response = mist_core.delete_team(org_id=org_id[:-1],
    #                                      team_id=member1_team_id,
    #                                      api_token=owner_api_token).delete()
    #     assert_response_unauthorized(response)
    #
    #     # owner tries to delete a team with wrong team id. it should fail
    #     response = mist_core.delete_team(org_id=org_id,
    #                                      team_id=member1_team_id[:-1],
    #                                      api_token=owner_api_token).delete()
    #     assert_response_not_found(response)
    #
    #     # owner tries to delete teams. it should succeed
    #     response = mist_core.delete_team(org_id=org_id,
    #                                      team_id=member1_team_id,
    #                                      api_token=owner_api_token).delete()
    #     assert_response_ok(response)
    #
    #     response = mist_core.delete_team(org_id=org_id,
    #                                      team_id=member2_team_id,
    #                                      api_token=owner_api_token).delete()
    #     assert_response_ok(response)
    #
    #     # owner tries to re-delete a team. it should fail
    #     response = mist_core.delete_team(org_id=org_id,
    #                                      team_id=member1_team_id,
    #                                      api_token=owner_api_token).delete()
    #     assert_response_not_found(response)
    #
    #     owner_api_token_id = cache.get('rbac/owner_api_token_id', '')
    #     response = mist_core.revoke_token(api_token=owner_api_token,
    #                                       api_token_id=owner_api_token_id).delete()
    #     assert_response_ok(response)
    #
    #     print "Success!!!!"
