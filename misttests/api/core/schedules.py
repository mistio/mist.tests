from misttests.api.helpers import *


############################################################################
#                             Unit Testing                                 #
############################################################################

# add schedule
# show schedule
# edit schedule
# delete schedule


def test_list_schedules(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_schedules(api_token=owner_api_token).post()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print "Success!!!"
