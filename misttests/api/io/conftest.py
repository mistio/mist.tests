import pytest

from misttests import config
from misttests.config import safe_get_var
from misttests.api.helpers import *
from misttests.helpers.setup import setup_user_if_not_exists

from io import MistIoApi
from misttests.api.core.core import MistCoreApi


@pytest.fixture
def pretty_print(request):
    print "\n============================================================"
    print " ".join([word.capitalize() for word in request.function.__name__.split('_')])

    def fin():
        print "\n============================================================"

    request.addfinalizer(fin)
    return 'bla'


@pytest.fixture
def email():
    return config.EMAIL


@pytest.fixture
def password1():
    return config.PASSWORD1


@pytest.fixture
def password2():
    return config.PASSWORD2


@pytest.fixture
def mist_io():
    return MistIoApi(config.MIST_URL + '/api/v1')


@pytest.fixture
def mist_core():
    return MistCoreApi(config.MIST_URL)


@pytest.fixture
def owner_email():
    BASE_EMAIL = config.BASE_EMAIL
    return "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1, 200000))


@pytest.fixture
def owner_password():
    return config.OWNER_PASSWORD


@pytest.fixture
def initialize_members():
    BASE_EMAIL = config.BASE_EMAIL
    config.MEMBER1_EMAIL = "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1, 200000))
    email = config.MEMBER1_EMAIL
    password = member1_password()
    setup_user_if_not_exists(email, password, 'Member1')

@pytest.fixture()
def member1_email():
    return config.MEMBER1_EMAIL


@pytest.fixture
def member1_password():
    return config.MEMBER1_PASSWORD


@pytest.fixture
def member2_email():
    BASE_EMAIL = config.BASE_EMAIL
    return "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1, 200000))


@pytest.fixture
def member2_password():
    return config.MEMBER2_PASSWORD


@pytest.fixture
def api_test_machine_name():
    return config.API_TESTING_MACHINE_NAME


@pytest.fixture
def private_key():
    return safe_get_var('keys/api_testing_machine_private_key', 'priv_key', config.API_TESTING_MACHINE_PRIVATE_KEY)


@pytest.fixture
def public_key():
    return config.API_TESTING_MACHINE_PUBLIC_KEY


@pytest.fixture()
def schedules_cleanup(mist_core, owner_api_token, cache):
    yield
    response = mist_core.list_schedules(api_token=owner_api_token).get()
    assert_response_ok(response)
    for schedule in response.json():
        mist_core.delete_schedule(api_token=owner_api_token, schedule_id=schedule['id']).delete()
    response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()
    for machine in response.json():
        if 'api_test_machine' in machine['name']:
            mist_core.machine_action(cloud_id=cache.get('cloud_id', ''),
                                     api_token=owner_api_token,
                                     machine_id=machine['machine_id'],
                                     action='destroy').post()


@pytest.fixture(scope='module', params=['name', 'location', 'exec_type'])
def script_missing_param(request):
    if request.param == 'name':
        return {'name': '', 'location': 'inline', 'exec_type': 'ansible'}
    elif request.param == 'location':
        return {'name': 'dummy', 'location': '', 'exec_type': 'ansible'}
    else:
        return {'name': 'dummy', 'location': 'inline', 'exec_type': ''}


@pytest.fixture(scope='module', params=['location', 'exec_type'])
def script_wrong_param(request):
    if request.param == 'location':
        return {'name': 'dummy', 'location': 'dummy', 'exec_type': 'ansible'}
    else:
        return {'name': 'dummy', 'location': 'inline', 'exec_type': 'dummy'}


@pytest.fixture(scope='module', params=[bash_script_no_shebang])
def script_wrong_script(request):
        return bash_script_no_shebang


@pytest.fixture(scope='module')
def base_exec_inline_script(request):
    return {'name': 'dummy', 'location': 'inline', 'exec_type': 'executable'}


def common_valid_api_token(request, email, password, org_id=None):
    _mist_core = mist_core()
    response = _mist_core.create_token(email=email,
                                       password=password,
                                       org_id=org_id).post()
    assert_response_ok(response)
    assert_is_not_none(response.json().get('token'))
    assert_is_not_none(response.json().get('id'))
    api_token = response.json().get('token', None)
    return api_token


@pytest.fixture(scope='module')
def owner_api_token(request):
    _mist_core = mist_core()
    email = owner_email()
    password = owner_password()
    setup_user_if_not_exists(email, password, 'Owner')
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
