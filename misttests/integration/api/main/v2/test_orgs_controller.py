import json
import time
import importlib
import random
import string
import pytest

from misttests.config import MIST_URL
from misttests.integration.api.helpers import assert_response_found
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.mistrequests import MistRequests

DELETE_KEYWORDS = ['delete', 'destroy', 'remove']
REDIRECT_OPERATIONS = ['ssh', 'console']

resource_name = 'OrgsController'.replace('Controller', '').lower()
resource_name_singular = resource_name.strip('s')
try:
    _setup_module = importlib.import_module(
        f'misttests.integration.api.main.v2.setup.{resource_name}')
except ImportError:
    SETUP_MODULE_EXISTS = False
else:
    SETUP_MODULE_EXISTS = True
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


class TestOrgsController:
    """OrgsController integration test stubs"""

    def test_create_org(self, pretty_print, owner_api_token):
        """Test case for create_org

        Create org
        """
        postfix = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        create_organization_request = setup_data.get('create_org', {}).get(
            'request_body') or json.loads(("""{
  "name" : "org-%s",
  "description" : "description",
  "logo" : "logo"
}""" % postfix), strict=False)
        uri = MIST_URL + '/api/v2/orgs'
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            json=create_organization_request)
        request_method = getattr(request, 'POST'.lower())
        response = request_method()
        if 'create_org' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        print('Success!!!')

    def test_get_member(self, pretty_print, owner_api_token):
        """Test case for get_member

        Get Org
        """
        query_string = setup_data.get('get_member', {}).get('query_string') or [('only', 'id')]
        uri = MIST_URL + '/api/v2/orgs/{org}/members/{member}'.format(
            org=setup_data.get('get_member', {}).get('org'), member=setup_data.get('get_member', {}).get('member') or setup_data.get('member') or 'my-member')
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            params=query_string)
        request_method = getattr(request, 'GET'.lower())
        response = request_method()
        if 'get_member' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        print('Success!!!')

    def test_get_org(self, pretty_print, owner_api_token):
        """Test case for get_org

        Get Org
        """
        query_string = setup_data.get('get_org', {}).get('query_string') or [('summary', False),
                        ('only', 'id'),
                        ('deref', 'auto')]
        uri = MIST_URL + '/api/v2/orgs/{org}'.format(
            org=setup_data.get('get_org', {}).get('org'))
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            params=query_string)
        request_method = getattr(request, 'GET'.lower())
        response = request_method()
        if 'get_org' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        print('Success!!!')

    def test_list_org_members(self, pretty_print, owner_api_token):
        """Test case for list_org_members

        List org members
        """
        query_string = setup_data.get('list_org_members', {}).get('query_string') or [('search', 'email:dev@mist.io'),
                        ('sort', '-name'),
                        ('start', '50'),
                        ('limit', 56),
                        ('only', 'id'),
                        ('at', '2021-07-21T17:32:28Z')]
        uri = MIST_URL + '/api/v2/orgs/{org}/members'.format(
            org=setup_data.get('list_org_members', {}).get('org'))
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            params=query_string)
        request_method = getattr(request, 'GET'.lower())
        response = request_method()
        if 'list_org_members' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        print('Success!!!')

    def test_list_org_teams(self, pretty_print, owner_api_token):
        """Test case for list_org_teams

        List org teams
        """
        query_string = setup_data.get('list_org_teams', {}).get('query_string') or [('search', 'name:finance'),
                        ('sort', '-name'),
                        ('start', '50'),
                        ('limit', 56),
                        ('only', 'id'),
                        ('deref', 'auto'),
                        ('at', '2021-07-21T17:32:28Z')]
        uri = MIST_URL + '/api/v2/orgs/{org}/teams'.format(
            org=setup_data.get('list_org_teams', {}).get('org'))
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            params=query_string)
        request_method = getattr(request, 'GET'.lower())
        response = request_method()
        if 'list_org_teams' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        print('Success!!!')

    def test_list_orgs(self, pretty_print, owner_api_token):
        """Test case for list_orgs

        List orgs
        """
        query_string = setup_data.get('list_orgs', {}).get('query_string') or [('allorgs', 'true'),
                        ('search', 'name:Acme'),
                        ('sort', '-name'),
                        ('start', '50'),
                        ('limit', 56),
                        ('only', 'id'),
                        ('deref', 'auto'),
                        ('at', '2021-07-21T17:32:28Z')]
        uri = MIST_URL + '/api/v2/orgs'
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            params=query_string)
        request_method = getattr(request, 'GET'.lower())
        response = request_method()
        if 'list_orgs' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        print('Success!!!')

    def test_update_org(self, pretty_print, owner_api_token):
        """Test case for update_org


        """
        body = """{
  "name" : "%s",
  "vault" : {
      "address" : "vault_address",
      "secrets_engine_path" : "vault_secrets_engine_path",
      "token": "vault_token",
      "role_id" : "vault_role_id",
      "secret_id": "vault_secret_id"
  }
}""" % setup_data.get('update_org', {}).get('org_name', '')
        patch_organization_request = setup_data.get('update_org', {}).get(
            'request_body') or json.loads(body, strict=False)
        uri = MIST_URL + '/api/v2/orgs/{org}'.format(
            org=setup_data.get('get_org', {}).get('org'))
        request = MistRequests(
            api_token=owner_api_token,
            uri=uri,
            json=patch_organization_request)
        request_method = getattr(request, 'PATCH'.lower())
        response = request_method()
        if 'update_org' in REDIRECT_OPERATIONS:
            assert_response_found(response)
        else:
            assert_response_ok(response)
        print('Success!!!')


if hasattr(_setup_module, 'TEST_METHOD_ORDERING'):
    # Impose custom ordering of machines test methods
    for order, k in enumerate(_setup_module.TEST_METHOD_ORDERING):
        method_name = k if k.startswith('test_') else f'test_{k}'
        method = getattr(TestOrgsController, method_name)
        setattr(TestOrgsController, method_name,
                pytest.mark.order(order + 1)(method))
else:
    # Mark delete-related test methods as last to be run
    for key in vars(TestOrgsController):
        attr = getattr(TestOrgsController, key)
        if callable(attr) and any(k in key for k in DELETE_KEYWORDS):
            setattr(TestOrgsController, key, pytest.mark.order('last')(attr))

if SETUP_MODULE_EXISTS:
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
    TestOrgsController = pytest.mark.usefixtures('setup')(
        TestOrgsController)
