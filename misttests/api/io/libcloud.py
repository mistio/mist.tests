from misttests.api.helpers import *
from misttests import config
from misttests.config import safe_get_var
import pytest

############################################################################
#                         Functional Testing                               #
############################################################################


@pytest.mark.incremental
class TestLibcloudFunctionality:

    def test_list_machines_docker(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.add_cloud(title='Docker', provider= 'docker', api_token=owner_api_token,
                                       docker_host=safe_get_var('clouds/docker', 'host', config.CREDENTIALS['DOCKER']['host']),
                                       docker_port=safe_get_var('clouds/docker_orchestrator', 'port', config.CREDENTIALS['DOCKER']['port']),
                                       authentication=safe_get_var('clouds/docker', 'authentication', config.CREDENTIALS['DOCKER']['authentication']),
                                       ca_cert_file=safe_get_var('clouds/docker', 'ca', config.CREDENTIALS['DOCKER']['ca']),
                                       key_file=safe_get_var('clouds/docker', 'key', config.CREDENTIALS['DOCKER']['key']),
                                       cert_file=safe_get_var('clouds/docker', 'cert', config.CREDENTIALS['DOCKER']['cert'])).post()
        assert_response_ok(response)
        cache.set('docker_cloud_id', response.json()['id'])
        response = mist_core.list_machines(cloud_id=cache.get('docker_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List Docker machines did not return any machines"
        print "Success!!!"

    def test_list_machines_linode(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.add_cloud(title='Linode', provider= 'linode', api_token=owner_api_token,
                                       api_key=safe_get_var('clouds/linode', 'api_key', config.CREDENTIALS['LINODE']['api_key'])).post()
        assert_response_ok(response)
        cache.set('linode_cloud_id', response.json()['id'])
        response = mist_core.list_machines(cloud_id=cache.get('linode_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) >= 0, "List Linode machines did not return a proper result"
        print "Success!!!"

    def test_list_machines_aws(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.add_cloud(title='AWS', provider= 'ec2', api_token=owner_api_token,
                                       api_key=safe_get_var('clouds/aws', 'api_key', config.CREDENTIALS['EC2']['api_key']),
                                       api_secret=safe_get_var('clouds/aws', 'api_secret', config.CREDENTIALS['EC2']['api_secret']),
                                       region='ec2_ap_northeast').post()
        assert_response_ok(response)
        cache.set('aws_cloud_id', response.json()['id'])
        response = mist_core.list_machines(cloud_id=cache.get('aws_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) >= 0, "List AWS machines did not return a proper result"
        print "Success!!!"

    def test_list_machines_digitalocean(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.add_cloud(title='Digital Ocean', provider= 'digitalocean', api_token=owner_api_token,
                                       token=safe_get_var('clouds/digitalocean', 'token', config.CREDENTIALS['DIGITALOCEAN']['token'])).post()
        assert_response_ok(response)
        cache.set('digitalocean_cloud_id', response.json()['id'])
        response = mist_core.list_machines(cloud_id=cache.get('digitalocean_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) >= 0, "List Digital Ocean machines did not return a proper result"
        print "Success!!!"


#    def test_list_machines_gce(self, pretty_print, mist_core, cache, owner_api_token):
#        response = mist_core.add_cloud(title='GCE', provider= 'gce', api_token=owner_api_token,
#                                       email=config.CREDENTIALS['GCE']['private_key']['client_email'],
#                                       project_id=config.CREDENTIALS['GCE']['project_id'],
#                                       private_key=config.CREDENTIALS['GCE']['private_key']).post()
#        assert_response_ok(response)
#        cache.set('gce_cloud_id', response.json()['id'])
#        response = mist_core.list_machines(cloud_id=cache.get('gce_cloud_id', ''), api_token=owner_api_token).get()
#        assert_response_ok(response)
#        assert len(response.json()) >= 0, "List GCE machines did not return a proper result"
#        print "Success!!!"

    def test_list_machines_softlayer(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.add_cloud(title='Softlayer', provider= 'softlayer', api_token=owner_api_token,
                                       username=safe_get_var('clouds/softlayer', 'username', config.CREDENTIALS['SOFTLAYER']['username']),
                                       api_key=safe_get_var('clouds/softlayer', 'api_key', config.CREDENTIALS['SOFTLAYER']['api_key'])).post()
        assert_response_ok(response)
        cache.set('softlayer_cloud_id', response.json()['id'])
        response = mist_core.list_machines(cloud_id=cache.get('softlayer_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) >= 0, "List Softlayer machines did not return a proper result"
        print "Success!!!"

    def test_list_machines_openstack(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.add_cloud(title='Openstack', provider= 'openstack', api_token=owner_api_token,
                                       username=safe_get_var('clouds/openstack', 'username', config.CREDENTIALS['OPENSTACK']['username']),
                                       auth_url=safe_get_var('clouds/openstack', 'auth_url', config.CREDENTIALS['OPENSTACK']['auth_url']),
                                       tenant=safe_get_var('clouds/openstack', 'tenant', config.CREDENTIALS['OPENSTACK']['tenant']),
                                       password=safe_get_var('clouds/openstack', 'password', config.CREDENTIALS['OPENSTACK']['password'])).post()
        assert_response_ok(response)
        cache.set('openstack_cloud_id', response.json()['id'])
        response = mist_core.list_machines(cloud_id=cache.get('openstack_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) >= 0, "List Openstack machines did not return a proper result"
        print "Success!!!"

    def test_list_machines_azure(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.add_cloud(title='Azure', provider= 'azure', api_token=owner_api_token,
                                       subscription_id=safe_get_var('clouds/azure', 'subscription_id', config.CREDENTIALS['AZURE']['subscription_id']),
                                       certificate=safe_get_var('clouds/azure', 'certificate', config.CREDENTIALS['AZURE']['certificate'])).post()
        assert_response_ok(response)
        cache.set('azure_cloud_id', response.json()['id'])
        response = mist_core.list_machines(cloud_id=cache.get('azure_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) >= 0, "List Azure machines did not return a proper result"
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

#    def test_list_sizes_gce(self, pretty_print, mist_core, cache, owner_api_token):
#        response = mist_core.list_sizes(cloud_id=cache.get('gce_cloud_id', ''), api_token=owner_api_token).get()
#        assert_response_ok(response)
#        assert len(response.json()) > 0, "List GCE sizes did not return any sizes"
#        print "Success!!!"

    def test_list_sizes_softlayer(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.list_sizes(cloud_id=cache.get('softlayer_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List Softlayer sizes did not return any sizes"
        print "Success!!!"

    def test_list_sizes_openstack(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.list_sizes(cloud_id=cache.get('openstack_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List Openstack sizes did not return any sizes"
        print "Success!!!"

    def test_list_sizes_azure(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.list_sizes(cloud_id=cache.get('azure_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List Azure sizes did not return any sizes"
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

#    def test_list_images_gce(self, pretty_print, mist_core, cache, owner_api_token):
#        response = mist_core.list_images(cloud_id=cache.get('gce_cloud_id', ''), api_token=owner_api_token).get()
#        assert_response_ok(response)
#        assert len(response.json()) > 0, "List GCE images did not return any images"
#        print "Success!!!"

    def test_list_images_softlayer(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.list_images(cloud_id=cache.get('softlayer_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List Softlayer images did not return any images"
        print "Success!!!"

    def test_list_images_openstack(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.list_images(cloud_id=cache.get('openstack_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List Openstack images did not return any images"
        print "Success!!!"

    def test_list_images_azure(self, pretty_print, mist_core, cache, owner_api_token):
        response = mist_core.list_images(cloud_id=cache.get('azure_cloud_id', ''), api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) > 0, "List Azure images did not return any images"
        print "Success!!!"
