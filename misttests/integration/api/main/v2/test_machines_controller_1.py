import json
import time

import pytest

from misttests.config import MIST_URL
from misttests.integration.api.helpers import poll
from misttests.integration.api.helpers import assert_response_found
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.mistrequests import MistRequests
from misttests.integration.api.main.v2.setup import machines_1 as _setup_module

DELETE_KEYWORDS = ['delete', 'destroy', 'remove']
REDIRECT_OPERATIONS = ['ssh', 'console']


setup_data = {}


@pytest.fixture(autouse=True)
def after_test(request):
    yield
    method_name = request._pyfuncitem._obj.__name__
    test_operation = method_name.replace('test_', '')
    callback = setup_data.get(test_operation, {}).get('callback')
    if callable(callback):
        assert callback()
    else:
        sleep = setup_data.get(test_operation, {}).get('sleep')
        if sleep:
            time.sleep(sleep)


class TestMachinesController1:
    """MachinesController integration test stubs"""

    def test_create_machine(self, pretty_print, owner_api_token):
        """Test case for create_machine

        Create machine
        """
        create_machine_request = setup_data.get('create_machine', {}).get(
            'request_body') or json.loads("""{
  "template" : "{}",
  "image" : "Debian",
  "quantity" : 1.4658129805029452,
  "disks" : {
    "disk_size" : 0,
    "disk_path" : "disk_path"
  },
  "fqdn" : "fqdn",
  "cloudinit" : "cloudinit",
  "volumes" : "",
  "save" : true,
  "dry" : true,
  "monitoring" : true,
  "tags" : "{}",
  "cloud" : "cloud",
  "size" : "m1.small",
  "optimize" : "optimize",
  "schedules" : [ "", "" ],
  "extra" : "",
  "name" : "DB mirror",
  "location" : "",
  "expiration" : {
    "date" : "2000-01-23T04:56:07.000+00:00",
    "action" : "stop",
    "notify" : {
      "period" : "minutes",
      "value" : 1
    },
    "notify_msg" : "notify_msg"
  },
  "net" : "",
  "scripts" : [ "", "" ],
  "key" : ""
}""", strict=False)
        uri = MIST_URL + '/api/v2/machines'
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            json=create_machine_request)
        request_method = getattr(request, 'POST'.lower())
        response = request_method()
        if 'create_machine' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        assert poll(
            api_token=owner_api_token,
            uri=setup_data['amazon_machine_uri'],
            data={'state': 'running', 'actions': {'reboot': True}},
            timeout=_setup_module.DEFAULT_TIMEOUT)
        print('Success!!!')

    def test_reboot_machine(self, pretty_print, owner_api_token):
        """Test case for reboot_machine

        Reboot machine
        """
        machine = setup_data.get('reboot_machine', {}).get(
            'machine') or setup_data.get('machine') or 'my-machine'
        uri = MIST_URL + \
            '/api/v2/machines/{machine}/actions/reboot'.format(machine=machine)
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri)
        request_method = getattr(request, 'POST'.lower())
        response = request_method()
        if 'reboot_machine' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        assert poll(
            api_token=owner_api_token,
            uri=setup_data['amazon_machine_uri'],
            data={'state': 'running', 'actions': {'stop': True}},
            timeout=_setup_module.DEFAULT_TIMEOUT)
        print('Success!!!')

    def test_resize_machine(self, pretty_print, owner_api_token):
        """Test case for resize_machine

        Resize machine
        """
        query_string = setup_data.get('resize_machine', {}).get(
            'query_string') or [('size', '9417745961a84bffbf6419e5of68faa5')]
        machine = setup_data.get('resize_machine', {}).get('machine') \
            or setup_data.get('machine') or 'my-machine'
        uri = MIST_URL + \
            '/api/v2/machines/{machine}/actions/resize'.format(machine=machine)
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            params=query_string)
        request_method = getattr(request, 'POST'.lower())
        response = request_method()
        if 'resize_machine' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        assert poll(
            api_token=owner_api_token,
            uri=setup_data['amazon_machine_uri'],
            data={'actions': {'start': True}},
            timeout=_setup_module.DEFAULT_TIMEOUT)
        print('Success!!!')

    def test_start_machine(self, pretty_print, owner_api_token):
        """Test case for start_machine

        Start machine
        """
        machine = setup_data.get('start_machine', {}).get('machine') \
            or setup_data.get('machine') or 'my-machine'
        uri = MIST_URL + \
            '/api/v2/machines/{machine}/actions/start'.format(machine=machine)
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri)
        request_method = getattr(request, 'POST'.lower())
        response = request_method()
        if 'start_machine' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        assert poll(
            api_token=owner_api_token,
            uri=setup_data['amazon_machine_uri'],
            data={'state': 'running', 'actions': {'stop': True}},
            timeout=_setup_module.DEFAULT_TIMEOUT)
        print('Success!!!')

    def test_stop_machine(self, pretty_print, owner_api_token):
        """Test case for stop_machine

        Stop machine
        """
        machine = setup_data.get('stop_machine', {}).get(
            'machine') or setup_data.get('machine') or 'my-machine'
        uri = MIST_URL + \
            '/api/v2/machines/{machine}/actions/stop'.format(machine=machine)
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri)
        request_method = getattr(request, 'POST'.lower())
        response = request_method()
        if 'stop_machine' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        assert poll(
            api_token=owner_api_token,
            uri=setup_data['amazon_machine_uri'],
            data={'state': 'stopped', 'actions': {'resize': True}},
            timeout=_setup_module.DEFAULT_TIMEOUT)
        print('Success!!!')


# Impose custom ordering of machines test methods
for order, k in enumerate(_setup_module.TEST_METHOD_ORDERING):
    method_name = k if k.startswith('test_') else f'test_{k}'
    method = getattr(TestMachinesController1, method_name)
    setattr(TestMachinesController1, method_name,
            pytest.mark.order(order + 1)(method))

# Add setup and teardown methods to test class
class_setup_done = False


@pytest.fixture(scope='class')
def setup(owner_api_token):
    global class_setup_done
    if class_setup_done:
        yield
    else:
        global setup_data
        setup_data = _setup_module.setup(owner_api_token) or {}
        yield
        _setup_module.teardown(owner_api_token, setup_data)
        class_setup_done = True


TestMachinesController1 = pytest.mark.usefixtures('setup')(
    TestMachinesController1)