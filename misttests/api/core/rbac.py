from misttests.api.helpers import *

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_create_org_missing_parameter(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_org(api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"
