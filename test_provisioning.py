import sys
import logging
import json
from time import time, sleep
import requests
from random import randint

from misttests import config
from misttests.api.utils import assert_response_ok
from misttests.config import safe_get_var
from misttests.api.core.core import MistIoApi
from misttests.api.io import conftest
from misttests.config import safe_get_var



log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

mist_core = MistIoApi(config.MIST_URL)

providers = {
    "Azure": {
        "credentials": "AZURE",
        "size": "ExtraSmall",
        "name_prefix": "mpazure_",
        "location": "West Europe",
        "image": "b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-17_04-amd64-server-20170412.1-en-us-30GB"
    },
    "Docker": {
        "credentials": "DOCKER",
        "size": "",
        "location": "",
        "image": "mist/ubuntu-14.04"
    },
    "Digital Ocean": {
        "credentials": "DIGITALOCEAN",
        "size": "512mb",
        "name_prefix": "mpdo",
        "location": "ams2",
        "image": "21419458"
    },
    "Linode": {
        "credentials": "LINODE",
        "size": "1",
        "name_prefix": "mpLinode_",
        "location": "10",
        "disk":12576,
        "image": "146"
    },
    "Nephoscale": {
        "credentials": "NEPHOSCALE",
        "size": "3",
        "name_prefix": "mpnephoscale",
        "location": "87729",
        "disk": 50
    },
    "SoftLayer": {
        "credentials": "SOFTLAYER",
        "size": "0",
        "name_prefix": "mpSoftLayer",
        "location": "ams01",
        "disk": 25,
        "image": "UBUNTU_LATEST_64"
    },
    "AWS": {
        "credentials": "EC2",
        "size": "m1.small",
        "name_prefix": "mpec2",
        "location": "ap-northeast-1a",
        "image": "ami-5e849130"
    },
    "GCE": {
        "credentials": "GCE",
        "size": "1000",
        "name_prefix": "mpgce",
        "location": "2101",
        "location_name":"europe-west1-b",
        "image":"7223507091408113841",
        "image_extra": { "selfLink":"https://www.googleapis.com/compute/v1/projects/ubuntu-os-cloud/global/images/ubuntu-1610-yakkety-v20170619a" }
    },
    "Rackspace": {
        "credentials": "RACKSPACE",
        "size": "2",
        "name_prefix": "mpRackspace_",
        "location": "0"
    },
    "Openstack": {
        "credentials": "OPENSTACK",
        "size": "1",
        "size_disk_primary": "5",
        "location": "0",
        "networks":["583bb96c-36c2-483a-b4bf-667f0278d1fb"],
        "size_cpu": "1",
        "associate_floating_ip":"true",
        "size_disk_swap": "1",
        "image": "d69e1f0e-5205-4698-880e-81f95774a633"
    }
}

def check_machine_creation(log_line, job_id):
    try:
        if (log_line['job_id'] == job_id) and (log_line['action'] == 'machine_creation_finished'):
            if log_line['error'] == False:
                print 'Machine created succesfully'
                machine_id = log_line['machine_id']
                return machine_id
            else:
                print log_line['error']
                return True
        else:
            return False
    except:
        return False


def check_cloud_exists(provider):
    resp = requests.get(
        config.MIST_URL + '/api/v1/clouds',
        headers={'Authorization': config.MIST_API_TOKEN},
        verify=True
    )
    cloud_id = None

    for cloud in resp.json():
        if cloud['title'] == provider:
            cloud_id = cloud['id']
    return cloud_id


def add_cloud(provider):
    cloud_id = check_cloud_exists(provider)
    if cloud_id == None:
        if provider == 'AWS':
            response = mist_core.add_cloud(title=provider, provider= 'ec2', api_token=config.MIST_API_TOKEN,
                                           api_key=config.CREDENTIALS['AWS']['api_key'],
                                           api_secret=config.CREDENTIALS['AWS']['api_secret'],
                                           region='ec2_ap_northeast').post()

        elif provider == 'Digital Ocean':
            response = mist_core.add_cloud(title=provider, provider= 'digitalocean', api_token=config.MIST_API_TOKEN,
                                           token=config.CREDENTIALS['DO']['token']).post()

        elif provider == "Linode":
            response = mist_core.add_cloud(title=provider, provider= 'linode', api_token=config.MIST_API_TOKEN,
                                           api_key=config.CREDENTIALS['LINODE']['api_key']).post()

        elif provider == "Azure":
            response = mist_core.add_cloud(title=provider, provider= 'azure', api_token=config.MIST_API_TOKEN,
                                           subscription_id=config.CREDENTIALS['AZURE']['subscription_id'],
                                           certificate=config.CREDENTIALS['AZURE']['certificate']).post()

        elif provider == 'Docker':
            response = mist_core.add_cloud(title=provider, provider= 'docker', api_token=config.MIST_API_TOKEN,
                                           docker_host=config.CREDENTIALS['DOCKER']['host'],
                                           docker_port=config.CREDENTIALS['DOCKER']['port'],
                                           authentication=config.CREDENTIALS['DOCKER']['authentication'],
                                           ca_cert_file=config.CREDENTIALS['DOCKER']['ca'],
                                           key_file=config.CREDENTIALS['DOCKER']['key'],
                                           cert_file=config.CREDENTIALS['DOCKER']['cert']).post()

        elif provider == "SoftLayer":
            response = mist_core.add_cloud(title=provider, provider= 'softlayer', api_token=config.MIST_API_TOKEN,
                                           username=config.CREDENTIALS['SOFTLAYER']['username'],
                                           api_key=config.CREDENTIALS['SOFTLAYER']['api_key']).post()

        elif provider == "GCE":
            response = mist_core.add_cloud(title='GCE', provider= 'gce', api_token=config.MIST_API_TOKEN,
                                      project_id=safe_get_var('clouds/gce/mist-dev', 'project_id',
                                                              config.CREDENTIALS['GCE']['project_id']),
                                      private_key = json.dumps(safe_get_var('clouds/gce/mist-dev', 'private_key',
                                                              config.CREDENTIALS['GCE']['private_key']))).post()

        elif provider == "Openstack":
            response = mist_core.add_cloud(title=provider, provider= 'openstack', api_token=config.MIST_API_TOKEN,
                                           username=config.CREDENTIALS['OPENSTACK']['username'],
                                           auth_url=config.CREDENTIALS['OPENSTACK']['auth_url'],
                                           tenant=config.CREDENTIALS['OPENSTACK']['tenant'],
                                           password=config.CREDENTIALS['OPENSTACK']['password']).post()

        assert_response_ok(response)
        cloud_id = response.json()['id']

    return cloud_id


def create_machine(cloud_id, provider):
    #creating machine
    try:
        disk = providers[provider]['disk']
    except:
        disk = ''
    try:
        location_name=providers[provider]['location_name']
    except:
        location_name = ''
    try:
        networks=providers[provider]['network']
    except:
        networks = ''
    try:
        image_extra=providers[provider]['image_extra']
    except:
        image_extra = ''



    response = mist_core.create_machine(api_token=config.MIST_API_TOKEN,
                                        cloud_id=cloud_id,
                                        name= provider.replace(" ", "").lower() + 'provisiontest' + str(randint(0,9999)),
                                        provider=provider,
                                        image=providers[provider]['image'],
                                        image_extra=providers[provider]['image_extra'],
                                        size=providers[provider]['size'],
                                        disk=disk,
                                        key_id=config.KEY_ID,
                                        location=providers[provider]['location'],
                                        location_name=location_name,
                                        async=True,
                                        cron_enable=False,
                                        monitoring=False).post()
    try:
        assert_response_ok(response)
        print "\n " + provider + ": Machine creation command has been submitted successfully. Now polling!\n"
    except AssertionError as e:
        print "Machine creation was not successful!"
        raise e

    job_id = json.loads(response.content)['job_id']

    return job_id


def main():
    for provider in providers:
        if provider in ['AWS', 'Digital Ocean', 'Linode', 'Azure', 'Docker', 'SoftLayer', 'GCE']:
            #add the provider if not there
            cloud_id = add_cloud(provider)

            job_id = create_machine(cloud_id, provider)

            # waiting for the creation of the machine to finish
            log_found = False
            machine_id = None
            timeout = time() + 240
            while time() < timeout:
                resp = requests.get(
                    config.MIST_URL + '/api/v1/logs',
                    headers={'Authorization': config.MIST_API_TOKEN},
                    verify=True
                )

                for log_line in resp.json():
                    machine_creation = check_machine_creation(log_line, job_id)
                    if machine_creation:
                        machine_id = machine_creation
                        log_found = True
                        break
                    else:
                        pass
                if log_found:
                    break
                sleep(5)

            #destroy the machine
#            if machine_id:
#                resp = requests.post(
#                    config.MIST_URL + '/api/v1/clouds/' + cloud_id + '/machines/' + machine_id,
#                    headers={'Authorization': config.MIST_API_TOKEN},
#                    data = {'action':'destroy'},
#                    verify=True
#                )
#
#                try:
#                    assert_response_ok(resp)
#                    print "\n " + provider + ": Machine destroyed successfully\n"
#                except AssertionError as e:
#                    print "Could not destroy machine!"
#                    raise e

if __name__ == "__main__":
    main()
