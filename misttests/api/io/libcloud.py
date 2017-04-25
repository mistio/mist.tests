from misttests.api.helpers import *
from misttests import config

import pytest

PROVIDERS = ["Docker","Linode"]

############################################################################
#                             Unit Testing                                 #
############################################################################


############################################################################
#                         Functional Testing                               #
############################################################################


@pytest.mark.incremental
class TestMachinesFunctionality:

    def test_list_machines(self, pretty_print, mist_core, cache, owner_api_token):
        for provider in PROVIDERS:
            if provider == "Docker":
                response = mist_core.add_cloud(title='Docker', provider= 'docker', api_token=owner_api_token,
                                               docker_host=config.CREDENTIALS['DOCKER']['host'],
                                               docker_port=config.CREDENTIALS['DOCKER']['port'],
                                               authentication=config.CREDENTIALS['DOCKER']['authentication'],
                                               ca_cert_file=config.CREDENTIALS['DOCKER']['ca'],
                                               key_file=config.CREDENTIALS['DOCKER']['key'],
                                               cert_file=config.CREDENTIALS['DOCKER']['cert']).post()
                assert_response_ok(response)
                cache.set('cloud_id', response.json()['id'])
                response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()
                assert_response_ok(response)
                assert len(response.json()) > 0, "List machines did not return any machines"
            elif provider == "Linode":
                response = mist_core.add_cloud(title='Linode', provider= 'linode', api_token=owner_api_token,
                                               api_key=config.CREDENTIALS['LINODE']['api_key']).post()
                assert_response_ok(response)
                cache.set('cloud_id', response.json()['id'])
                response = mist_core.list_machines(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).get()
                assert_response_ok(response)
                assert len(response.json()) > 0, "List machines did not return any machines"
        print "Success!!!"
