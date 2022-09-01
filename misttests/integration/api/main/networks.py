from misttests.integration.api.helpers import *
from misttests import config
from misttests.config import safe_get_var
import pytest

############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_networks_wrong_cloud_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.list_networks(api_token=owner_api_token,
                                       cloud_id='dummy').get()
    assert_response_not_found(response)
    print("Success!!!")


def test_list_networks_wrong_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.list_networks(api_token='dummy',
                                       cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_list_networks_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.list_networks(api_token='',
                                       cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_list_subnets_wrong_cloud_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.list_subnets(api_token=owner_api_token,
                                      cloud_id='dummy', network_id='dummy').get()
    assert_response_not_found(response)
    print("Success!!!")


def test_list_subnets_wrong_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.list_subnets(api_token='dummy', network_id='dummy',
                                      cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_list_subnets_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.list_networks(api_token='',
                                       cloud_id='dummy').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_create_network_missing_parameter(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.create_network(api_token=owner_api_token,
                                        cloud_id='dummy').post()
    assert_response_bad_request(response)
    print("Success!!!")


def test_create_network_wrong_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.create_network(api_token='dummy',
                                        cloud_id='dummy').post()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_create_network_wrong_cloud_id(pretty_print, mist_api_v1, owner_api_token):
     response = mist_api_v1.create_network(api_token=owner_api_token, network_params={'network': {'cidr': '10.1.0.0/16'}},
                                         cloud_id='dummy').post()
     assert_response_not_found(response)
     print("Success!!!")


def test_create_network_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.create_network(api_token='', cloud_id='dummy').post()
    assert_response_forbidden(response)
    print("Success!!!")


def test_create_subnet_wrong_cloud_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.create_subnet(api_token=owner_api_token,
                                       cloud_id='dummy', network_id='dummy').post()
    assert_response_not_found(response)
    print("Success!!!")


def test_create_subnet_wrong_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.create_subnet(api_token='dummy', network_id='dummy',
                                       cloud_id='dummy').post()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_create_subnet_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.create_subnet(api_token='', network_id='dummy',
                                       cloud_id='dummy').post()
    assert_response_forbidden(response)
    print("Success!!!")


def test_delete_network_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.delete_network(api_token='', network_id='dummy',
                                        cloud_id='dummy').delete()
    assert_response_forbidden(response)
    print("Success!!!")


def test_delete_network_wrong_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.delete_network(api_token='dummy', network_id='dummy',
                                        cloud_id='dummy').delete()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_delete_network_wrong_cloud_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.delete_network(api_token=owner_api_token,
                                       cloud_id='dummy', network_id='dummy').delete()
    assert_response_not_found(response)
    print("Success!!!")


def test_delete_subnet_wrong_api_token(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.delete_subnet(api_token='dummy', network_id='dummy',
                                       cloud_id='dummy', subnet_id='dummy').delete()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_delete_subnet_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.delete_subnet(api_token='', network_id='dummy',
                                       cloud_id='dummy', subnet_id='dummy').delete()
    assert_response_forbidden(response)
    print("Success!!!")


def test_delete_subnet_wrong_cloud_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.delete_subnet(api_token=owner_api_token, network_id='dummy',
                                       cloud_id='dummy', subnet_id='dummy').delete()
    assert_response_not_found(response)
    print("Success!!!")


############################################################################
#                          Functional Testing                              #
############################################################################

@pytest.mark.incremental
class TestNetworksFunctionality:

    def test_create_network_ec2(self, mist_api_v1, cache, owner_api_token, network_valid_cidr):
        response = mist_api_v1.add_cloud(name='AWS', provider= 'ec2', api_token=owner_api_token,
                                       api_key=safe_get_var('clouds/aws', 'apikey', config.CREDENTIALS['EC2']['apikey']),
                                       api_secret=safe_get_var('clouds/aws', 'apisecret', config.CREDENTIALS['EC2']['apisecret']),
                                       region=safe_get_var('clouds/aws', 'region', config.CREDENTIALS['EC2']['region'])).post()
        assert_response_ok(response)
        cache.set('cloud_ids/ec2', response.json()['id'])
        response = mist_api_v1.create_network(api_token=owner_api_token,
                                            network_params={'network': {'cidr': network_valid_cidr}},
                                            cloud_id=cache.get('cloud_ids/ec2', '')).post()
        assert_response_ok(response)

        cache.set('network_ids/ec2', response.json()['id'])

        response = mist_api_v1.list_networks(api_token=owner_api_token,
                                           cloud_id=cache.get('cloud_ids/ec2', '')).get()
        assert_response_ok(response)
        print("Success!!!")

    def test_create_subnet(self, mist_api_v1, cache, owner_api_token, network_valid_cidr, availability_zone):
        response = mist_api_v1.create_subnet(api_token=owner_api_token,
                                           subnet_params={'cidr': network_valid_cidr,
                                                          'availability_zone': availability_zone},
                                           network_id=cache.get('network_ids/ec2', ''),
                                           cloud_id=cache.get('cloud_ids/ec2', '')).post()
        assert_response_ok(response)
        cache.set('subnet_ids/ec2', response.json()['id'])

        response = mist_api_v1.list_subnets(api_token=owner_api_token,
                                          network_id=cache.get('network_ids/ec2', ''),
                                          cloud_id=cache.get('cloud_ids/ec2', '')).get()
        for subnet in response.json():
            if subnet['id'] == cache.get('subnet_ids/ec2', ''):
                print("Success!!!")
                break

            assert False, "Subnet created above is not returned in list_subnets."

    def test_delete_subnet(self, mist_api_v1, cache, owner_api_token):
        response = mist_api_v1.delete_subnet(api_token=owner_api_token,
                                           network_id=cache.get('network_ids/ec2', ''),
                                           subnet_id=cache.get('subnet_ids/ec2', ''),
                                           cloud_id=cache.get('cloud_ids/ec2', '')).delete()
        assert_response_ok(response)

        response = mist_api_v1.list_subnets(api_token=owner_api_token,
                                          network_id=cache.get('network_ids/ec2', ''),
                                          cloud_id=cache.get('cloud_ids/ec2', '')).get()
        assert_response_ok(response)
        assert len(response.json()) == 0, "List subnets returns subnets, although they have been deleted"
        print("Success!!!")

    def test_delete_network(self, mist_api_v1, cache, owner_api_token):
        response = mist_api_v1.delete_network(api_token=owner_api_token,
                                            network_id=cache.get('network_ids/ec2', ''),
                                            cloud_id=cache.get('cloud_ids/ec2', '')).delete()
        assert_response_ok(response)

        response = mist_api_v1.list_networks(api_token=owner_api_token,
                                           cloud_id=cache.get('cloud_ids/ec2', '')).get()
        assert_response_ok(response)

        for network in response.json():
            if network.get('id') == cache.get('subnet_ids/ec2', ''):
                assert False, "Network is still returned in list_networks, although it has been deleted"

        print("Success!!!")
