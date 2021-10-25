from misttests.config import MIST_URL
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.mistrequests import MistRequests


USER_EMAIL = 'example-member@something.com'
ORG_NAME = 'example-org'
TEAM_NAME = 'example-team'


def setup(api_token):
    orgs_uri = MIST_URL + '/api/v2/orgs'
    request = MistRequests(api_token=api_token, uri=orgs_uri)
    response = request.get()
    assert_response_ok(response)
    org_id = response.json()['data'][0]['id']
    members_uri = orgs_uri + f'/{org_id}/members'
    request = MistRequests(api_token=api_token, uri=members_uri)
    response = request.get()
    assert_response_ok(response)
    member_id = response.json()['data'][0]['id']
    return {
        'org': org_id,
        'member': member_id
    }


def teardown(api_token):
    pass
