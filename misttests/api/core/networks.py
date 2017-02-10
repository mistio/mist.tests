from misttests.api.helpers import *


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_networks(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_networks(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print "Success!!!"
