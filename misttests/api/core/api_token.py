from misttests.api.utils import assert_response_bad_request
from misttests.api.utils import assert_response_unauthorized


def test_get_api_token_empty_fields(pretty_print, mist_core):
    print "\n>>>  POSTing /auth and /tokens to get a token with empty creds:"
    response = mist_core.check_auth(email='', password='').post()
    assert_response_bad_request(response)
    response = mist_core.create_token(email='', password='').post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_get_api_token_wrong_ttl(pretty_print, mist_core, email,
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


def test_su(pretty_print, cache, mist_core):
    print "\n>>>  POSTing /su with api token. Should get forbidden error"
    response = mist_core.su(
        api_token=cache.get('api_token_test/api_token', '')).get()
    assert_response_unauthorized(response)
    print "Success!!!!"
