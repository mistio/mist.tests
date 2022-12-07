from misttests.config import MIST_URL
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.mistrequests import MistRequests


def setup(api_token):
    orgs_uri = MIST_URL + '/api/v2/orgs'
    request = MistRequests(api_token=api_token, uri=orgs_uri)
    response = request.get()
    assert_response_ok(response)
    org_id = response.json()['data'][0]['id']
    org_name = response.json()['data'][0]['name']
    members_uri = orgs_uri + f'/{org_id}/members'
    request = MistRequests(api_token=api_token, uri=members_uri)
    response = request.get()
    assert_response_ok(response)
    member_id = response.json()['data'][0]['id']
    setup_data = {
        'get_member': {
            'org': org_id,
            'org_name': org_name,
            'member': member_id
        },
        'get_org': {'org': org_id, 'org_name': org_name,},
        'list_org_members': {'org': org_id, 'org_name': org_name,},
        'list_org_teams': {'org': org_id, 'org_name': org_name,},
        'update_org': { 'org_name': org_name}
    }
    return setup_data


def teardown(api_token, setup_data):
    pass
