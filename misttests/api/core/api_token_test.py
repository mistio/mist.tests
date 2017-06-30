from misttests.api.helpers import *

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

# def test_013_test_list_supported_providers_with_wrong_token(pretty_print,
#                                                             cache, mist_core):
#     print "\n>>>  GETing /providers for a list of supported providers with" \
#           " wrong token"
#     response = mist_core.supported_providers(
#         api_token=cache.get('api_token_test/api_token', '')[2:]).get()
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
