from misttests.api.helpers import *
from misttests import config

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_machines_no_api_token(pretty_print, mist_core):
    response = mist_core.list_machines(cloud_id='dummy').get()
    assert_response_forbidden(response)
    print "Success!!!"



# def test_add_cloud_missing_parameter(pretty_print, mist_core, owner_api_token):
#     response = mist_core.add_cloud("Openstack", 'openstack',
#                                    api_token=owner_api_token).post()
#     assert_response_bad_request(response)
#     print "Success!!!"
