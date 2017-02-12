import pytest

from misttests.api.helpers import *


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_keys(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_keys(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print "Success!!!"


# # # TODO: check below... csrf=None is ok but csrf='' is not?
# # def test_generate_key_wrong_api_token(pretty_print, mist_core):
# #     response = mist_core.generate_keypair(csrf_token='').post()
# #     assert_response_bad_request(response)
# #     print "Success!!!"


def test_delete_key_wrong_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_key(key_id='dummy',api_token=owner_api_token).delete()
    assert_response_not_found(response)
    print "Success!!!"


def test_delete_key_wrong_api_token(pretty_print, mist_core):
    response = mist_core.delete_key(key_id='dummy',api_token='dummy').delete()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_delete_multiple_keys_wrong_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_keys(key_ids=['dummy','dummy1'], api_token=owner_api_token).delete()
    assert_response_not_found(response)
    print "Success!!!"


def test_delete_multiple_keys_no_ids(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_keys(key_ids=[], api_token=owner_api_token).delete()
    assert_response_bad_request(response)
    print "Success!!!"


def test_delete_multiple_keys_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_keys(key_ids=['dummy','dummy1'], api_token='1234').delete()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_rename_key_wrong_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.edit_key('dummy_id', 'new_name', api_token=owner_api_token).put()
    assert_response_not_found(response)
    print "Success!!!"


def test_rename_key_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.edit_key('dummy_id', 'new_name', api_token=owner_api_token[:-2]).put()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_rename_key_missing_parameter(pretty_print, mist_core, owner_api_token):
    response = mist_core.edit_key('dummy_id', '', api_token=owner_api_token).put()
    assert_response_bad_request(response)
    print "Success!!!"


def test_set_default_key_wrong_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.set_default_key(key_id='dummy',api_token=owner_api_token).post()
    assert_response_not_found(response)
    print "Success!!!"


def test_set_default_key_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.set_default_key(key_id='dummy',api_token='dummy').post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_add_key_no_name_no_private(pretty_print, mist_core,
                                            owner_api_token):
    response = mist_core.add_key(name='', private='',
                                 api_token=owner_api_token).put()
    assert_response_bad_request(response)
    print "Success!!!"


def test_add_key_no_private(pretty_print, cache, mist_core,
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


def test_get_private_key_wrong_id(pretty_print, cache, mist_core,
                                  owner_api_token):
    response = mist_core.get_private_key('bla', api_token=owner_api_token).get()
    assert_response_not_found(response)
    print "Success!!!"


def test_get_public_key_wrong_id(pretty_print, cache, mist_core,
                                 owner_api_token):
    response = mist_core.get_public_key(
        cache.get('keys_tests/key_name', '')[:-2],
        api_token=owner_api_token).get()
    assert_response_not_found(response)
    print "Success!!!"


def test_set_default_key_wrong_id(pretty_print, cache, mist_core,
                                  owner_api_token):
    response = mist_core.set_default_key(
        key_id='bla',
        api_token=owner_api_token).post()
    assert_response_not_found(response)
    print "Success!!!"


############################################################################
#                          Functional Testing                              #
############################################################################


@pytest.mark.incremental
class TestSimpleUserKeyCycle:
    def test_add_key(self, pretty_print, cache, mist_core, owner_api_token,
                     private_key):
        response = mist_core.list_keys(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 0
        response = mist_core.add_key(
            name='TestKey',
            private=private_key,
            api_token=owner_api_token).put()
        assert_response_ok(response)
        cache.set('key_id', response.json()['id'])
        response = mist_core.list_keys(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 1
        print "Success!!!"

    def test_add_key_duplicate_name(self, pretty_print, cache, mist_core,
                                    owner_api_token, private_key):
        response = mist_core.add_key(
            name='TestKey',
            private=private_key,
            api_token=owner_api_token).put()
        assert_response_conflict(response)
        print "Success!!!"

    def test_rename_key(self, pretty_print, cache, mist_core,
                        owner_api_token):
        response = mist_core.edit_key(
                    id=cache.get('key_id', ''),
                    new_name='Key1',
                    api_token=owner_api_token).put()
        assert_response_ok(response)
        response = mist_core.list_keys(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert 'Key1' == response.json()[0]['name'], "Although response was 200, key was not renamed"
        print "Success"

    def test_rename_key_no_name(self, pretty_print, cache, mist_core,
                                owner_api_token):
        response = mist_core.edit_key(
                    id=cache.get('key_id', ''),
                    new_name='',
                    api_token=owner_api_token).put()
        assert_response_bad_request(response)
        response = mist_core.list_keys(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert 'Key1' == response.json()[0]['name']
        print "Success"

    def test_generate_key(self, pretty_print, cache, mist_core, owner_api_token):
        response = mist_core.generate_keypair(api_token=owner_api_token).post()
        assert_response_ok(response)
        if 'public' not in response.json().keys() or 'priv' not in response.json().keys():
            assert False, "Public key was not generated!"
        cache.set('key_priv', response.json()['priv'])
        response = mist_core.add_key(
            name='Key2',
            private=cache.get('key_priv', ''),
            api_token=owner_api_token).put()
        assert_response_ok(response)
        response = mist_core.list_keys(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 2
        print "Success!!!"

    def test_get_private_key(self, pretty_print, private_key, cache, mist_core, owner_api_token):
        response = mist_core.get_private_key(key_id=cache.get('key_id', ''),
                                             api_token=owner_api_token).get()
        assert_response_ok(response)
        assert response.json() == private_key
        print "Success!!!"

    def test_delete_key(self, pretty_print, cache, mist_core, owner_api_token):
        response = mist_core.delete_key(key_id=cache.get('key_id', ''),
                                        api_token=owner_api_token).delete()
        assert_response_ok(response)
        response = mist_core.delete_key(key_id=cache.get('key_id', ''),
                                        api_token=owner_api_token).delete()
        assert_response_not_found(response)
        print "Success"

    def test_set_default_key(self, pretty_print, cache, mist_core, owner_api_token,
                             private_key):
        response = mist_core.add_key(
            name='TestKey',
            private=private_key,
            api_token=owner_api_token).put()
        assert_response_ok(response)
        cache.set('key_id', response.json()['id'])
        assert response.json()['isDefault'] == False, "Key was added as default although it shouldn't be!"
        response = mist_core.list_keys(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 2
        response = mist_core.set_default_key(
            key_id=cache.get('key_id', ''),
            api_token=owner_api_token).post()
        assert_response_ok(response)
        response = mist_core.list_keys(api_token=owner_api_token).get()
        for key in response.json():
            if key['id'] == cache.get('key_id', ''):
                assert key['isDefault'], "Key is not default although response was 200"
            else:
                assert key['isDefault'] == False, "More than one keys are set as default!"
        print "Success!!!"

        # delete keys

#     def test_delete_multiple_keys(self, pretty_print, mist_core,
#                                   owner_api_token, private_key):
#         key_ids = []
#         # add 3 more keys and then delete them
#         for i in range(3):
#             response = mist_core.list_keys(api_token=owner_api_token).get()
#             assert_response_ok(response)
#             new_key_name = get_random_key_id(json.loads(response.content))
#             response = mist_core.add_key(name=new_key_name, private=private_key,
#                                          api_token=owner_api_token).put()
#             assert_response_ok(response)
#             response = mist_core.list_keys(api_token=owner_api_token).get()
#             assert_response_ok(response)
#             script = get_keys_with_id(new_key_name,
#                                       json.loads(response.content))
#             new_key_id = script[0]['id']
#             assert_list_not_empty(script, "Key was added but is not visible in"
#                                           " the list of keys")
#             key_ids.append(new_key_id)
#
#         key_ids.append('bla')
#         key_ids.append('bla2')
#
#         response = mist_core.delete_keys(key_ids=key_ids,
#                                          api_token=owner_api_token).delete()
#         assert_response_ok(response)
#         report = json.loads(response.content)
#         for key_id in key_ids:
#             if 'bla' not in key_id:
#                 assert_equal(report.get(key_id, ''), 'deleted', report)
#             if 'bla' in key_id:
#                 assert_equal(report.get(key_id, ''), 'not_found', report)
#         print "Success!!!"
