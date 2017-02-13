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


def test_create_network_missing_parameter(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_network(api_token=owner_api_token,
                                        cloud_id='dummy').post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_create_network_wrong_api_token(pretty_print, mist_core):
    response = mist_core.create_network(api_token='dummy',
                                        cloud_id='dummy').post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_create_network_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_network(api_token=owner_api_token, network='Net1',
                                        cloud_id='dummy').post()
    assert_response_not_found(response)
    print "Success!!!"


def test_create_network_no_api_token(pretty_print, mist_core):
    response = mist_core.create_network(api_token='', cloud_id='dummy').post()
    assert_response_forbidden(response)
    print "Success!!!"


# create_subnet_missing_parameter -- isn't 'subnet' or sth required???


def test_create_subnet_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_subnet(api_token=owner_api_token,
                                       cloud_id='dummy', network_id='dummy').post()
    assert_response_not_found(response)
    print "Success!!!"


def test_create_subnet_wrong_api_token(pretty_print, mist_core):
    response = mist_core.create_subnet(api_token='dummy', network_id='dummy',
                                       cloud_id='dummy').post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_create_subnet_no_api_token(pretty_print, mist_core):
    response = mist_core.create_subnet(api_token='', network_id='dummy',
                                       cloud_id='dummy').post()
    assert_response_forbidden(response)
    print "Success!!!"


# delete_network
# delete subnet
