import requests
import misttests.api.helpers
from conftest import mist_io, cloud
from misttests.api.core.conftest import owner_api_token


def test_001_create_network(pretty_print, mist_io, owner_api_token, cloud, network_test_cleanup):
    # Creating a network
    network_params = {'network': {'name': 'api_test_network', 'description': 'A Test Network', 'cidr': '10.1.0.0/16'}}
    response = mist_io.create_network(cloud_id=cloud.id,
                                      network_params=network_params,
                                      api_token=owner_api_token).post()
    # Testing the API response
    assert response.status_code == requests.codes.ok

    response_content = response.json()
    misttests.api.helpers.assert_is_instance(response_content, dict)

    assert response_content['name'] == 'api_test_network'
    assert response_content['description'] == 'A Test Network'


def test_002_create_subnet(pretty_print, mist_io, owner_api_token, cloud, network_test_cleanup):
    # Creating a network
    network_params = {'network': {'name': 'api_test_network', 'description': 'A Test Network', 'cidr': '10.1.0.0/16'}}
    network_response = mist_io.create_network(cloud_id=cloud.id,
                                              network_params=network_params,
                                              api_token=owner_api_token).post()
    assert network_response.status_code == requests.codes.ok

    # Creating a subnet
    subnet_params = {'subnet': {'name': 'api_test_subnet', 'cidr': '10.1.1.0/24', 'description': 'A Test Subnet'}}

    if cloud.ctl.provider == 'ec2':
        subnet_params['subnet']['availability_zone'] = 'ap-northeast-1a'

    response = mist_io.create_subnet(cloud_id=cloud.id,
                                     subnet_params=subnet_params,
                                     network_id=network_response.json()['id'],
                                     api_token=owner_api_token).post()

    # Testing the API response
    assert response.status_code == requests.codes.ok

    response_content = response.json()
    misttests.api.helpers.assert_is_instance(response_content, dict)

    assert response_content['name'] == 'api_test_subnet'
    assert response_content['description'] == 'A Test Subnet'


def test_003_list_networks(pretty_print, mist_io, owner_api_token, cloud):
    # Getting a network listing
    response = mist_io.list_networks(cloud.id, api_token=owner_api_token).get()
    assert response.status_code == requests.codes.ok

    # Verifying that the API response has the correct structure
    response_content = response.json()
    misttests.api.helpers.assert_is_instance(response_content, dict)
    for base_key in ['public', 'private', 'routers']:
        assert base_key in response_content

    network_dict_required_keys = ['name', 'id', 'description', 'network_id', 'cloud', 'subnets']

    for network in zip(response_content['public'], response_content['private']):
        for required_key in network_dict_required_keys:
            assert network.get(required_key)
            misttests.api.helpers.assert_is_instance(network['subnets'], list)


def test_004_list_subnets(pretty_print, mist_io, owner_api_token, cloud):
    # Creating a network
    network_params = {'network': {'name': 'api_test_network', 'description': 'A Test Network', 'cidr': '10.1.0.0/16'}}
    network_response = mist_io.create_network(cloud_id=cloud.id,
                                              network_params=network_params,
                                              api_token=owner_api_token).post()
    assert network_response.status_code == requests.codes.ok

    # Creating a subnet
    subnet_params = {'subnet': {'name': 'api_test_subnet', 'cidr': '10.1.1.0/24', 'description': 'A Test Subnet'}}

    if cloud.ctl.provider == 'ec2':
        subnet_params['subnet']['availability_zone'] = 'ap-northeast-1a'

    subnet_response = mist_io.create_subnet(cloud_id=cloud.id,
                                            subnet_params=subnet_params,
                                            network_id=network_response.json()['id'],
                                            api_token=owner_api_token).post()

    assert subnet_response.status_code == requests.codes.ok

    # Getting a subnet listing
    subnet_listing = mist_io.list_subnets(cloud.id,
                                          api_token=owner_api_token,
                                          network_id=network_response.json()['id']).get()
    assert subnet_listing.status_code == requests.codes.ok

    # Verifying that the API response has the correct structure
    subnets = subnet_listing.json()
    misttests.api.helpers.assert_is_instance(subnets, list)

    subnet_dict_required_keys = ['name', 'id', 'description', 'subnet_id', 'cloud', 'cidr', 'network']

    for subnet in subnets:
        for required_key in subnet_dict_required_keys:
            assert subnet.get(required_key)


def test_005_delete_network(pretty_print, mist_io, owner_api_token, cloud, network_test_cleanup):
    # Creating a network
    network_params = {'network': {'name': 'api_test_network', 'description': 'A Test Network', 'cidr': '10.1.0.0/16'}}
    network_response = mist_io.create_network(cloud_id=cloud.id,
                                              network_params=network_params,
                                              api_token=owner_api_token).post()
    assert network_response.status_code == requests.codes.ok

    network_db_id = network_response.json()['id']

    # Deleting the network and testing the response
    delete_response = mist_io.delete_network(cloud_id=cloud.id,
                                             network_id=network_db_id,
                                             api_token=owner_api_token).delete()
    assert delete_response.status_code == requests.codes.ok

    # Getting a network listing
    network_listing_response = mist_io.list_networks(cloud.id, api_token=owner_api_token).get()
    assert network_listing_response.status_code == requests.codes.ok

    # Verifying that the deleted network is no longer present in the listing
    networks = network_listing_response.json()
    api_network_ids = [network['id'] for network in zip(networks['public'], networks['private'])]
    assert network_db_id not in api_network_ids


def test_006_delete_subnet(pretty_print, mist_io, owner_api_token, cloud, network_test_cleanup):
    # Creating a network
    network_params = {'network': {'name': 'api_test_network', 'description': 'A Test Network', 'cidr': '10.1.0.0/16'}}
    network_response = mist_io.create_network(cloud_id=cloud.id,
                                              network_params=network_params,
                                              api_token=owner_api_token).post()
    assert network_response.status_code == requests.codes.ok

    network_db_id = network_response.json()['id']

    # Creating a subnet
    subnet_params = {'subnet': {'name': 'api_test_subnet', 'cidr': '10.1.1.0/24', 'description': 'A Test Subnet'}}

    if cloud.ctl.provider == 'ec2':
        subnet_params['subnet']['availability_zone'] = 'ap-northeast-1a'

    subnet_response = mist_io.create_subnet(cloud_id=cloud.id,
                                            subnet_params=subnet_params,
                                            network_id=network_response.json()['id'],
                                            api_token=owner_api_token).post()

    assert subnet_response.status_code == requests.codes.ok

    subnet_db_id = subnet_response.json()['id']

    # Deleting the subnet and testing the response
    delete_response = mist_io.delete_subnet(cloud_id=cloud.id,
                                            network_id=network_db_id,
                                            subnet_id=subnet_response.json()['id'],
                                            api_token=owner_api_token).delete()
    assert delete_response.status_code == requests.codes.ok

    # Getting a subnet listing
    subnet_listing_response = mist_io.list_subnets(cloud.id,
                                                   api_token=owner_api_token,
                                                   network_id=network_response.json()['id']).get()
    assert subnet_listing_response.status_code == requests.codes.ok

    # Verifying that the deleted subnet is no longer present in the listing
    subnets = subnet_listing_response.json()
    api_subnet_ids = [subnet['id'] for subnet in subnets]
    assert subnet_db_id not in api_subnet_ids
