import sys
from pprint import pprint

from mist.core.tests.api.helpers import *


#############################################################################
# Unit testing
#############################################################################

def test_000_initialize_org_team_for_owner(cache, pretty_print, mist_core,
                                     owner_api_token, org_name, owner_email,
                                     owner_password):
    print "\nfor intialize org_id, team_id"
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

    # get a random new team name
    response = mist_core.list_teams(org_id=org_id,
                                    api_token=owner_api_token).get()
    assert_response_ok(response)
    cache.set('team/team_name',
    get_random_team_name(json.loads(response.content)))

    # add a team using the org owner
    response = mist_core.add_team(
         name=cache.get('team/team_name', ''),
         description='bla',
         org_id=org_id,
         api_token=owner_api_token).post()
    assert_response_ok(response)
    rjson = json.loads(response.content)
    assert_is_not_none(rjson.get('id'),
                        "Did not get an id back in the response")
    cache.set('team/team_id', rjson['id'])

    print "Success!!!!"


def test_001_show_user_org_without_token(pretty_print, mist_core):
    print "\n>>> GETing /org to get a user org without token"
    response = mist_core.show_user_org(api_token='').get()
    assert_response_unauthorized(response)
    print "Success!!!!"


def test_0021_add_team_without_name(cache, pretty_print, mist_core,
                                    owner_api_token):
    print "\n>>> POSTing /teams to add a team to org"
    org_id = cache.get('org/org_id','')
    print org_id
    response = mist_core.add_team(name='', description='',
                                  org_id=org_id,
                                  api_token=owner_api_token).post()
    assert_response_bad_request(response)

    print "Success!!!"


def test_0041_list_team_with_wrong_org_id(cache, pretty_print, mist_core,
                                          owner_api_token):
    print "\n>>> GETing /teams to list an org's teams with wrong org's id"
    org_id = cache.get('org/org_id','')[:-2]
    response = mist_core.list_teams(org_id=org_id,
                                    api_token=owner_api_token).get()
    assert_response_unauthorized(response)
    print "Success!!!!"


def test_0051_show_team_with_wrong_org_id(cache, pretty_print, mist_core,
                                          owner_api_token):

    print "\n>>> GETing /team to show an org's team with wrong org's id"
    org_id = cache.get('org/org_id','')[:-2]
    team_id = cache.get('team/team_id','')
    response = mist_core.show_team(org_id=org_id,
                                   team_id=team_id,
                                    api_token=owner_api_token).get()
    assert_response_unauthorized(response)
    print "Success!!!!"


def test_005_show_team_with_wrong_team_id(cache, pretty_print, mist_core,
                                          owner_api_token):
    print "\n>>> GETing /team to show an org's team with wrong team's id"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')[:-2]
    response = mist_core.show_team(org_id=org_id,
                                   team_id=team_id,
                                    api_token=owner_api_token).get()
    assert_response_not_found(response)
    print "Success!!!!"


def test_0061_edit_team_with_wrong_org_id(cache, pretty_print, mist_core,
                                          owner_api_token):
    print "\n>>> PUTing /team to edit an org's team with wrong org's id"
    org_id = cache.get('org/org_id','')[:-2]
    team_id = cache.get('team/team_id','')
    response = mist_core.edit_team(org_id=org_id,
                                   team_id=team_id,
                                   name='lala3', description='skata',
                                    api_token=owner_api_token).put()
    assert_response_unauthorized(response)
    print "Success!!!!"


def test_0062_edit_team_with_wrong_team_id(cache, pretty_print, mist_core,
                                           owner_api_token):
    print "\n>>> PUTing /team to edit an org's team with wrong tem's id"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')[:-2]
    response = mist_core.edit_team(org_id=org_id,
                                   team_id=team_id,
                                   name='lala3', description='skata',
                                    api_token=owner_api_token).put()
    assert_response_not_found(response)
    print "Success!!!!"


def test_0071_invite_member_to_team_with_wrong_org_id(cache, pretty_print,
                                                      mist_core,
                                                      owner_api_token):
    print "\n>>> POSTing /team_members to invite a new member to an org's team"
    org_id = cache.get('org/org_id','')[:-2]
    team_id = cache.get('team/team_id','')
    email = 'sag@yahoo.gr'
    response = mist_core.\
        invite_member_to_team(org_id=org_id,
                                               team_id=team_id,
                                               email=email,
                                     api_token=owner_api_token).post()
    assert_response_unauthorized(response)
    print "Success!!!!"


def test_0072_invite_member_to_team_with_wrong_team_id(cache, pretty_print,
                                                       mist_core,
                                                       owner_api_token):
    print "\n>>> POSTing /team_members to invite a new member to an org's team"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')[:-2]
    email = 'sag@yahoo.gr'
    response = mist_core.\
        invite_member_to_team(org_id=org_id,
                              team_id=team_id,
                              email=email, api_token=owner_api_token).post()
    assert_response_not_found(response)
    print "Success!!!!"


def test_0073_invite_member_to_team_without_mail(cache, pretty_print, mist_core,
                                                 owner_api_token):
    print "\n>>> POSTing /team_members to invite a new member to an org's team"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')

    email = ''
    response = mist_core.invite_member_to_team(org_id=org_id, team_id=team_id,
                                               email=email,
                                     api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!!"


def test_0081_delete_member_from_team_with_wrong_org_id(cache,
                                                        pretty_print, mist_core,
                                                        owner_api_token):
    print "\n>>> Deleteing /team_members to delete a member from an org's team"
    org_id = cache.get('org/org_id','')[:-2]
    team_id = cache.get('team/team_id','')
    user_id = cache.get('member/member_id','')

    response = mist_core.delete_member_from_team(org_id=org_id, team_id=team_id,
                                               user_id=user_id,
                                     api_token=owner_api_token).delete()
    assert_response_unauthorized(response)
    print "Success!!!!"


def test_0082_delete_member_from_team_with_wrong_team_id(cache,
                                                         pretty_print, mist_core,
                                                         owner_api_token):
    print "\n>>> Deleteing /team_members to delete a member from an org's team"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')[:-2]
    user_id = cache.get('member/member_id','')

    response = mist_core.delete_member_from_team(org_id=org_id, team_id=team_id,
                                               user_id=user_id,
                                     api_token=owner_api_token).delete()
    assert_response_not_found(response)
    print "Success!!!!"


def test_0083_delete_member_from_team_with_wrong_user_id(cache,
                                                         pretty_print,
                                                         mist_core,
                                                         owner_api_token):
    print "\n>>> Deleteing /team_members to delete a member from an org's team"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')
    user_id = cache.get('member/member_id','')[:-2]

    response = mist_core.delete_member_from_team(org_id=org_id, team_id=team_id,
                                               user_id=user_id,
                                     api_token=owner_api_token).delete()
    assert_response_not_found(response)
    print "Success!!!!"


def test_0091_edit_team_policy_operator_with_wrong_org_id(cache, pretty_print,
                              mist_core, owner_api_token):
    print "\n>>> Posting /team_policy to edit team policy"
    org_id = cache.get('org/org_id','')[:-2]
    team_id = cache.get('team/team_id','')

    policy_operator = "ALLOW"
    response = mist_core.edit_team_policy_operator(org_id=org_id,
                                    team_id=team_id,
                                    policy_operator=policy_operator,
                                    api_token=owner_api_token).post()
    assert_response_unauthorized(response)
    print "Success!!!!"


def test_0092_edit_team_policy_operator_with_wrong_team_id(cache, pretty_print,
                              mist_core, owner_api_token):
    print "\n>>> Posting /team_policy to edit team policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')[:-2]

    policy_operator = "ALLOW"
    response = mist_core.edit_team_policy_operator(org_id=org_id,
                                    team_id=team_id,
                                    policy_operator=policy_operator,
                                    api_token=owner_api_token).post()
    assert_response_not_found(response)
    print "Success!!!!"


def test_0093_edit_team_policy_operator_without_operator(cache, pretty_print,
                              mist_core, owner_api_token):
    print "\n>>> Posting /team_policy to edit team policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')

    policy_operator = ""
    response = mist_core.edit_team_policy_operator(org_id=org_id,
                                    team_id=team_id,
                                    policy_operator=policy_operator,
                                    api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!!"


def test_0101_append_rule_to_policy_with_wrong_org_id(cache, pretty_print,
                              mist_core, owner_api_token):
    print "\n>>> Posting /policy_rules to append new rule to policy"
    org_id = cache.get('org/org_id','')[:-2]
    team_id = cache.get('team/team_id','')
    response = mist_core.append_rule_to_policy(org_id=org_id, team_id=team_id,
                                          api_token=owner_api_token,
                                          operator="ALLOW", action="read",
                                          rtype="key",
                                          rid='7a53482d35fe405ca469e88d041bb114',
                                          rtags={}).post()
    assert_response_unauthorized(response)
    print "Success!!!!"
#

def test_0102_append_rule_to_policy_with_wrong_team_id(cache, pretty_print,
                              mist_core, owner_api_token):
    print "\n>>> Posting /policy_rules to append new rule to policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')[:-2]
    response = mist_core.append_rule_to_policy(org_id=org_id, team_id=team_id,
                                          api_token=owner_api_token,
                                          operator="ALLOW", action="read",
                                          rtype="key",
                                          rid='7a53482d35fe405ca469e88d041bb114',
                                          rtags={}).post()
    assert_response_not_found(response)
    print "Success!!!!"


def test_0103_append_rule_to_policy_without_operator(cache, pretty_print,
                              mist_core, owner_api_token):
    print "\n>>> Posting /policy_rules to append new rule to policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')
    response = mist_core.append_rule_to_policy(org_id=org_id, team_id=team_id,
                                          api_token=owner_api_token,
                                          operator="", action="read",
                                          rtype="key",
                                          rid='7a53482d35fe405ca469e88d041bb114',
                                          rtags={}).post()
    assert_response_bad_request(response)
    print "Success!!!!"


def test_0104_append_rule_to_policy_with_wrong_action(cache, pretty_print,
                              mist_core, owner_api_token):
    print "\n>>> Posting /policy_rules to append new rule to policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')
    response = mist_core.append_rule_to_policy(org_id=org_id, team_id=team_id,
                                          api_token=owner_api_token,
                                          operator="ALLOW", action="try",
                                          rtype="key",
                                          rid='7a53482d35fe405ca469e88d041bb114',
                                          rtags={}).post()
    assert_response_bad_request(response)
    print "Success!!!!"


def test_0105_append_rule_to_policy_with_wrong_rtype(cache, pretty_print,
                              mist_core, owner_api_token):
    print "\n>>> Posting /policy_rules to append new rule to policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')
    response = mist_core.append_rule_to_policy(org_id=org_id, team_id=team_id,
                                          api_token=owner_api_token,
                                          operator="ALLOW", action="read",
                                          rtype="pc",
                                          rid='7a53482d35fe405ca469e88d041bb114',
                                          rtags={}).post()
    assert_response_bad_request(response)
    print "Success!!!!"


def test_0106_append_rule_to_policy_with_wrong_rid(cache, pretty_print,
                              mist_core, owner_api_token):
    print "\n>>> Posting /policy_rules to append new rule to policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')
    response = mist_core.\
        append_rule_to_policy(org_id=org_id, team_id=team_id,
                                api_token=owner_api_token,
                                operator="ALLOW", action="read",
                                rtype="key",
                                rid='7a53482d35fe405ca469e88d041bb114'[:-2],
                                rtags={}).post()
    assert_response_not_found(response)
    print "Success!!!!"


def test_0111_insert_rule_to_policy_with_wrong_index_id(cache, pretty_print,
                              mist_core, owner_api_token):
    print "\n>>> Posting /policy_rules to append new rule to policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')
    response = mist_core.insert_rule_to_policy(org_id=org_id, team_id=team_id,
                                          api_token=owner_api_token,
                                          operator="ALLOW", action="read",
                                          rtype="key",
                                          rid='7a53482d35fe405ca469e88d041bb114',
                                          rtags={}, index_id=10).post()
    assert_response_bad_request(response)
    print "Success!!!!"


def test_012_edit_rule_to_policy_with_wrong_index_id(cache, pretty_print,
                              mist_core, owner_api_token):
    print "\n>>> Posting /policy_rules to append new rule to policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')
    response = mist_core.edit_rule_to_policy(org_id=org_id, team_id=team_id,
                                          api_token=owner_api_token,
                                          operator="ALLOW", action="read",
                                          rtype="key",
                                          rid='7a53482d35fe405ca469e88d041bb114',
                                          rtags={}, index_id=10).put()
    assert_response_bad_request(response)
    print "Success!!!!"


def test_014_delete_rule_from_policy(cache, pretty_print, mist_core,
                                     owner_api_token):
    print "\n>>> Deleting /policy_rules to append new rule to policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')
    response = mist_core.delete_rule_from_policy(org_id=org_id, team_id=team_id,
                                                 api_token=owner_api_token,
                                                 index_id=10).delete()
    assert_response_bad_request(response)
    print "Success!!!!"


def test_015_edit_team_policy(cache, pretty_print, mist_core, owner_api_token):
    print "\n>>> Puting /team_policy to save whole policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')

    policy=[]

    response = mist_core.edit_team_policy(org_id=org_id, team_id=team_id,
                                                 api_token=owner_api_token,
                                          policy=policy).put()
    assert_response_bad_request(response)
    print "Success!!!!"


def test_0151_edit_team_policy_without_policy_operator(cache, pretty_print,
                                                       mist_core,
                                                       owner_api_token):
    print "\n>>> Puting /team_policy to save whole policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')

    policy={"operator":"","rules":[
    {"operator":"ALLOW","action":"add","rtype":"cloud",
     "rid":"17a6e656597d44cdb690d5a7e31ec88c","rtags":{}},
    {"operator":"ALLOW","action":"read","rtype":"cloud",
     "rid":"17a6e656597d44cdb690d5a7e31ec88c","rtags":{}}
    ]}

    response = mist_core.edit_team_policy(org_id=org_id, team_id=team_id,
                                                 api_token=owner_api_token,
                                          policy=policy).put()
    assert_response_bad_request(response)
    print "Success!!!!"


def test_0152_edit_team_policy_with_wrong_action(cache, pretty_print,
                                                 mist_core, owner_api_token):
    print "\n>>> Puting /team_policy to save whole policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')

    policy={"operator":"","rules":[
    {"operator":"ALLOW","action":"bla","rtype":"cloud",
     "rid":"17a6e656597d44cdb690d5a7e31ec88c","rtags":{}}
    ]}

    response = mist_core.edit_team_policy(org_id=org_id, team_id=team_id,
                                                 api_token=owner_api_token,
                                          policy=policy).put()
    assert_response_bad_request(response)
    print "Success!!!!"


def test_0153_edit_team_policy_with_wrong_rtype(cache, pretty_print, mist_core,
                                                owner_api_token):
    print "\n>>> Puting /team_policy to save whole policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')

    policy={"operator":"","rules":[
    {"operator":"ALLOW","action":"read","rtype":"bla",
     "rid":"17a6e656597d44cdb690d5a7e31ec88c","rtags":{}}
    ]}

    response = mist_core.edit_team_policy(org_id=org_id, team_id=team_id,
                                                 api_token=owner_api_token,
                                          policy=policy).put()
    assert_response_bad_request(response)
    print "Success!!!!"


def test_0154_edit_team_policy_with_wrong_rid(cache, pretty_print, mist_core,
                                              owner_api_token):
    print "\n>>> Puting /team_policy to save whole policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')

    policy={"operator":"ALLOW","rules":[
    {"operator":"ALLOW","action":"read","rtype":"bla",
     "rid":"17a6e656597d44cdb690d5a7e31ec88c"[:-2],"rtags":{}}
    ]}

    response = mist_core.edit_team_policy(org_id=org_id, team_id=team_id,
                                                 api_token=owner_api_token,
                                          policy=policy).put()
    assert_response_bad_request(response)
    print "Success!!!!"


def test_0155_edit_team_policy_without_rid_rtags(cache, pretty_print,
                                                 mist_core, owner_api_token):
    print "\n>>> Puting /team_policy to save whole policy"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')

    policy={"operator":"ALLOW","rules":[
    {"operator":"ALLOW","action":"read","rtype":"bla",
     "rid":"","rtags":{}}
    ]}

    response = mist_core.edit_team_policy(org_id=org_id, team_id=team_id,
                                                 api_token=owner_api_token,
                                          policy=policy).put()
    assert_response_bad_request(response)
    print "Success!!!!"


def test_016_delete_team_with_wrong_team_id(cache, pretty_print, mist_core,
                      owner_api_token):
    print "\n>>> DELETEing /team to delete an org's team"
    org_id = cache.get('org/org_id','')
    team_id = cache.get('team/team_id','')[:-2]
    response = mist_core.delete_team(org_id=org_id, team_id=team_id,
                                     api_token=owner_api_token).delete()
    assert_response_not_found(response)
    print "Success!!!!"

#
# def test_012_patch_rule_to_policy(cache, pretty_print,
#                               mist_core, owner_api_token):
#     print "\n>>> Posting /policy_rules to append new rule to policy"
#     org_id = cache.get('org/org_id','')
#     team_id = cache.get('team/team_id','')
#     response = mist_core.insert_rule_to_policy(org_id=org_id, team_id=team_id,
#                                           api_token=owner_api_token,
#                                           operator="ALLOW", action="read",
#                                           rtype="Machine", rid="",
#                                           rtag={}, index_id=0, pos=1).patch()
#     assert_response_ok(response)
#     print "Success!!!!"
