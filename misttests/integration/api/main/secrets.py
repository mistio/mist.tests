import pytest

from misttests.integration.api.helpers import assert_response_unauthorized
from misttests.integration.api.helpers import assert_response_bad_request
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import assert_response_not_found


def test_list_secrets(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_secrets(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print "Success!!!"


def test_delete_secret_wrong_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_secret(secret_id='dummy',
                                       api_token=owner_api_token).delete()
    assert_response_not_found(response)
    print "Success!!!"


def test_delete_secret_wrong_api_token(pretty_print, mist_core):
    response = mist_core.delete_secret(secret_id='dummy',
                                       api_token='dummy').delete()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_create_secret_no_name(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_secret(name='', secret={'a': 'b'},
                                       api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_create_secret_no_secret(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_secret(name='dummy', secret={},
                                       api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_get_secret_wrong_id(pretty_print, cache, mist_core,
                             owner_api_token):
    response = mist_core.get_secret('dummy', api_token=owner_api_token).get()
    assert_response_not_found(response)
    print "Success!!!"


# ############################################################################
# #                          Functional Testing                              #
# ############################################################################


@pytest.mark.incremental
class TestSecretsFunctionality:
    def test_create_secret(self, pretty_print, cache, mist_core,
                           owner_api_token):
        response = mist_core.list_secrets(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 0
        response = mist_core.create_secret(
            name='TestKey',
            secret="Just a string",
            api_token=owner_api_token).post()
        assert_response_bad_request(response)
        response = mist_core.create_secret(
            name='TestKey',
            # TODO: make it configurable
            secret={'password': 'password'},
            api_token=owner_api_token).post()
        assert_response_ok(response)
        cache.set('secret_id', response.json()['id'])
        response = mist_core.list_secrets(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 1
        print "Success!!!"

    def test_create_secret_duplicate_name(self, pretty_print, mist_core,
                                          owner_api_token):
        response = mist_core.create_secret(
            name='TestKey',
            secret={"username": "username"},
            api_token=owner_api_token).post()
        assert_response_bad_request(response)
        print "Success!!!"

    def test_get_secret(self, pretty_print, cache, mist_core,
                        owner_api_token):
        response = mist_core.get_secret(
                    secret_id=cache.get('secret_id', ''),
                    api_token=owner_api_token).get()
        assert_response_ok(response)
        # TODO: Make sure that response is a dict: {"password": "password"}

        # TODO: extra get_Secret, with key: password
        # TODO: extra get_Secret, with key that does not exist
        print "Success"
