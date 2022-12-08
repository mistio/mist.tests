import time
import importlib

import pytest

from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.mistrequests import MistRequests
from misttests.integration.api.utils import assert_equal, assert_in
from datetime import datetime

from misttests.integration.api.utils import assert_list_empty

from misttests.integration.api.main.v2.setup.search_tags import N_KEYS
from misttests.integration.api.main.v2.setup.search_tags import KEYS_URI
from misttests.integration.api.main.v2.setup.search_tags import TAGS_URI

try:
    _setup_module = importlib.import_module(
        'misttests.integration.api.main.v2.setup.search_tags')
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


def search_keys_template(owner_api_token, query_string):

    print(datetime.now().time())
    print(f"The tagged resources are {setup_data['tagged']} \n")
    print("Hitting the api:")

    response = MistRequests(
        api_token=owner_api_token,
        uri=KEYS_URI,
        params=query_string).get()

    assert_response_ok(response)
    print("List keys with query=", query_string)
    data = response.json()['data']
    print(data)

    return data


class TestSearchTags:
    """Search by tags in list_keys test stubs"""

    def test_search_tags_before_tagging(self, pretty_print, owner_api_token):
        """
            Test case for searching keys by tags when no
            key is tagged. Should return []
        """
        query_string = [('search', 'tag:dev,value1'), ('only', 'id')]
        data = search_keys_template(owner_api_token, query_string)
        assert_list_empty(data)
        print('Success!!!')

    def test_tag_keys(self, pretty_print, owner_api_token):
        """
            Test case for tagging keys.
        """
        request = MistRequests(
            api_token=owner_api_token,
            uri=TAGS_URI,
            json=setup_data['tag_request'])

        response = request.post()
        assert_response_ok(response)
        print(f'Tagged at {datetime.now().time()} \n')
        print(f"{setup_data['tag_request']['operations'][0]['resources']}\n")

        # Check if the keys are tagged
        query_params = [('search', 'tagged-key')]
        response = MistRequests(
            api_token=owner_api_token,
            uri=KEYS_URI,
            params=query_params).get()

        assert_response_ok(response)

    def test_search_fulltag(self, pretty_print, owner_api_token):
        """Test case for search Keys by full tag=key:value"""

        # Checking if all Keys exist:
        print('Checking if all Keys exist:\n')
        query_string = [('only', 'id')]

        response = MistRequests(
            api_token=owner_api_token,
            uri=KEYS_URI,
            params=query_string).get()
        assert_response_ok(response)
        print(response.json()['data'])
        assert_equal(response.json()['meta']['total'], N_KEYS)

        query_string = [('search', 'tag:dev,value1'), ('only', 'id')]
        data = search_keys_template(owner_api_token, query_string)
        for id in setup_data['tagged']:
            assert_in(id, data)
        print('Success!!!')

    def test_search_only_tagkey(self, pretty_print, owner_api_token):
        """Test case for search Keys by tagkey"""

        query_string = [('search', 'tag:dev,value1'), ('only', 'id')]
        data = search_keys_template(owner_api_token, query_string)
        for id in setup_data['tagged']:
            assert_in(id, data)
        print('Success!!!')

    def test_search_only_tagvalue(self, pretty_print, owner_api_token):
        """Test case for search Keys by tagValue"""

        query_string = [('search', 'tag:,value1'), ('only', 'id')]
        data = search_keys_template(owner_api_token, query_string)
        for id in setup_data['tagged']:
            assert_in(id, data)
        print('Success!!!')

    def test_search_implicit_tagkey(self, pretty_print, owner_api_token):
        """Test case for implicit search Keys by tagKey"""

        query_string = [('search', 'dev'), ('only', 'id')]
        data = search_keys_template(owner_api_token, query_string)
        for id in setup_data['tagged']:
            assert_in(id, data)
        print('Success!!!')

    def test_search_implicit_tagValue(self, pretty_print, owner_api_token):
        """Test case for implicit search Keys by tagValue"""

        query_string = [('search', 'value1'), ('only', 'id')]
        data = search_keys_template(owner_api_token, query_string)
        for id in setup_data['tagged']:
            assert_in(id, data)
        print('Success!!!')

    def test_untag_keys(self, pretty_print, owner_api_token):
        """Test case for untagging keys.
        """
        print(datetime.now().time())
        print("Untagging")
        remove_request = setup_data['tag_request'].copy()
        remove_request['operations'][0].update({'operation': 'remove'})

        request = MistRequests(
            api_token=owner_api_token,
            uri=TAGS_URI,
            json=remove_request)

        response = request.post()
        assert_response_ok(response)
        print('Success!!!')

    def test_search_tags_after_untagging(self, pretty_print, owner_api_token):
        """
            Test case for searching keys by tags when no
            key is tagged. Should return []
        """
        query_string = [('search', 'tag:dev,value1'), ('only', 'id')]
        data = search_keys_template(owner_api_token, query_string)
        assert_list_empty(data)
        print('Success!!!')


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
    TestSearchTags = pytest.mark.usefixtures('setup')(
        TestSearchTags)