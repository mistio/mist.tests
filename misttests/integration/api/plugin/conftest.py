from misttests.integration.api.main.conftest import *
from misttests import config


@pytest.fixture
def org_name():
    return config.ORG_NAME


@pytest.fixture
def template_github():
    return 'https://github.com/mistio/simple-resource-provisioning-blueprint'


@pytest.fixture(scope='module')
def valid_api_token(request):
    return common_valid_api_token(request, email=email(), password=password1())


@pytest.fixture(scope='module')
def member2_api_token(request):
    _mist_api_v1 = mist_api_v1()
    email = member2_email()
    password = member2_password()
    personal_api_token = common_valid_api_token(request,
                                                email=email,
                                                password=password)
    _org_name = org_name()
    response = _mist_api_v1.list_orgs(api_token=personal_api_token).get()
    assert_response_ok(response)
    org_id = None
    for org in response.json():
        if _org_name == org['name']:
            org_id = org['id']
            break
    assert_is_not_none(org_id)

    return common_valid_api_token(request,
                                  email=email,
                                  password=password,
                                  org_id=org_id)
