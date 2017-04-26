from misttests.api.helpers import *
from misttests import config

import pytest

############################################################################
#                         Functional Testing                               #
############################################################################


@pytest.mark.incremental
class TestLibcloudFunctionality:

    def test_list_machines_docker(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.add_cloud(title='Docker', provider= 'docker', api_token=owner_api_token,
                                       docker_host=config.CREDENTIALS['DOCKER']['host'],
                                       docker_port=config.CREDENTIALS['DOCKER']['port'],
                                       authentication=config.CREDENTIALS['DOCKER']['authentication'],
                                       ca_cert_file=config.CREDENTIALS['DOCKER']['ca'],
                                       key_file=config.CREDENTIALS['DOCKER']['key'],
                                       cert_file=config.CREDENTIALS['DOCKER']['cert']).post()
        assert_response_ok(response)
        cache.set('docker_cloud_id', response.json()['id'])
        response = mist_core.list_machines(cloud_id=cache.get('docker_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List Docker machines did not return any machines"
        print "Success!!!"


    def test_list_machines_linode(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.add_cloud(title='Linode', provider= 'linode', api_token=owner_api_token,
                                       api_key=config.CREDENTIALS['LINODE']['api_key']).post()
        assert_response_ok(response)
        cache.set('linode_cloud_id', response.json()['id'])
        response = mist_core.list_machines(cloud_id=cache.get('linode_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) >= 0, "List Linode machines did not return a proper result"
        print "Success!!!"


    def test_list_machines_aws(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.add_cloud(title='AWS', provider= 'ec2', api_token=owner_api_token,
                                       api_key=config.CREDENTIALS['AWS']['api_key'],
                                       api_secret=config.CREDENTIALS['AWS']['api_secret'],
                                       region=config.CREDENTIALS['AWS']['region']).post()
        assert_response_ok(response)
        cache.set('aws_cloud_id', response.json()['id'])
        response = mist_core.list_machines(cloud_id=cache.get('aws_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) >= 0, "List AWS machines did not return a proper result"
        print "Success!!!"


    def test_list_machines_digitalocean(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.add_cloud(title='Digital Ocean', provider= 'digitalocean', api_token=owner_api_token,
                                       api_key=config.CREDENTIALS['DIGITALOCEAN']['token']).post()
        assert_response_ok(response)
        cache.set('digitalocean_cloud_id', response.json()['id'])
        response = mist_core.list_machines(cloud_id=cache.get('digitalocean_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) >= 0, "List Digital Ocean machines did not return a proper result"
        print "Success!!!"


    def test_list_sizes_docker(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.list_sizes(cloud_id=cache.get('docker_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List Docker sizes did not return any sizes"
        print "Success!!!"


    def test_list_sizes_linode(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.list_sizes(cloud_id=cache.get('linode_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List Linode sizes did not return any sizes"
        print "Success!!!"


    def test_list_sizes_aws(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.list_sizes(cloud_id=cache.get('aws_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List AWS sizes did not return any sizes"
        print "Success!!!"


    def test_list_sizes_digitalocean(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.list_sizes(cloud_id=cache.get('digitalocean_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List Digital Ocean sizes did not return any sizes"
        print "Success!!!"


    def test_list_images_docker(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.list_images(cloud_id=cache.get('docker_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List Docker images did not return any images"
        print "Success!!!"


    def test_list_images_linode(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.list_images(cloud_id=cache.get('linode_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List Linode images did not return any images"
        print "Success!!!"


    def test_list_images_aws(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.list_images(cloud_id=cache.get('aws_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List AWS images did not return any images"
        print "Success!!!"


    def test_list_images_digitalocean(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.list_images(cloud_id=cache.get('digitalocean_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List Digital Ocean images did not return any images"
        print "Success!!!"
