from misttests.api.helpers import *


############################################################################
#                             Unit Testing                                 #
############################################################################

def test_list_clouds(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_clouds(api_token=owner_api_token).get()
    assert_response_ok(response)
    print "Success!!!"


def test_list_images(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_images('dummy').get()
    assert_response_ok(response)
