from misttests.integration.api.helpers import uniquify_string


def setup(api_token):
    cloud_name = uniquify_string('test-cloud')
    return {'cloud': cloud_name}


def teardown(api_token, setup_data):
    pass
