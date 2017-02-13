from misttests.api.helpers import *


#     configurator.add_route('api_v1_network','/api/v1/clouds/{cloud}/networks/{network}')


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_networks_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_networks(api_token=owner_api_token,
                                       cloud_id='dummy').get()
    assert_response_not_found(response)
    print "Success!!!"


def test_list_networks_wrong_api_token(pretty_print, mist_core):
    response = mist_core.list_networks(api_token='dummy',
                                       cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


# check - it should get forbidden?
def test_list_networks_no_api_token(pretty_print, mist_core):
    response = mist_core.list_networks(api_token='',
                                       cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_list_subnets_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_subnets(api_token=owner_api_token,
                                      cloud_id='dummy', network_id='dummy').get()
    assert_response_not_found(response)
    print "Success!!!"


def test_list_subnets_wrong_api_token(pretty_print, mist_core):
    response = mist_core.list_subnets(api_token='dummy', network_id='dummy',
                                      cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


# check - it should get forbidden?
def test_list_subnets_no_api_token(pretty_print, mist_core):
    response = mist_core.list_networks(api_token='',
                                       cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


# create_network
# create_subnet
# delete_network
# delete subnet
