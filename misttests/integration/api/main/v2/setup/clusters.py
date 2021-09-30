from misttests import config
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.mistrequests import MistRequests


def setup(api_token):
    add_cloud_request = {
        "name": "example-cloud",
        "provider": "google",
        "credentials": {
            "projectId": "projectId",
            "privateKey": "privateKey",
            "email": "email"
        },
        "features": {
            "container": True,
        },
    }
    config.inject_vault_credentials(add_cloud_request)
    uri = config.MIST_URL + '/api/v2/clouds'
    request = MistRequests(
        api_token=api_token, uri=uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)


def teardown(api_token):
    uri = config.MIST_URL + '/api/v2/clouds/{cloud}'.format(
        cloud="example-cloud")
    request = MistRequests(
        api_token=api_token, uri=uri)
    response = request.delete()
    assert_response_ok(response)
