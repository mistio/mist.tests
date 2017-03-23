from .core import MistCoreApi

from misttests.api.io.conftest import *
from misttests.helpers.setup import setup_user_if_not_exists


@pytest.fixture
def mist_core():
    return MistCoreApi(config.MIST_URL)


@pytest.fixture(scope='session')
def user():
    from mist.io.users.models import User
    _email = email()
    print "\n>>> Getting user with email %s from db" % _email
    return User.objects.get(email=_email)


@pytest.fixture
def user_with_empty_password(request):
    _user = user()
    _password1 = password1()
    print "\n>>>  Removing password from user %s" % _user.email
    _user.password = ''
    _user.save()

    def fin():
        print "\n>>>  Reading password to user %s" % _user.email
        _user.set_password(_password1)
        _user.save()

    request.addfinalizer(fin)
    return _user


@pytest.fixture(scope='module')
def valid_api_token(request):
    return common_valid_api_token(request, email=email(), password=password1())


@pytest.fixture(scope='module')
def owner_api_token(request):
    _mist_core = mist_core()
    email = owner_email()
    password = owner_password()
    setup_user_if_not_exists(email, password)
    _mist_core.login(email, password)
    personal_api_token = common_valid_api_token(request,
                                                email=email,
                                                password=password)
    response = _mist_core.list_orgs(api_token=personal_api_token).get()
    assert_response_ok(response)
    org_id = None
    org = response.json()

    org_id = org[0]['id']
    assert_is_not_none(org_id)

    return common_valid_api_token(request,
                                  email=email,
                                  password=password,
                                  org_id=org_id)


@pytest.fixture(scope='module')
def member1_api_token(request):
    _mist_core = mist_core()
    email = member1_email()
    password = member1_password()
    personal_api_token = common_valid_api_token(request,
                                                email=email,
                                                password=password)

    _org_name = org_name()
    response = _mist_core.list_orgs(api_token=personal_api_token).get()
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


@pytest.fixture(scope='module')
def member2_api_token(request):
    _mist_core = mist_core()
    email = member2_email()
    password = member2_password()
    personal_api_token = common_valid_api_token(request,
                                                email=email,
                                                password=password)

    _org_name = org_name()
    response = _mist_core.list_orgs(api_token=personal_api_token).get()
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


def common_valid_api_token(request, email, password, org_id=None):
    _mist_core = mist_core()
    response = _mist_core.create_token(email=email,
                                       password=password,
                                       org_id=org_id).post()
    assert_response_ok(response)
    assert_is_not_none(response.json().get('token'))
    assert_is_not_none(response.json().get('id'))
    api_token = response.json().get('token', None)
    api_token_id = response.json().get('id', None)

    # def fin():
    #     _response = _mist_core.revoke_token(api_token=api_token,
    #                                         api_token_id=api_token_id).delete()
    #     assert_response_ok(_response)
    #
    # request.addfinalizer(fin)
    return api_token
