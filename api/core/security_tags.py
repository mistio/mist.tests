from tests.api.helpers import *
from tests.api.utils import *

from tests.helpers.setup import setup_team
from tests.helpers.setup import setup_user_if_not_exists

from tests import config


# def test_create_token_for_member(pretty_print, mist_core, cache,
#                                  member1_email, password1):
#     print "\n>>> GETing / to get personal token of team member\n"
#
#     response = mist_core.create_token(email=member1_email,
#                                       password=password1).post()
#     assert_response_ok(response)
#     api_token_id = response.json().get('id', None)
#     api_token = response.json().get('token', None)
#
#     cache.set('rbac/member1_api_token_id', api_token_id)
#     cache.set('rbac/member1_api_token', api_token)
#
#     print "Success!!!!"


def test_tag_cloud(pretty_print, mist_core, cache, owner_api_token):
    setup_user_if_not_exists(config.MEMBER1_EMAIL, config.MEMBER1_PASSWORD)
    cache.set('rbac/member1_team_id', setup_team(config.ORG_NAME, 'cloud_tag_tests', [config.MEMBER1_EMAIL]))

    print '\n>>> POSTing  policy rules to team (ALLOW read cloud, ' \
          'ALLOW read machine, ALLOW edit_tags machine)\n'

    response = mist_core.show_user_org(api_token=owner_api_token).get()
    assert_response_ok(response)
    rjson = json.loads(response.content)
    assert_is_not_none(rjson.get('id'),
                       "Did not get an id back in the response")

    cache.set('rbac/org_id', rjson.get('id'))

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

    print'\n>>> GETing list of clouds\n' % config.API_TESTING_CLOUD

    clouds = mist_core.list_clouds(api_token=owner_api_token).get()
    assert_response_ok(clouds)
    clouds = json.loads(clouds.content)
    assert_list_not_empty(clouds)
    test_cloud = None
    for cloud in clouds:
        if cloud['title'] == config.API_TESTING_CLOUD:
            test_cloud = cloud
            break
    assert_is_not_none(test_cloud)
    cloud_id = test_cloud['id']

    print'\n>>> GETing list of machines\n' % config.API_TESTING_MACHINE_NAME

    machines = mist_core.list_machines(cloud_id=cloud_id,
                                       api_token=owner_api_token).get()
    machines = json.loads(machines.content)
    assert_list_not_empty(machines)
    test_machine = None
    for machine in machines:
        if machine['name'] == config.API_TESTING_MACHINE_NAME:
            test_machine = machine
            break
    assert_is_not_none(test_machine)
    machine_id = test_machine['id']

    cache.set('rbac/cloud_id', cloud_id)
    cache.set('rbac/machine_id', machine_id)

    tags = {'security': 'test'}

    print'\n>>> Tagging %s machine with the security tag: `security=test`\n' % config.API_TESTING_MACHINE_NAME

    response = mist_core.set_machine_tags(api_token=owner_api_token,
                                          cloud_id=cloud_id,
                                          machine_id=machine_id,
                                          **tags).post()
    assert_response_ok(response)
    print 'Success!!!!'


# def test_modify_security_tags(pretty_print, mist_core, cache,
#                               member1_api_token):
#     print '\n>>> Regular team member attempting to modify security tags\n'
#
#     cloud_id = cache.get('rbac/cloud_id', '')
#     machine_id = cache.get('rbac/machine_id', '')
#
#     # The {'security': 'test'} tag added by the owner in the previous method
#     # exists also as part of team policies, thus it should be present in
#     # every set_machine_tags request by the team member in order for the
#     # action to be allowed. Also, the {'sec': 'tes'} tag is a security tag,
#     # but it is not present on any resource, therefore no team member is
#     # allowed to add it.
#
#     tags = [
#         {'sec': 'test'},
#         {'security': 't'},
#         {'security': 'test', 'sec': 'tes'}
#     ]
#     for tag in tags:
#         response = mist_core.set_machine_tags(api_token=member1_api_token,
#                                               cloud_id=cloud_id,
#                                               machine_id=machine_id,
#                                               **tag).post()
#         assert_response_forbidden(response)
#
#     tags = {'security': 'test', 'something': 'else'}
#     response = mist_core.set_machine_tags(api_token=member1_api_token,
#                                           cloud_id=cloud_id,
#                                           machine_id=machine_id,
#                                           **tags).post()
#     assert_response_ok(response)
#
#     tags = {'something': 'else'}
#     response = mist_core.set_machine_tags(api_token=member1_api_token,
#                                           cloud_id=cloud_id,
#                                           machine_id=machine_id,
#                                           **tags).post()
#     assert_response_forbidden(response)
#
#     tags = {'security': 'test'}
#     response = mist_core.set_machine_tags(api_token=member1_api_token,
#                                           cloud_id=cloud_id,
#                                           machine_id=machine_id,
#                                           **tags).post()
#     assert_response_ok(response)
#
#     print 'Success!!!!'
