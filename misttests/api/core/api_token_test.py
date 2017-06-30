from misttests.api.helpers import *


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_create_api_token_empty_password(pretty_print, mist_core, email, owner_api_token):
    response = mist_core.create_token(email=email, password='', api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_create_api_token_wrong_password(pretty_print, mist_core, email, owner_api_token):
    response = mist_core.create_token(email=email, password='wrong',
                                      api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_create_api_token_wrong_org_id(pretty_print, mist_core, email,
                                       password1):
    response = mist_core.create_token(email=email, password=password1,
                                      org_id='bla').post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_008_test_su(pretty_print, cache, mist_core):
    response = mist_core.su(
        api_token=cache.get('api_token_test/api_token', '')).get()
    assert_response_unauthorized(response)
    print "Success!!!!"


# def test_create_api_token_ttl_ok(pretty_print, cache, mist_core, email, password1, owner_api_token):
#     response = mist_core.create_token(email=email, password=password1,
#                                       api_token=owner_api_token, ttl=300).post()
#     assert_response_ok(response)
#     assert_is_not_none(response.json().get('token', None),
#                        "Did not get an api token back in the response")
#     assert_is_not_none(response.json().get('name', None),
#                        "Did not get the api token name in the response")
#     response = mist_core.create_token(email=email, password=password1, ttl=300, new_api_token_name='testToken').post()
#     assert_response_ok(response)
#     assert_is_not_none(response.json().get('token', None),
#                        "Did not get an api token back in the response")
#     assert_is_not_none(response.json().get('name', None),
#                        "Did not get the api token name in the response")
#
#     print "Success!!!!"


############################################################################
#                         Functional Testing                               #
############################################################################


# @pytest.mark.incremental
# class TestApiTokenFunctionality:
#
#     def test_create_api_token_ok(pretty_print, cache, mist_core, email, password,
#                                  owner_api_token):
#         response = mist_core.create_token(email=email, password=password,api_token=owner_api_token).post()
#         assert_response_ok(response)
#         assert_is_not_none(response.json().get('token', None),
#                            "Did not get an api token back in the response")
#         assert_is_not_none(response.json().get('name', None),
#                            "Did not get the api token name in the response")
#         cache.set('api_token_test/api_token', response.json().get('token', None))
#         cache.set('api_token_test/api_token_name',
#                   response.json().get('name', None))
#         cache.set('api_token_test/api_token_id', response.json().get('id', None))
#         print "Success!!!!"

# def test_confirm_api_token(pretty_print, cache, mist_core, email):
#     script_data = {'location_type':'inline','exec_type':'executable', 'name': 'Script1'}
#     response = mist_core.add_script(api_token=cache.get('api_token_test/api_token', ''),
#                                     script_data=script_data, script=bash_script).post()
#     assert_response_ok(response)
#
#     response = mist_core.check_token(
#         api_token=cache.get('api_token_test/api_token',
#                             '')).post()
#     assert_response_ok(response)
#     assert_equal(email, response.json().get('hello', None), response.content)
#     print "Success!!!!"


# def test_005_confirm_same_name_token_exception(pretty_print, cache, mist_core,
#                                                   email, password1):
#        print "\n>>>  POSTing /tokens to see that there cannot be a second " \
#              "token with same name as the one i got:"
#        response = mist_core.create_token(email, password1,
#                                          new_api_token_name=
#                                          cache.get('api_token_test/api_token_name',
#                                                    '')).post()
#        assert_response_conflict(response)
#        print "Success!!!!"


# def test_006_create_short_lived_api_token(pretty_print, cache, mist_core, email,
#                                           password1):
#     print "\n>>>  POSTing /tokens to create another short lived ApiToken"
#     response = mist_core.create_token(email=email,
#                                       password=password1,
#                                       api_token=cache.get(
#                                           'api_token_test/api_token', ''),
#                                       ttl=10).post()
#     assert_response_ok(response)
#     api_token = response.json().get('token', None)
#     api_token_id = response.json().get('id', None)
#     assert_is_not_none(response.json().get('token', None))
#     assert_is_not_none(response.json().get('id', None))
#     assert_is_not_none(response.json().get('name', None))
#     print "\n>>>  POSTing /check_token to see that new token works fine"
#     response = mist_core.check_token(api_token=api_token).post()
#     assert_response_ok(response)
#     assert_equal(email, response.json().get('hello'))
#     print "\n>>>  Sleeping for 10 secs"
#     for _ in range(10):
#         sleep(1)
#         sys.stdout.write('.')
#         sys.stdout.flush()
#     print "\n>>>  POSTing /check_token to see that new token is invalid"
#     response = mist_core.check_token(api_token=api_token).post()
#     assert_response_unauthorized(response)
#     print "\n>>>  DELETEing /tokens for second ApiToken i got"
#     response = mist_core.revoke_token(
#         api_token=cache.get('api_token_test/api_token', ''),
#         api_token_id=api_token_id).delete()
#     assert_response_ok(response)
#     print "Success!!!!"



# def test_007_check_auth_with_wrong_token(pretty_print, cache, mist_core, email,
#                                          password1):
#     print "\n>>>  POSTing /tokens with wrong token but correct creds"
#     response = mist_core.create_token(email=email,
#                                       password=password1,
#                                       ttl=10,
#                                       api_token=cache.get(
#                                           'api_token_test/api_token', '')[
#                                                 :-2]).post()
#     assert_response_ok(response)
#     print "Success!!!!"


# def test_009_test_api_token_creation_for_oauth_user(mist_core,
#                                                     user_with_empty_password,
#                                                     email,
#                                                     password1):
#     print "\n>>>  POSTing /tokens with password. Should fail"
#     response = mist_core.create_token(email=email,
#                                       password=password1,
#                                       ttl=10).post()
#     assert_response_bad_request(response)
#     print "Success!!!!"



# def test_010_test_api_token_creation_for_oauth_user2(mist_core,
#                                                      user_with_empty_password,
#                                                      email,
#                                                      password1):
#     print "\n>>>  POSTing /tokens with no password and no api token. Should " \
#           "fail"
#     response = mist_core.create_token(email=email,
#                                       password='',
#                                       ttl=10).post()
#     assert_response_bad_request(response)
#     print "Success!!!!"


# def test_011_test_api_token_creation_for_oauth_user3(pretty_print, cache,
#                                                      mist_core,
#                                                      user_with_empty_password,
#                                                      email):
#     print "\n>>>  POSTing /tokens with no password and api token. Should fail"
#     response = mist_core.create_token(email=email,
#                                       password='',
#                                       api_token=cache.get(
#                                           'api_token_test/api_token', ''),
#                                       ttl=10).post()
#     assert_response_bad_request(response)
#     print "Success!!!!"


# def test_012_test_list_supported_providers(pretty_print, cache, mist_core):
#     print "\n>>>  GETing /providers for a list of supported providers"
#     response = mist_core.supported_providers(
#         api_token=cache.get('api_token_test/api_token', '')).get()
#     assert_response_ok(response)
#     print "Success!!!!"



# def test_013_test_list_supported_providers_with_wrong_token(pretty_print,
#                                                             cache, mist_core):
#     print "\n>>>  GETing /providers for a list of supported providers with" \
#           " wrong token"
#     response = mist_core.supported_providers(
#         api_token=cache.get('api_token_test/api_token', '')[2:]).get()
#     assert_response_ok(response)
#     print "Success!!!!"


# def test_014_revoke_api_token(pretty_print, cache, mist_core):
#     print "\n>>>  DELETEing /tokens for original ApiToken i got"
#     response = mist_core.revoke_token(
#         api_token=cache.get('api_token_test/api_token', ''),
#         api_token_id=cache.get('api_token_test/api_token_id', '')).delete()
#     assert_response_ok(response)
#     print "Success!!!!"


# def test_016_fail_list_tokens_with_revoked_api_token(pretty_print, cache,
#                                                      mist_core):
#     print "\n>>>  GETing /tokens to make sure that i fail"
#     response = mist_core.list_tokens(
#         api_token=cache.get('api_token_test/api_token', '')).get()
#     assert_response_unauthorized(response)
#     print "Success!!!!"



# def test_017_fail_revoke_token_with_revoked_api_token(pretty_print, cache,
#                                                       mist_core):
#     print "\n>>>  DELETEing /tokens for revoked token"
#     response = mist_core.revoke_token(
#         api_token=cache.get('api_token_test/api_token', ''),
#         api_token_id=cache.get('api_token_test/api_token_id', '')).delete()
#
#     assert_response_unauthorized(response)
#     print "Success!!!!"


# def test_018_fail_revoke_token_with_no_api_token(pretty_print, cache,
#                                                  mist_core):
#     print "\n>>>  DELETEing /tokens for revoked token"
#     response = mist_core.revoke_token(
#         api_token=cache.get('api_token_test/api_token', ''),
#         api_token_id=cache.get('api_token_test/api_token_id', '')).delete()
#
#     assert_response_unauthorized(response)
#     print "Success!!!!"
