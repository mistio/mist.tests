import pytest

from time import time

from datetime import date
from datetime import timedelta

from misttests import config
from io import MistIoApi
from mist.io.clouds.models import Cloud
from mist.io.networks.models import Network, Subnet


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
    return config.OWNER_EMAIL


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
def network_test_cloud_names():
    return config.NETWORK_TESTING_CLOUDS


@pytest.fixture(params=network_test_cloud_names())
def network_test_cloud(request):
    test_cloud = Cloud.objects.get(title=request.param)
    return test_cloud


@pytest.fixture()
def network_test_cleanup(request):
    def fin():
        for network in Network.objects(description='api-test-net'):
            try:
                network.ctl.delete()
            except Exception as e:
                print 'Failed to delete network {0}: exception:{1}'.format(network.id, e.message)
        for subnet in Subnet.objects(description='api-test-subnet'):
            try:
                subnet.ctl.delete()
            except Exception as e:
                print 'Failed to delete subnet {0} exception:{1}'.format(subnet.id, e.message)
    request.addfinalizer(fin)
    return None
