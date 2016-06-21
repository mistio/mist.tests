from tests.api.helpers import *
from tests.api.utils import *

from tests.helpers.setup import setup_team

from tests import config


def test_tag_machine(pretty_print, mist_core, cache, owner_api_token):
    print "\n>>> Checking the functionality of tag validation methods\n"
    # actions will be performed in org context in order to also verify policy
    # rules' validation
    response = mist_core.show_user_org(api_token=owner_api_token).get()
    assert_response_ok(response)
    rjson = json.loads(response.content)
    assert_is_not_none(rjson.get('id'),
                       "Did not get an id back in the response")
    cache.set('rbac/org_id', rjson.get('id'))
    org_id = cache.get('rbac/org_id', '')

    print "\n>>> GETing list of clouds\n"
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

    print'\n>>> GETing list of machines\n'
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

    print "\n>>> POSTing machine tags to verify Tag model's validation\n"
    tags = {
        'test': 'pass',
        'test_2': 'pass_2',
        '-test-': '-'
    }
    response = mist_core.set_machine_tags(api_token=owner_api_token,
                                          cloud_id=cloud_id,
                                          machine_id=machine_id,
                                          **tags).post()
    assert_response_ok(response)

    tags = [
        {'test': '!'},
        {'(&)': 'fail'},
        {'?': '/#'}
    ]
    for tag in tags:
        response = mist_core.set_machine_tags(api_token=owner_api_token,
                                              cloud_id=cloud_id,
                                              machine_id=machine_id,
                                              **tag).post()
        assert_response_bad_request(response)

    print "\n>>> POSTing team policies to verify policy rules' validation\n"
    # creating new team in order to test policy rules' tag validation
    cache.set('rbac/team_id', setup_team(config.ORG_NAME, 'validate_tags'))
    team_id = cache.get('rbac/team_id', '')
    team_policies_pass = [
         {
             'operator': 'ALLOW',
             'action': 'read',
             'rtype': 'cloud',
             'rid': '',
             'rtags': {'test': 'pass'}
             },
         {
             'operator': 'ALLOW',
             'action': 'read',
             'rtype': 'cloud',
             'rid': '',
             'rtags': {'test_2': 'pass_2'}
             },
         {
             'operator': 'ALLOW',
             'action': 'read',
             'rtype': 'cloud',
             'rid': '',
             'rtags': {'test_3': ''}
             },
         {
             'operator': 'ALLOW',
             'action': 'read',
             'rtype': 'cloud',
             'rid': '',
             'rtags': {'-test-': '-'}
             },
    ]
    team_policies_fail = [
         {
             'operator': 'ALLOW',
             'action': 'read',
             'rtype': 'cloud',
             'rid': '',
             'rtags': {'test': '!'}
             },
         {
             'operator': 'ALLOW',
             'action': 'read',
             'rtype': 'cloud',
             'rid': '',
             'rtags': {'*': 'test'}
             },
         {
             'operator': 'ALLOW',
             'action': 'read',
             'rtype': 'cloud',
             'rid': '',
             'rtags': {'': 'something'}
             },
         {
             'operator': 'ALLOW',
             'action': 'read',
             'rtype': 'cloud',
             'rid': '',
             'rtags': {'-test-': 'p-$'}
             },
    ]

    for policy in team_policies_pass:
        response = mist_core.append_rule_to_policy(api_token=owner_api_token,
                                                   org_id=org_id,
                                                   team_id=team_id,
                                                   **policy).post()
        assert_response_ok(response)
    for policy in team_policies_fail:
        response = mist_core.append_rule_to_policy(api_token=owner_api_token,
                                                   org_id=org_id,
                                                   team_id=team_id,
                                                   **policy).post()
        assert_response_bad_request(response)
