import sys
import logging
import json
from time import time, sleep
import requests

from misttests import config
from misttests.api.utils import assert_response_ok
from misttests.config import safe_get_var
from misttests.api.core.core import MistIoApi
from misttests.api.io import conftest



log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

mist_core = MistIoApi(config.MIST_URL)

providers = {
    "Azure": {
        "credentials": "AZURE",
        "size": "ExtraSmall",
        "name_prefix": "mpazure_",
        "location": "West Europe"
    },
    "Digital Ocean": {
        "credentials": "DIGITALOCEAN",
        "size": "512mb",
        "name_prefix": "mpdo",
        "location": "ams2"
    },
    "Linode": {
        "credentials": "LINODE",
        "size": "1",
        "name_prefix": "mpLinode_",
        "location": "10",
         "disk":24576
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
        "disk": 25
    },
    "AWS": {
        "credentials": "EC2",
        "size": "m1.small",
        "name_prefix": "mpec2",
        "location": "ap-northeast-1a"
    },
    "GCE": {
        "credentials": "GCE",
        "size": "1000",
        "name_prefix": "mpgce",
        "location": "2101",
        "location_name":"europe-west1-b"
    },
    "Rackspace": {
        "credentials": "RACKSPACE",
        "size": "2",
        "name_prefix": "mpRackspace_",
        "location": "0"
    }
}

def check_machine_creation(log_line, job_id):
    try:
        if (log_line['job_id'] == job_id) and (log_line['action'] == 'machine_creation_finished'):
            if log_line['error'] == False:
                print 'Machine created succesfully'
                return True
            else:
                print log_line['error']
                return True
        else:
            return False
    except:
        return False

def add_cloud(provider):

    #TODO: First check if cloud exists and return the cloud ID and then try to add
    if provider == 'AWS':
        response = mist_core.add_cloud(title=provider, provider= 'ec2', api_token=config.MIST_API_TOKEN,
                                       api_key=config.CREDENTIALS['AWS']['api_key'],
                                       api_secret=config.CREDENTIALS['AWS']['api_secret'],
                                       region='ec2_ap_northeast').post()

    if response.text == u'Cloud with this name already exists':
        print "\nCloud already exists. Moving on.\n"
        return None
    else:
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

    response = mist_core.create_machine(api_token=config.MIST_API_TOKEN,
                                        cloud_id=cloud_id,
                                        name='AWSprovisiontest',
                                        provider=provider,
                                        image="ami-5e849130",
                                        size=providers['AWS']['size'],
                                        disk=disk,
                                        key_id=config.KEY_ID,
                                        location=providers[provider]['location'],
                                        location_name=location_name,
                                        async=True,
                                        cron_enable=False,
                                        monitoring=False).post()
    try:
        assert_response_ok(response)
        print "\nMachine creation command has been submitted successfully. Now polling!\n"
    except AssertionError as e:
        print "Machine creation was not successful!"
        raise e

    job_id = json.loads(response.content)['job_id']

    return job_id


def main():
    for provider in providers:
        if provider == 'AWS':
            #add the provider if not there
            cloud_id = add_cloud(provider)

            job_id = create_machine(cloud_id, provider)

            # waiting for the creation of the machine to finish
            log_found = False
            machine_id = None
            timeout = time() + 240
            while time() < timeout:
                resp = requests.get(
                    'https://mist.io/api/v1/logs',
                    headers={'Authorization': config.MIST_API_TOKEN},
                    verify=True
                )

                for log_line in resp.json():
                    if check_machine_creation(log_line, job_id):
                        log_found = True
                        break
                    else:
                        pass
                if log_found:
                    break
                sleep(5)

if __name__ == "__main__":
    main()
