import requests

from tests import config

from tests.api.utils import *


def test_001_simple_api_token_test(pretty_print, mist_core,
                                   user_with_api_token):
    from mist.core.auth.models import ApiToken
    mist_api_token_string = "mist_1 " + config.EMAIL + \
                            ":" + user_with_api_token.mist_api_token
    print "\n>>>  Pinging core with old api token"
    response = mist_core.ping(mist_api_token_string).post()
    assert_response_ok(response)
    token = ApiToken.objects.get(token=user_with_api_token.mist_api_token)
    assert_equal(token.get_user().get_id(),
                 user_with_api_token.get_id(),
                 'ApiToken user is different than the actual user')
    response = mist_core.ping(mist_api_token_string).post()
    assert response.status_code == requests.codes.ok
    print "Success!!!!"


def test_002_short_api_token_test(pretty_print, mist_core,
                                  user_with_short_api_token):
    from mist.core.auth.models import ApiToken
    mist_api_token_string = "mist_1 " + config.EMAIL + \
                            ":" + user_with_short_api_token.mist_api_token
    print "\n>>>  Pinging core with short old api token"
    response = mist_core.ping(mist_api_token_string).post()
    assert_response_ok(response)
    short_token = '0' + user_with_short_api_token.mist_api_token
    token = ApiToken.objects.get(token=short_token)
    assert_equal(token.get_user().get_id(),
                 user_with_short_api_token.get_id(),
                 'ApiToken user is different than the actual user')
    print "Success!!!!"
