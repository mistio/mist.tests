import time

import pytest

from misttests.config import MIST_URL
from misttests.integration.api.helpers import poll
from misttests.integration.api.helpers import assert_response_found
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.mistrequests import MistRequests
from misttests.integration.api.main.v2.setup import machines_3 as _setup_module

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


class TestMachinesController2:
    """MachinesController integration test stubs"""

    def test_clone_machine(self, pretty_print, owner_api_token):
        """Test case for clone_machine

        Clone machine
        """
        query_string = setup_data.get('clone_machine', {}).get(
            'query_string') or [('name', 'my-machine-clone'),
                                ('run_async', False)]
        uri = MIST_URL + '/api/v2/machines/{machine}/actions/clone'.format(
            machine=setup_data.get('clone_machine', {}).get('machine')
            or setup_data.get('machine') or 'my-machine')
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            params=query_string)
        request_method = getattr(request, 'POST'.lower())
        response = request_method()
        if 'clone_machine' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        assert poll(
            api_token=owner_api_token,
            uri=setup_data['clone_machine_uri'],
            data={'state': 'running', 'actions': {'suspend': True}},
            timeout=_setup_module.DEFAULT_TIMEOUT)
        print('Success!!!')

    def test_console(self, pretty_print, owner_api_token):
        """Test case for console

        Open console
        """
        uri = MIST_URL + '/api/v2/machines/{machine}/actions/console'.format(
            machine=setup_data.get('console', {}).get('machine')
            or setup_data.get('machine') or 'my-machine')
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri)
        request_method = getattr(request, 'POST'.lower())
        response = request_method()
        if 'console' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        print('Success!!!')

    def test_destroy_machine(self, pretty_print, owner_api_token):
        """Test case for destroy_machine

        Destroy machine
        """
        uri = MIST_URL + '/api/v2/machines/{machine}/actions/destroy'.format(
            machine=setup_data.get('destroy_machine', {}).get('machine')
            or setup_data.get('machine') or 'my-machine')
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri)
        request_method = getattr(request, 'POST'.lower())
        response = request_method()
        if 'destroy_machine' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        assert poll(
            api_token=owner_api_token,
            uri=setup_data['clone_machine_uri'],
            data={'state': 'terminated', 'actions': {'undefine': True}},
            timeout=_setup_module.DEFAULT_TIMEOUT)
        print('Success!!!')

    def test_resume_machine(self, pretty_print, owner_api_token):
        """Test case for resume_machine

        Resume machine
        """
        uri = MIST_URL + '/api/v2/machines/{machine}/actions/resume'.format(
            machine=setup_data.get('resume_machine', {}).get('machine')
            or setup_data.get('machine') or 'my-machine')
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri)
        request_method = getattr(request, 'POST'.lower())
        response = request_method()
        if 'resume_machine' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        assert poll(
            api_token=owner_api_token,
            uri=setup_data['clone_machine_uri'],
            data={'state': 'running', 'actions': {'destroy': True}},
            timeout=_setup_module.DEFAULT_TIMEOUT)
        print('Success!!!')

    def test_suspend_machine(self, pretty_print, owner_api_token):
        """Test case for suspend_machine

        Suspend machine
        """
        uri = MIST_URL + '/api/v2/machines/{machine}/actions/suspend'.format(
            machine=setup_data.get('suspend_machine', {}).get('machine')
            or setup_data.get('machine') or 'my-machine')
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri)
        request_method = getattr(request, 'POST'.lower())
        response = request_method()
        if 'suspend_machine' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        assert poll(
            api_token=owner_api_token,
            uri=setup_data['clone_machine_uri'],
            data={'state': 'suspended', 'actions': {'resume': True}},
            timeout=_setup_module.DEFAULT_TIMEOUT)
        print('Success!!!')

    def test_undefine_machine(self, pretty_print, owner_api_token):
        """Test case for undefine_machine

        Undefine machine
        """
        query_string = setup_data.get('undefine_machine', {}).get(
            'query_string') or [('delete_domain_image', True)]
        uri = MIST_URL + '/api/v2/machines/{machine}/actions/undefine'.format(
            machine=setup_data.get('undefine_machine', {}).get('machine')
            or setup_data.get('machine') or 'my-machine')
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            params=query_string)
        request_method = getattr(request, 'POST'.lower())
        response = request_method()
        if 'undefine_machine' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        print('Success!!!')


# Impose custom ordering of machines test methods
for order, k in enumerate(_setup_module.TEST_METHOD_ORDERING):
    method_name = k if k.startswith('test_') else f'test_{k}'
    method = getattr(TestMachinesController2, method_name)
    setattr(TestMachinesController2, method_name,
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


TestMachinesController2 = pytest.mark.usefixtures('setup')(
    TestMachinesController2)