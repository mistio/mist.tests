from misttests.api.utils import *


def test_001_get_api_token_with_empty_fields(pretty_print, mist_core):
    print "\n>>>  POSTing /auth and /tokens to get a token with empty creds:"
    response = mist_core.check_auth(email='', password='').post()
    assert_response_bad_request(response)
    response = mist_core.create_token(email='', password='').post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_002_get_api_token_with_empty_password(pretty_print, mist_core, email):
    print "\n>>>  POSTing /auth and /tokens to get a token with no password:"
    response = mist_core.check_auth(email=email, password='').post()
    assert_response_bad_request(response)
    response = mist_core.create_token(email=email, password='').post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_003_get_api_token_with_wrong_ttl(pretty_print, mist_core, email,
                                          password1):
    print "\n>>>  POSTing /auth and /tokens to get a token with good creds" \
          " but wrong ttl:"
    response = mist_core.check_auth(email=email,
                                    password=password1,
                                    ttl='bla').post()
    assert_response_bad_request(response)
    response = mist_core.check_auth(email=email,
                                    password=password1,
                                    ttl='10a').post()
    assert_response_bad_request(response)
    response = mist_core.create_token(email=email,
                                      password=password1,
                                      ttl='bla').post()
    assert_response_bad_request(response)
    response = mist_core.create_token(email=email,
                                      password=password1,
                                      ttl='10a').post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_004_get_api_token(pretty_print, cache, mist_core, email, password1):
    print "\n>>>  POSTing /tokens to get a token with correct creds"
    response = mist_core.create_token(email=email, password=password1).post()
    assert_response_ok(response)
    assert_is_not_none(response.json().get('token', None),
                       "Did not get an api token back in the response")
    assert_is_not_none(response.json().get('name', None),
                       "Did not get the api token name in the response")
    cache.set('api_token_test/api_token', response.json().get('token', None))
    cache.set('api_token_test/api_token_name',
              response.json().get('name', None))
    cache.set('api_token_test/api_token_id', response.json().get('id', None))
    print "Success!!!!"


# def test_005_confirm_api_token(pretty_print, cache, mist_core, email):
#     print "\n>>>  POSTing /check_token again to see if my token is recognized:"
#     response = mist_core.check_token(
#         api_token=cache.get('api_token_test/api_token',
#                             '')).post()
#     assert_response_ok(response)
#     assert_equal(email, response.json().get('hello', None), response.content)
#     print "Success!!!!"


# def test_006_confirm_same_name_token_exception(pretty_print, cache, mist_core,
#                                                email, password1):
#     print "\n>>>  POSTing /tokens to see that there cannot be a second " \
#           "token with same name as the one i got:"
#     response = mist_core.create_token(email, password1,
#                                       new_api_token_name=
#                                       cache.get('api_token_test/api_token_name',
#                                                 '')).post()
#     assert_response_conflict(response)
#     print "Success!!!!"


# def test_007_list_api_tokens(pretty_print, cache, mist_core):
#     print "\n>>>  GETing /tokens to get a list of all ApiTokens"
#     response = mist_core.list_tokens(
#         cache.get('api_token_test/api_token', '')).get()
#     assert_response_ok(response)
#     print "Got a list of tokens: \n"
#     my_token = None
#     pprint.pprint(response.json(), indent=3, stream=sys.stdout)
#     tokens = json.loads(response.content)
#     for token in tokens:
#         if token['name'] == cache.get('api_token_test/api_token_name', ''):
#             my_token = token
#             break
#     assert_is_not_none(my_token,
#                        "Token was not present in the list of tokens returned")
#     print "Success!!!!"
#
#
# def test_008_create_short_lived_api_token(pretty_print, cache, mist_core, email,
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


def test_008_test_su(pretty_print, cache, mist_core):
    print "\n>>>  POSTing /su with api token. Should get forbidden error"
    response = mist_core.su(
        api_token=cache.get('api_token_test/api_token', '')).get()
    assert_response_unauthorized(response)
    print "Success!!!!"


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
#
#
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
#
#
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
#
#
# def test_013_test_list_supported_providers_with_wrong_token(pretty_print,
#                                                             cache, mist_core):
#     print "\n>>>  GETing /providers for a list of supported providers with" \
#           " wrong token"
#     response = mist_core.supported_providers(
#         api_token=cache.get('api_token_test/api_token', '')[2:]).get()
#     assert_response_ok(response)
#     print "Success!!!!"
#
#
# def test_014_revoke_api_token(pretty_print, cache, mist_core):
#     print "\n>>>  DELETEing /tokens for original ApiToken i got"
#     response = mist_core.revoke_token(
#         api_token=cache.get('api_token_test/api_token', ''),
#         api_token_id=cache.get('api_token_test/api_token_id', '')).delete()
#     assert_response_ok(response)
#     print "Success!!!!"
#
#
# def test_016_fail_list_tokens_with_revoked_api_token(pretty_print, cache,
#                                                      mist_core):
#     print "\n>>>  GETing /tokens to make sure that i fail"
#     response = mist_core.list_tokens(
#         api_token=cache.get('api_token_test/api_token', '')).get()
#     assert_response_unauthorized(response)
#     print "Success!!!!"
#
#
# def test_017_fail_revoke_token_with_revoked_api_token(pretty_print, cache,
#                                                       mist_core):
#     print "\n>>>  DELETEing /tokens for revoked token"
#     response = mist_core.revoke_token(
#         api_token=cache.get('api_token_test/api_token', ''),
#         api_token_id=cache.get('api_token_test/api_token_id', '')).delete()
#
#     assert_response_unauthorized(response)
#     print "Success!!!!"
#
#
# def test_018_fail_revoke_token_with_no_api_token(pretty_print, cache,
#                                                  mist_core):
#     print "\n>>>  DELETEing /tokens for revoked token"
#     response = mist_core.revoke_token(
#         api_token=cache.get('api_token_test/api_token', ''),
#         api_token_id=cache.get('api_token_test/api_token_id', '')).delete()
#
#     assert_response_unauthorized(response)
#     print "Success!!!!"
