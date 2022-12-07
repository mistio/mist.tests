import pytest

from misttests import config
from misttests.config import safe_get_var
from misttests.integration.api.helpers import *
from misttests.helpers.setup import setup_user_if_not_exists

from .io import MistIoApi
from misttests.integration.api.main.io import MistIoApi


def mist_api_v1():
    return MistIoApi(config.MIST_URL)


def owner_email():
    BASE_EMAIL = config.BASE_EMAIL
    return "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1, 200000))


def owner_password():
    return config.OWNER_PASSWORD


def member1_email():
    return config.MEMBER1_EMAIL


def member1_password():
    return config.MEMBER1_PASSWORD


@pytest.fixture
def pretty_print(request):
    print("\n============================================================")
    print((" ".join([word.capitalize() for word in request.function.__name__.split('_')])))

    def fin():
        print("\n============================================================")

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


@pytest.fixture(name='mist_api_v1')
def mist_api_v1_fixture():
    return mist_api_v1()


@pytest.fixture(name='owner_email')
def owner_email_fixture():
    return owner_email()


@pytest.fixture(name='owner_password')
def owner_password_fixture():
    return owner_password()


@pytest.fixture
def initialize_members():
    BASE_EMAIL = config.BASE_EMAIL
    config.MEMBER1_EMAIL = "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1, 200000))
    email = config.MEMBER1_EMAIL
    password = member1_password()
    setup_user_if_not_exists(email, password, 'Member1')


@pytest.fixture(name='member1_email')
def member1_email_fixture():
    return member1_email()


@pytest.fixture(name='member1_password')
def member1_password_fixture():
    return member1_password()


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
    return safe_get_var('keys/api_testing_machine_private_key', 'priv_key', config.TESTING_PRIVATE_KEY)


@pytest.fixture()
def schedules_cleanup(mist_api_v1, owner_api_token, cache):
    yield
    response = mist_api_v1.list_schedules(api_token=owner_api_token).get()
    assert_response_ok(response)
    for schedule in response.json():
        mist_api_v1.delete_schedule(api_token=owner_api_token, schedule_id=schedule['id']).delete()
    response = mist_api_v1.list_machines(cloud_id=cache.get('docker_id', ''), api_token=owner_api_token).get()
    for machine in response.json():
        if 'api_test_machine' in machine['name']:
            mist_api_v1.machine_action(cloud_id=cache.get('docker_id', ''),
                                     api_token=owner_api_token,
                                     machine_id=machine['external_id'],
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
    _mist_api_v1 = mist_api_v1()
    response = _mist_api_v1.create_token(email=email,
                                       password=password,
                                       org_id=org_id).post()
    assert_response_ok(response)
    assert_is_not_none(response.json().get('token'))
    assert_is_not_none(response.json().get('id'))
    api_token = response.json().get('token', None)
    return api_token


@pytest.fixture(scope='module')
def owner_api_token(request):
    _mist_api_v1 = mist_api_v1()
    email = owner_email()
    password = owner_password()
    setup_user_if_not_exists(email, password, 'Owner')
    _mist_api_v1.login(email, password)
    personal_api_token = common_valid_api_token(request,
                                                email=email,
                                                password=password)
    response = _mist_api_v1.list_orgs(api_token=personal_api_token).get()
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
    _mist_api_v1 = mist_api_v1()
    email = member1_email()
    password = member1_password()
    personal_api_token = common_valid_api_token(request,
                                                email=email,
                                                password=password)
    response = _mist_api_v1.list_orgs(api_token=personal_api_token).get()
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
def network_valid_cidr(request):
    return '10.1.0.0/16'

@pytest.fixture(scope='module')
def availability_zone(request):
    return safe_get_var('clouds/aws', 'region', config.CREDENTIALS['EC2']['region']) + 'a'
