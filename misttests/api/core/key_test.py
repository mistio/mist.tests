import pytest
import requests

from misttests.api.helpers import *


#############################################################################
# Unit testing
#############################################################################


def test_001_list_keys(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_keys(api_token=owner_api_token).get()
    assert_response_ok(response)
    print "Success!!!"


def test_002_add_key_with_no_id_and_no_priv(pretty_print, mist_core,
                                            owner_api_token):
    response = mist_core.add_key(name='', private='',
                                 api_token=owner_api_token).put()
    assert_response_bad_request(response)
    print "Success!!!"


def test_003_add_key_with_no_private(pretty_print, cache, mist_core,
                                     owner_api_token):
    response = mist_core.list_keys(api_token=owner_api_token).get()
    assert_response_ok(response)
    keys_list = json.loads(response.content)
    cache.set('keys_tests/key_name', get_random_key_id(keys_list))
    response = mist_core.add_key(name=cache.get('keys_tests/key_name', ''),
                                 private='',
                                 api_token=owner_api_token).put()
    assert_response_bad_request(response)
    print "Success!!!"


def test_004_add_key_with_wrong_private(pretty_print, cache, mist_core,
                                        owner_api_token, private_key):
    response = mist_core.add_key(name=cache.get('keys_tests/key_name', ''),
                                 private=private_key[:-40],
                                 api_token=owner_api_token).put()
    assert_response_bad_request(response)
    print "Success!!!"


def test_005_get_private_key_with_wrong_id(pretty_print, cache, mist_core,
                                           owner_api_token):
    response = mist_core.get_private_key('bla', api_token=owner_api_token).get()
    assert_response_not_found(response)
    print "Success!!!"


def test_006_get_private_key_with_wrong_id(pretty_print, cache, mist_core,
                                           owner_api_token):
    response = mist_core.get_private_key(
        cache.get('keys_tests/key_name', '')[:-2],
        api_token=owner_api_token).get()
    assert_response_not_found(response)
    print "Success!!!"


def test_007_get_public_key_with_wrong_id(pretty_print, cache, mist_core,
                                          owner_api_token):
    response = mist_core.get_public_key(
        cache.get('keys_tests/key_name', '')[:-2],
        api_token=owner_api_token).get()
    assert_response_not_found(response)
    print "Success!!!"


def test_008_set_default_key_with_wrong_key_id(pretty_print, cache, mist_core,
                                               owner_api_token):
    response = mist_core.set_default_key(
        key_id='bla',
        api_token=owner_api_token).post()
    assert_response_not_found(response)
    print "Success!!!"


def test_009_test_generate_keypair(pretty_print, mist_core, owner_api_token):
    response = mist_core.generate_keypair(api_token=owner_api_token).post()
    assert_response_ok(response)
    print "Success!!!"


def test_010_delete_multiple_keys_with_no_key_ids(pretty_print, mist_core,
                                                  owner_api_token):
    response = mist_core.delete_keys(key_ids=[],
                                     api_token=owner_api_token).delete()
    assert_response_bad_request(response)
    print "Success!!!"


def test_011_delete_multiple_wrong_key_ids(pretty_print, cache, mist_core,
                                           owner_api_token):
    response = mist_core.delete_keys(key_ids=['bla', 'bla2'],
                                     api_token=owner_api_token).delete()
    assert_response_not_found(response)
    print "Success!!!"


def test_012_delete_multiple_keys_with_wrong_api_token(pretty_print,
                                                       mist_core,
                                                       owner_api_token):
    response = mist_core.delete_keys(key_ids=['bla', 'bla2'],
                                     api_token=owner_api_token[:-2]).delete()
    assert_response_unauthorized(response)
    print "Success!!!"


#############################################################################
# Scenarios
#############################################################################


@pytest.mark.incremental
class TestSimpleUserKeyCycle:
    def test_add_key(self, pretty_print, cache, mist_core, owner_api_token,
                     private_key):
        response = mist_core.list_keys(api_token=owner_api_token).get()
        assert_response_ok(response)
        keys_list = json.loads(response.content)
        cache.set('keys_tests/simple_key_name', get_random_key_id(keys_list))
        response = mist_core.add_key(
            name=cache.get('keys_tests/simple_key_name', ''),
            private=private_key,
            api_token=owner_api_token).put()
        assert_response_ok(response)
        response = mist_core.list_keys(api_token=owner_api_token).get()
        assert_response_ok(response)
        script = get_keys_with_id(cache.get('keys_tests/simple_key_name', ''),
                                  json.loads(response.content))
        assert_list_not_empty(script,
                              "Key was added through the api but is not "
                              "visible in the list of keys")

        cache.set('keys_tests/simple_key_id', script[0]['id'])
        print "Success!!!"

    def test_add_key_with_duplicate_id(self, pretty_print, cache, mist_core,
                                       owner_api_token, private_key):
        response = mist_core.add_key(
            name=cache.get('keys_tests/simple_key_name', ''),
            private=private_key,
            api_token=owner_api_token).put()
        assert_response_conflict(response)
        print "Success!!!"

    def test_edit_key(self, pretty_print, cache, mist_core, owner_api_token):
        response = mist_core.list_keys(api_token=owner_api_token).get()
        assert_response_ok(response)
        new_key_name = get_random_key_id(json.loads(response.content))
        response = mist_core.edit_key(
            id=cache.get('keys_tests/simple_key_id', ''),
            new_name=new_key_name,
            api_token=owner_api_token).put()
        assert_response_ok(response)
        response = mist_core.list_keys(api_token=owner_api_token).get()
        assert_response_ok(response)
        script = get_keys_with_id(new_key_name,
                                  json.loads(response.content))
        assert_list_not_empty(script,
                              "Key was added through the api but is not "
                              "visible in the list of keys")
        cache.set('keys_tests/simple_key_name', new_key_name)
        print "Success!!!"

    def test_edit_key_with_no_new_id(self, pretty_print, cache, mist_core,
                                     owner_api_token):
        response = mist_core.edit_key(
            id=cache.get('keys_tests/simple_key_id', ''),
            new_name='',
            api_token=owner_api_token).put()
        assert_response_bad_request(response)
        print "Success!!!"

    def test_edit_key_with_same_id(self, pretty_print, cache, mist_core,
                                   owner_api_token):
        key_id = cache.get('keys_tests/simple_key_id', '')
        key_name = cache.get('keys_tests/simple_key_name', '')
        response = mist_core.edit_key(id=key_id,
                                      new_name=key_name,
                                      api_token=owner_api_token).put()
        assert_response_ok(response)
        print "Success!!!"

    def test_get_private_key(self, pretty_print, cache, mist_core,
                             owner_api_token, private_key):
        response = mist_core.get_private_key(
            cache.get('keys_tests/simple_key_id', ''),
            api_token=owner_api_token).get()
        assert_response_ok(response)
        assert_equal(private_key, json.loads(response.content),
                     response.content)
        print "Success!!!"

    def test_get_public_key(self, pretty_print, cache, mist_core,
                            owner_api_token, public_key):
        response = mist_core.get_public_key(
            cache.get('keys_tests/simple_key_id', ''),
            api_token=owner_api_token).get()
        assert_response_ok(response)
        assert_equal(public_key, json.loads(response.content), response.content)
        print "Success!!!"

    def test_add_second_key_and_set_default(self, pretty_print, cache,
                                            mist_core, owner_api_token,
                                            private_key):
        response = mist_core.list_keys(api_token=owner_api_token).get()
        assert_response_ok(response)
        keys_list = json.loads(response.content)
        cache.set('keys_tests/other_key_name', get_random_key_id(keys_list))
        response = mist_core.add_key(
            name=cache.get('keys_tests/other_key_name', ''),
            private=private_key,
            api_token=owner_api_token).put()
        assert_response_ok(response)
        response = mist_core.list_keys(api_token=owner_api_token).get()
        assert_response_ok(response)
        script = get_keys_with_id(cache.get('keys_tests/other_key_name', ''),
                                  json.loads(response.content))
        assert_list_not_empty(script,
                              "Key was added through the api but is not "
                              "visible in the list of keys")

        cache.set('keys_tests/other_key_id', script[0]['id'])
        other_key_id = cache.get('keys_tests/other_key_id', '')
        response = mist_core.set_default_key(
            key_id=other_key_id,
            api_token=owner_api_token).post()
        assert_response_ok(response)
        response = mist_core.list_keys(api_token=owner_api_token).get()
        assert_response_ok(response)
        script = get_keys_with_id(cache.get('keys_tests/other_key_name', ''),
                                  json.loads(response.content))
        assert_list_not_empty(script,
                              "Key was added through the api but is not "
                              "visible in the list of keys")
        assert script[0]['isDefault'], 'Key is not default'
        print "Success!!!"

    def test_delete_key(self, pretty_print, cache, mist_core, owner_api_token):
        response = mist_core.delete_key(
            key_id=cache.get('keys_tests/simple_key_id', ''),
            api_token=owner_api_token).delete()
        assert response.status_code == requests.codes.ok, response.content
        response = mist_core.delete_key(
            key_id=cache.get('keys_tests/other_key_id', ''),
            api_token=owner_api_token).delete()
        assert_response_ok(response)
        print "Success!!!"

    def test_redelete_key(self, pretty_print, cache, mist_core,
                          owner_api_token):
        response = mist_core.delete_key(
            key_id=cache.get('keys_tests/other_key_id', '')[:-2],
            api_token=owner_api_token).delete()
        assert_response_not_found(response)
        print "Success!!!"

    def test_delete_multiple_keys(self, pretty_print, mist_core,
                                  owner_api_token, private_key):
        key_ids = []
        # add 3 more keys and then delete them
        for i in range(3):
            response = mist_core.list_keys(api_token=owner_api_token).get()
            assert_response_ok(response)
            new_key_name = get_random_key_id(json.loads(response.content))
            response = mist_core.add_key(name=new_key_name, private=private_key,
                                         api_token=owner_api_token).put()
            assert_response_ok(response)
            response = mist_core.list_keys(api_token=owner_api_token).get()
            assert_response_ok(response)
            script = get_keys_with_id(new_key_name,
                                      json.loads(response.content))
            new_key_id = script[0]['id']
            assert_list_not_empty(script, "Key was added but is not visible in"
                                          " the list of keys")
            key_ids.append(new_key_id)

        key_ids.append('bla')
        key_ids.append('bla2')

        response = mist_core.delete_keys(key_ids=key_ids,
                                         api_token=owner_api_token).delete()
        assert_response_ok(response)
        report = json.loads(response.content)
        for key_id in key_ids:
            if 'bla' not in key_id:
                assert_equal(report.get(key_id, ''), 'deleted', report)
            if 'bla' in key_id:
                assert_equal(report.get(key_id, ''), 'not_found', report)
        print "Success!!!"
