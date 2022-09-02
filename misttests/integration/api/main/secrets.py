import pytest

from misttests.integration.api.helpers import assert_response_unauthorized
from misttests.integration.api.helpers import assert_response_bad_request
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import assert_response_not_found

from misttests.config import safe_get_var
from misttests import config


def test_list_secrets(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.list_secrets(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print("Success!!!")


def test_delete_secret_wrong_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.delete_secret(secret_id='dummy',
                                         api_token=owner_api_token).delete()
    assert_response_not_found(response)
    print("Success!!!")


def test_delete_secret_wrong_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.delete_secret(secret_id='dummy',
                                         api_token='dummy').delete()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_create_secret_no_name(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.create_secret(name='', secret={'a': 'b'},
                                         api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print("Success!!!")


def test_create_secret_no_secret(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.create_secret(name='dummy', secret={},
                                         api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print("Success!!!")


def test_get_secret_wrong_id(pretty_print, cache, mist_api_v1,
                             owner_api_token):
    response = mist_api_v1.get_secret('dummy', api_token=owner_api_token).get()
    assert_response_not_found(response)
    print("Success!!!")


# ############################################################################
# #                          Functional Testing                              #
# ############################################################################


@pytest.mark.incremental
class TestSecretsFunctionality:
    def test_create_secret(self, pretty_print, cache, mist_api_v1,
                           owner_api_token):
        response = mist_api_v1.list_secrets(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 0
        response = mist_api_v1.create_secret(
            name='TestKey',
            secret="Just a string",
            api_token=owner_api_token).post()
        assert_response_bad_request(response)
        response = mist_api_v1.create_secret(
            name='TestKey',
            secret={'password': 'password'},
            api_token=owner_api_token).post()
        assert_response_ok(response)
        cache.set('secret_id', response.json()['id'])
        response = mist_api_v1.list_secrets(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 1
        print("Success!!!")

    def test_create_secret_duplicate_name(self, pretty_print, mist_api_v1,
                                          owner_api_token):
        response = mist_api_v1.create_secret(
            name='TestKey',
            secret={"username": "username"},
            api_token=owner_api_token).post()
        assert_response_bad_request(response)
        print("Success!!!")

    def test_get_secret(self, pretty_print, cache, mist_api_v1,
                        owner_api_token):
        response = mist_api_v1.get_secret(
                    secret_id=cache.get('secret_id', ''),
                    api_token=owner_api_token).get()
        assert_response_ok(response)
        assert isinstance(response.json(), dict), "Returned value \
            is not of type `dict`"
        assert response.json() == {'password': 'password'}, "Wrong \
            value returned!"
        # TODO: extra get_secret, requesting key (correct and wrong)
        print("Success")

    def test_update_secret(self, pretty_print, cache, mist_api_v1,
                           owner_api_token):
        response = mist_api_v1.update_secret(
                    secret_id=cache.get('secret_id', ''),
                    secret='String',
                    api_token=owner_api_token).put()
        assert_response_bad_request(response)
        response = mist_api_v1.update_secret(secret_id=cache.get('secret_id',
                                                                 ''),
                                             secret={"username": "username"},
                                             api_token=owner_api_token).put()
        assert_response_ok(response)
        response = mist_api_v1.get_secret(
                    secret_id=cache.get('secret_id', ''),
                    api_token=owner_api_token).get()
        assert_response_ok(response)
        expected_dict = {
            "username": "username",
            "password": "password"
        }
        assert response.json() == expected_dict, "Wrong value returned!"
        print("Success")

    def test_delete_secret(self, pretty_print, cache, mist_api_v1,
                           owner_api_token):
        response = mist_api_v1.delete_secret(
                    secret_id=cache.get('secret_id', ''),
                    api_token=owner_api_token).delete()
        assert_response_ok(response)
        response = mist_api_v1.list_secrets(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 0
        print("Success!!!")

    def test_add_key_from_secret(self, pretty_print, cache, mist_api_v1,
                                 owner_api_token, private_key):
        # first, store key in Vault
        response = mist_api_v1.create_secret(
            name='TestKey',
            secret={'private': private_key},
            api_token=owner_api_token).post()
        assert_response_ok(response)
        cache.set('secret_id', response.json()['id'])

        # add a key, using secret's id
        response = mist_api_v1.add_key(
            name='TestKey',
            private='secret(TestKey:private)',
            api_token=owner_api_token).put()
        assert_response_ok(response)
        cache.set('key_id', response.json()['id'])
        response = mist_api_v1.get_private_key(key_id=cache.get('key_id', ''),
                                               api_token=owner_api_token).get()
        assert_response_ok(response)
        assert response.json() == private_key
        print("Success!!!")

    def test_add_cloud_from_secret(self, pretty_print, mist_api_v1, cache,
                                   owner_api_token, private_key):
        # first, add cloud
        token = safe_get_var('clouds/digitalocean', 'token',
                             config.CREDENTIALS['DIGITALOCEAN']['token'])
        response = mist_api_v1.add_cloud('Digital Ocean',
                                         provider='digitalocean',
                                         api_token=owner_api_token,
                                         token=token).post()
        cache.set('cloud_id', response.json()['id'])
        assert_response_ok(response)
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 1
        # add another cloud, using the same credentials, obtained from secret
        token = 'secret(mist/clouds/Digital Ocean:token)'
        response = mist_api_v1.add_cloud('Digital Ocean New',
                                         provider='digitalocean',
                                         api_token=owner_api_token,
                                         token=token).post()
        assert_response_ok(response)
        response = mist_api_v1.list_clouds(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 2
        print("Success!!!")

    def test_delete_cloud_from_vault(self, pretty_print, mist_api_v1,
                                     cache, owner_api_token):
        response = mist_api_v1.remove_cloud(cloud_id=cache.get('cloud_id', ''),
                                            api_token=owner_api_token,
                                            delete_from_vault=True).delete()
        response = mist_api_v1.list_secrets(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 1
        print("Success!!!")
