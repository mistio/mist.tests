from .core import MistCoreApi

from misttests.api.helpers import *
from misttests.api.io.conftest import *
from misttests.helpers.setup import setup_user_if_not_exists

from misttests.api.helpers import get_keys_with_id


@pytest.fixture
def mist_core():
    return MistCoreApi(config.MIST_URL)


@pytest.fixture
def fresh_api_token():
    print "\n>>> Producing new api token!"
    from mist.core.auth.models import get_secure_rand_token
    return get_secure_rand_token()


@pytest.fixture(scope='session')
def user():
    from mist.io.users.models import User
    _email = email()
    print "\n>>> Getting user with email %s from db" % _email
    return User.objects.get(email=_email)


@pytest.fixture
def user_with_api_token(request):
    _user = user()
    _fresh_api_token = fresh_api_token()
    print "\n>>> Adding new api token to user in the db"
    _user.mist_api_token = _fresh_api_token
    _user.save()

    def fin():
        print "\n>>> Cleaning up user's token"
        _user.mist_api_token = ""
        _user.save()
    request.addfinalizer(fin)
    return _user


@pytest.fixture
def user_with_short_api_token(request):
    _user_with_api_token = user_with_api_token(request)
    print "\n>>> Shortening user's api token"
    _user_with_api_token.mist_api_token = _user_with_api_token.mist_api_token[:-1]
    _user_with_api_token.save()
    return _user_with_api_token


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
  #  import ipdb;ipdb.set_trace()
    email = owner_email()
    password = owner_password()
    setup_user_if_not_exists(email, password)
    _mist_core.login(email, password)
    personal_api_token = common_valid_api_token(request,
                                                email=email,
                                                password=password)
    #_org_name = org_name()
    #setup_org_if_not_exists(_org_name, email)
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


@pytest.fixture(scope='module')
def random_ssh_key(request):
    _mist_core = mist_core()
    _valid_api_token = valid_api_token(request)
    response = _mist_core.list_keys(api_token=_valid_api_token).get()
    assert_response_ok(response)
    keys_list = json.loads(response.content)
    if len(keys_list) == 0:
        new_ssh_key_id = get_random_key_id([])
        response = _mist_core.add_key(id=new_ssh_key_id,
                                      private=private_key,
                                      api_token=_valid_api_token).put()
        assert_response_ok(response)
        response = _mist_core.list_keys(api_token=_valid_api_token).get()
        assert_response_ok(response)
        keys = get_keys_with_id(new_ssh_key_id,
                                json.loads(response.content))
        assert_list_not_empty(keys, msg="Key was added through the api"
                                        " but is not visible in the "
                                        "list of keys")

        def fin():
            _response = _mist_core.delete_key(api_token=_valid_api_token,
                                              key_id=keys[0]['key_id']).delete()
            assert_response_ok(_response)

        request.addfinalizer(fin)
        return keys[0]

    return random.choice(keys_list)


@pytest.fixture(scope='module')
def random_bash_script(request):
    _mist_core = mist_core()
    _valid_api_token = valid_api_token(request)
    response = _mist_core.list_scripts(api_token=_valid_api_token).get()
    assert_response_ok(response)
    script_list = json.loads(response.content)
    if len(script_list) == 0:
        new_script_name = get_random_script_name([])
        response = _mist_core.add_script(api_token=_valid_api_token,
                                         name=new_script_name,
                                         location_type='inline',
                                         exec_type='executable',
                                         script=bash_script).post()

        assert_response_ok(response)
        response = _mist_core.list_scripts(api_token=_valid_api_token).get()
        assert_response_ok(response)
        script = get_scripts_with_name(
            new_script_name,
            json.loads(response.content))
        assert_list_not_empty(script, "Script was added but is not visible in"
                                      " the list of scripts")

        def fin():
            _response = _mist_core.delete_script(api_token=_valid_api_token,
                                                 script_id=script[0][
                                                     'script_id']).delete()
            assert_response_ok(_response)

        request.addfinalizer(fin)
        return script[0]

    return random.choice(script_list)


@pytest.fixture(scope='module')
def machines_per_cloud(request):
    _mist_core = mist_core()
    _valid_api_token = valid_api_token(request)
    response = _mist_core.list_clouds(api_token=_valid_api_token).get()
    assert_response_ok(response)
    clouds = json.loads(response.content)
    assert_list_not_empty(clouds)
    cloud_id = None
    for cloud in clouds:
        if cloud['title'] == 'EC2':
            cloud_id = cloud['id']
            break
    assert_is_not_none(cloud_id)
    response = _mist_core.list_machines(cloud_id=cloud_id,
                                        api_token=_valid_api_token).get()
    assert_response_ok(response)
    machines = json.loads(response.content)
    assert_list_not_empty(machines)
    machines_per_cloud = []
    machine_num = 2
    while len(machines) > 0 and machine_num != 0:
        machine = machines.pop()
        machines_per_cloud.append([cloud_id, machine['id']])
        machine_num -= 1
    print "machines per cloud to be used is: %s" % machines_per_cloud
    return machines_per_cloud


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
