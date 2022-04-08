from misttests.config import inject_vault_credentials
from misttests.integration.api.helpers import uniquify_string


def setup(api_token):
    cloud_name = uniquify_string('test-cloud')
    add_cloud_request_body = {
        'credentials': {
            'email': None,
            'privateKey': None,
            'projectId': None
        },
        'name': cloud_name,
        'provider': 'google'
    }
    inject_vault_credentials(add_cloud_request_body)
    test_args = {
        'add_cloud': {'request_body': add_cloud_request_body},
        'edit_cloud': {
            'request_body': {'name': cloud_name},
            'cloud': cloud_name
        },
        'get_cloud': {
            'cloud': cloud_name,
        },
        'remove_cloud': {'cloud': cloud_name}
    }
    return test_args


def teardown(api_token, setup_data):
    pass
