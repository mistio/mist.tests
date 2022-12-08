import json
import time

import pytest

from misttests.config import MIST_URL
from misttests.integration.api.helpers import poll
from misttests.integration.api.helpers import assert_response_found
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.mistrequests import MistRequests
from misttests.integration.api.main.v2.setup import machines_2 as _setup_module

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

    def test_associate_key(self, pretty_print, owner_api_token):
        """Test case for associate_key

        Associate a key with a machine
        """
        key_machine_association = setup_data.get('associate_key', {}).get(
            'request_body') or json.loads("""{
  "port" : 1,
  "machine" : "machine",
  "last_used" : 6,
  "sudo" : true,
  "user" : "user",
  "key" : "key"
}""", strict=False)
        machine = setup_data.get('associate_key', {}).get('machine') or \
            setup_data.get('machine') or 'my-machine'
        uri = MIST_URL + \
            '/api/v2/machines/{machine}/actions/associate-key'.format(
                machine=machine)
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            json=key_machine_association)
        request_method = getattr(request, 'PUT'.lower())
        response = request_method()
        if 'associate_key' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        print('Success!!!')

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
            data={'state': 'running', 'actions': {'rename': True}},
            timeout=_setup_module.DEFAULT_TIMEOUT,
            post_delay=60)
        print('Success!!!')

    def test_disassociate_key(self, pretty_print, owner_api_token):
        """Test case for disassociate_key

        Disassociate a key from a machine
        """
        key_machine_disassociation = setup_data.get(
            'disassociate_key', {}).get(
            'request_body') or json.loads("""{
  "key" : "key"
}""", strict=False)
        machine = setup_data.get('disassociate_key', {}).get('machine') or \
            setup_data.get('machine') or 'my-machine'
        uri = MIST_URL + \
            '/api/v2/machines/{machine}/actions/disassociate-key'.format(
                machine=machine)
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            json=key_machine_disassociation)
        request_method = getattr(request, 'DELETE'.lower())
        response = request_method()
        if 'disassociate_key' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        print('Success!!!')

    def test_edit_machine(self, pretty_print, owner_api_token):
        """Test case for edit_machine

        Edit machine
        """
        edit_machine_request = setup_data.get('edit_machine', {}).get(
            'request_body') or json.loads("""{
  "expiration" : {
    "date" : "date",
    "action" : "stop",
    "notify" : 0
  }
}""", strict=False)
        machine = setup_data.get('edit_machine', {}).get('machine') or \
            setup_data.get('machine') or 'my-machine'
        uri = MIST_URL + '/api/v2/machines/{machine}'.format(machine=machine)
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            json=edit_machine_request)
        request_method = getattr(request, 'PUT'.lower())
        response = request_method()
        if 'edit_machine' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        assert poll(
            api_token=owner_api_token,
            uri=setup_data['amazon_machine_uri'],
            data={'actions': {'rename': True}},
            timeout=_setup_module.DEFAULT_TIMEOUT)
        print('Success!!!')

    def test_get_machine(self, pretty_print, owner_api_token):
        """Test case for get_machine

        Get machine
        """
        query_string = setup_data.get('get_machine', {}).get(
            'query_string') or [('only', 'id'),
                                ('deref', 'auto')]
        machine = setup_data.get('get_machine', {}).get('machine') or \
            setup_data.get('machine') or 'my-machine'
        uri = MIST_URL + '/api/v2/machines/{machine}'.format(machine=machine)
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            params=query_string)
        request_method = getattr(request, 'GET'.lower())
        response = request_method()
        if 'get_machine' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        print('Success!!!')

    def test_list_machines(self, pretty_print, owner_api_token):
        """Test case for list_machines

        List machines
        """
        default_query_string = [('cloud', '0194030499e74b02bdf68fa7130fb0b2'),
                                ('search',
                                 'state:running'),
                                ('sort',
                                 '-name'),
                                ('start',
                                 '50'),
                                ('limit', 56),
                                ('only',
                                 'id'),
                                ('deref',
                                 'auto'),
                                ('at', '2021-07-21T17:32:28Z')]
        query_string = setup_data.get('list_machines', {}).get(
            'query_string') or default_query_string
        uri = MIST_URL + '/api/v2/machines'
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            params=query_string)
        request_method = getattr(request, 'GET'.lower())
        response = request_method()
        if 'list_machines' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        print('Success!!!')

    def test_rename_machine(self, pretty_print, owner_api_token):
        """Test case for rename_machine

        Rename machine
        """
        query_string = setup_data.get('rename_machine', {}).get(
            'query_string') or [('name', 'my-renamed-machine')]
        machine = setup_data.get('rename_machine', {}).get(
            'machine') or setup_data.get('machine') or 'my-machine'
        uri = MIST_URL + '/api/v2/machines/{machine}/actions/rename'.format(
            machine=machine)
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            params=query_string)
        request_method = getattr(request, 'POST'.lower())
        response = request_method()
        if 'rename_machine' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        print('Success!!!')

    def test_ssh(self, pretty_print, owner_api_token):
        """Test case for ssh

        Open secure shell
        """
        machine = setup_data.get('ssh', {}).get(
            'machine') or setup_data.get('machine') or 'my-machine'
        uri = MIST_URL + \
            '/api/v2/machines/{machine}/actions/ssh'.format(machine=machine)
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri)
        request_method = getattr(request, 'POST'.lower())
        response = request_method()
        if 'ssh' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
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