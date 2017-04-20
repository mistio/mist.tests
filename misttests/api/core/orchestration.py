from misttests.api.helpers import *
from misttests import config

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_templates(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_templates(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print "Success!!!"


def test_add_template_missing_parameter(pretty_print, mist_core, owner_api_token):
    response = mist_core.add_template(name='', location_type='github',
                                      api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"

#
# def test_add_cloud_wrong_api_token(pretty_print, mist_core, owner_api_token):
#     response = mist_core.add_cloud("Openstack", 'openstack',
#                                    api_token='00' + owner_api_token[:-2]).post()
#     assert_response_unauthorized(response)
#     print "Success!!!"
#
#
# def test_add_cloud_no_api_token(pretty_print, mist_core):
#     response = mist_core.add_cloud("Openstack", 'openstack').post()
#     assert_response_forbidden(response)
#     print "Success!!!"
#
#
# def test_add_cloud_ok(pretty_print, mist_core, owner_api_token, name='Linode'):
#     response = mist_core.add_cloud(name, 'linode', api_token=owner_api_token,
#                                    api_key=config.CREDENTIALS['LINODE']['api_key']).post()
#     assert_response_ok(response)
#     print "Success!!!"
