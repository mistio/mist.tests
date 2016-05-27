from tests.api.helpers import *
from tests.api.utils import *


# This test requires that the organization `MyOrg` has been created by the user
# Also, make sure that a single docker cloud exists in the organization context
# in order to avoid cross-context conflict

def test_show_user_org_for_owner(pretty_print, mist_core, cache,
                                 org_name, owner_api_token):
    print "\n>>> GETing /orgs to get a list of all user orgs and the api" \
          "token with access to that org\n"
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

    print "Success!!!!"


def test_create_personal_tokens_for_member(pretty_print, mist_core,
                                           cache, member1_email, member1_password):
    print "\n>>> GETing / to get personal token of team member\n"

    response = mist_core.create_token(email=member1_email,
                                      password=member1_password).post()
    assert_response_ok(response)
    api_token_id = response.json().get('id', None)
    api_token = response.json().get('token', None)

    cache.set('rbac/member1_api_token_id', api_token_id)
    cache.set('rbac/member1_api_token', api_token)

    print "Success!!!!"


def test_invite_member_to_team(pretty_print, mist_core, cache,
                               owner_api_token, org_name, member1_email):
    print "\n>>> POSTing / to invite member1 to a team\n"
    org_id = cache.get('rbac/org_id', '')
    member1_api_token = cache.get('rbac/member1_api_token', '')

    # get a random new team name
    response = mist_core.list_teams(org_id=org_id,
                                    api_token=owner_api_token).get()
    assert_response_ok(response)
    cache.set('rbac/member1_team_name',
              get_random_team_name(json.loads(response.content)))

    # create an new team for member1
    response = mist_core.add_team(name=cache.get('rbac/member1_team_name', ''),
                                  description='', org_id=org_id,
                                  api_token=owner_api_token).post()
    assert_response_ok(response)
    rjson = json.loads(response.content)
    assert_is_not_none(rjson.get('id'),
                       "Did not get an id back in the response")
    cache.set('rbac/member1_team_id', rjson['id'])

    # add member1 to new team
    response = mist_core.invite_member_to_team(org_id=org_id,
                                               team_id=cache.get('rbac/member1_team_id', ''),
                                               email=member1_email,
                                               api_token=owner_api_token).post()
    assert_response_ok(response)
    rjson = json.loads(response.content)
    assert_is_not_none(rjson.get('id'),
                       "Did not get an id back in the response")
    cache.set('rbac/member1_id', rjson.get('id'))

    pending = rjson['pending']
    if pending is True:
        # this is for member that is already a user in our db
        # but not member of the org
        response = mist_core.show_user_invitations(api_token=member1_api_token).get()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        token = rjson[0]['token']

        response = mist_core.confirm_invitation(api_token=member1_api_token,
                                                invitoken=token).get()

    print "Success!!!!"


def test_append_rules_to_policy(pretty_print, mist_core, cache,
                                owner_api_token):
    print '\n>>> POSTing  policy rules to team (ALLOW read cloud, ' \
          'ALLOW read machine, ALLOW edit_tags machine)\n'
    org_id = cache.get('rbac/org_id', '')
    member1_team_id = cache.get('rbac/member1_team_id', '')

    allow_cloud_read_policy = {
        'operator': 'ALLOW',
        'action': 'read',
        'rtype': 'cloud',
        'rid': '',
        'rtags': {}
    }
    allow_machine_read_policy = {
        'operator': 'ALLOW',
        'action': 'read',
        'rtype': 'machine',
        'rid': '',
        'rtags': {}
    }
    allow_machine_edit_tags_1 = {
        'operator': 'ALLOW',
        'action': 'edit_tags',
        'rtype': 'machine',
        'rid': '',
        'rtags': {'security': 'test'}
    }
    allow_machine_edit_tags_2 = {
        'operator': 'ALLOW',
        'action': 'edit_tags',
        'rtype': 'machine',
        'rid': '',
        'rtags': {'sec': 'tes'}
    }

    response = mist_core.append_rule_to_policy(api_token=owner_api_token,
                                               org_id=org_id,
                                               team_id=member1_team_id,
                                               **allow_cloud_read_policy).post()
    assert_response_ok(response)
    response = mist_core.append_rule_to_policy(api_token=owner_api_token,
                                               org_id=org_id,
                                               team_id=member1_team_id,
                                               **allow_machine_read_policy).post()
    assert_response_ok(response)
    response = mist_core.append_rule_to_policy(api_token=owner_api_token,
                                               org_id=org_id,
                                               team_id=member1_team_id,
                                               **allow_machine_edit_tags_1).post()
    assert_response_ok(response)
    response = mist_core.append_rule_to_policy(api_token=owner_api_token,
                                               org_id=org_id,
                                               team_id=member1_team_id,
                                               **allow_machine_edit_tags_2).post()
    assert_response_ok(response)


def test_tag_docker_dev(pretty_print, mist_core, cache, owner_api_token):
    print'\n>>> Tagging docker-dev with the security tag: `security=test`\n'

    tags = {'security': 'test'}

    clouds = mist_core.list_clouds(api_token=owner_api_token).get()
    assert_response_ok(clouds)
    clouds = json.loads(clouds.content)
    assert_list_not_empty(clouds)
    test_cloud = None
    for cloud in clouds:
        if cloud['provider'] == 'docker':
            test_cloud = cloud
            break
    assert_is_not_none(test_cloud)
    cloud_id = test_cloud['id']

    machines = mist_core.list_machines(cloud_id=cloud_id,
                                       api_token=owner_api_token).get()
    machines = json.loads(machines.content)
    assert_list_not_empty(machines)
    test_machine = None
    for machine in machines:
        if machine['name'] == 'mistio-mist-core':
            test_machine = machine
            break
    assert_is_not_none(test_machine)
    machine_id = test_machine['id']

    cache.set('rbac/cloud_id', cloud_id)
    cache.set('rbac/machine_id', machine_id)

    response = mist_core.set_machine_tags(api_token=owner_api_token,
                                          cloud_id=cloud_id,
                                          machine_id=machine_id,
                                          **tags).post()
    assert_response_ok(response)
    print 'Success!!!!'


def test_modify_security_tags(pretty_print, mist_core, cache,
                              member1_api_token):
    print '\n>>> Regular team member attempting to modify security tags\n'

    cloud_id = cache.get('rbac/cloud_id', '')
    machine_id = cache.get('rbac/machine_id', '')

    # The {'security': 'test'} tag added by the owner in the previous method
    # exists also as part of team policies, thus it should be present in
    # every set_machine_tags request by the team member in order for the
    # action to be allowed

    tags = [
        {'sec': 'test'},
        {'security': 't'},
        {'security': 'test', 'sec': 'tes'}
    ]
    for tag in tags:
        response = mist_core.set_machine_tags(api_token=member1_api_token,
                                              cloud_id=cloud_id,
                                              machine_id=machine_id,
                                              **tag).post()
        assert_response_unauthorized(response)

    tags = {'security': 'test', 'something': 'else'}
    response = mist_core.set_machine_tags(api_token=member1_api_token,
                                          cloud_id=cloud_id,
                                          machine_id=machine_id,
                                          **tags).post()
    assert_response_ok(response)

    tags = {'something': 'else'}
    response = mist_core.set_machine_tags(api_token=member1_api_token,
                                          cloud_id=cloud_id,
                                          machine_id=machine_id,
                                          **tags).post()
    assert_response_unauthorized(response)

    tags = {'security': 'test'}
    response = mist_core.set_machine_tags(api_token=member1_api_token,
                                          cloud_id=cloud_id,
                                          machine_id=machine_id,
                                          **tags).post()
    assert_response_ok(response)

    print 'Success!!!!'
