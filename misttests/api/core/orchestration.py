from misttests.api.helpers import *
from misttests import config

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_clouds(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_clouds(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print "Success!!!"