from misttests.api.helpers import *
from misttests import config


############################################################################
#                             Unit Testing                                 #
############################################################################

def test_list_clouds(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_clouds(api_token=owner_api_token).get()
    assert_response_ok(response)
    print "Success!!!"


def test_add_cloud_missing_parameter(pretty_print, mist_core, owner_api_token):
    response = mist_core.add_cloud("Openstack", 'openstack',
                                   api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_add_cloud_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.add_cloud("Openstack", 'openstack',
                                   api_token='00' + owner_api_token[:-2]).post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_add_cloud_no_api_token(pretty_print, mist_core):
    response = mist_core.add_cloud("Openstack", 'openstack').post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_add_cloud_ok(pretty_print, mist_core, owner_api_token):
    response = mist_core.add_cloud('Linode', 'linode', api_token=owner_api_token,
                                   api_key=config.CREDENTIALS['LINODE']['api_key']).post()
    assert_response_ok(response)
    print "Success!!!"


# def test_add_cloud_ok_v2(pretty_print, mist_core, owner_api_token):
#     response = mist_core.add_cloud('Nephoscale', 'nephoscale', api_token=owner_api_token,
#                                    username=config.CREDENTIALS['NEPHOSCALE']['username'],
#                                    password=config.CREDENTIALS['NEPHOSCALE']['password']).post()
#     assert_response_ok(response)
#     print "Success!!!"


def test_rename_cloud_wrong_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.rename_cloud(cloud_id='dummy', new_name='test',
                                      api_token=owner_api_token).put()
    assert_response_not_found(response)
    print "Success!!!"


def test_rename_cloud_no_api_token(pretty_print, mist_core):
    response = mist_core.rename_cloud(cloud_id='dummy', new_name='test').put()
    assert_response_forbidden(response)
    print "Success!!!"


def test_rename_cloud_no_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.rename_cloud(cloud_id='dummy', new_name='test',
                                      api_token='00' + owner_api_token[:-2]).put()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_rename_cloud_missing_parameter(pretty_print, mist_core, owner_api_token):
    response = mist_core.rename_cloud(cloud_id='dummy', new_name='',
                                      api_token=owner_api_token).put()
    assert_response_not_found(response)
    print "Success!!!"


def test_delete_cloud_wrong_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_cloud(cloud_id='dummy',api_token=owner_api_token).delete()
    assert_response_not_found(response)
    print "Success"


def test_delete_cloud_no_api_token(pretty_print, mist_core):
    response = mist_core.delete_cloud(cloud_id='dummy').delete()
    assert_response_forbidden(response)
    print "Success!!!"


def test_delete_cloud_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_cloud(cloud_id='dummy', api_token='00' + owner_api_token[:-2]).delete()
    assert_response_unauthorized(response)
    print "Success!!!"
