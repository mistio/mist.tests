import pytest
import random

from time import time

from datetime import date
from datetime import timedelta

from misttests import config
from misttests.api.helpers import *

from io import MistIoApi


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
def expires():
    return (date.fromtimestamp(time()) + timedelta(days=1, hours=1)).strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture
def expired():
    return (date.fromtimestamp(time()) + timedelta(days=-1, hours=1)).strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture
def owner_email():
    BASE_EMAIL = config.BASE_EMAIL
    return "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1, 200000))


@pytest.fixture
def owner_password():
    return config.OWNER_PASSWORD


@pytest.fixture
def member1_email():
    return config.MEMBER1_EMAIL


@pytest.fixture
def member1_password():
    return config.MEMBER1_PASSWORD


@pytest.fixture
def member2_email():
    return config.MEMBER2_EMAIL


@pytest.fixture
def member2_password():
    return config.MEMBER2_PASSWORD


@pytest.fixture
def private_key():
    return config.API_TESTS_PRIVATE_KEY


@pytest.fixture
def public_key():
    return config.API_TESTS_PUBLIC_KEY


@pytest.fixture
def api_test_machine_name():
    return config.API_TESTING_MACHINE_NAME


@pytest.fixture
def private_key():
    return config.API_TESTING_MACHINE_PRIVATE_KEY


@pytest.fixture
def public_key():
    return config.API_TESTING_MACHINE_PUBLIC_KEY


@pytest.fixture
def cloud_name():
    return config.API_TESTING_CLOUD


@pytest.fixture
def org_name():
    return config.ORG_NAME

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
                                     machine_id=machine['id'], action='start').post()
