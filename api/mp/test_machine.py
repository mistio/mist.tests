import os
import json
import random

from time import time
from time import sleep

from tests import config

from tests.api.helpers import *

# This are the names fo the providers that will be tested. The clouds that have
# been added to the test account should be equal to these.

provider_data = {
    "Azure": {
        "credentials": "AZURE",
        "size": "ExtraSmall",
        "name_prefix": "mpazure_",
        "location": "West Europe"
    },
    # "Digital Ocean": {
    #     "credentials": "DIGITALOCEAN",
    #     "size": "512mb",
    #     "name_prefix": "mpdo",
    #     "location": "ams2"
    # },
    # "Linode": {
    #     "credentials": "LINODE",
    #     "size": "1",
    #     "name_prefix": "mpLinode_",
    #     "location": "10",
    #     "disk":24576
    # },
    # "Nephoscale": {
    #     "credentials": "NEPHOSCALE",
    #     "size": "3",
    #     "name_prefix": "mpnephoscale",
    #     "location": "87729",
    #     "disk": 50
    # },
    # "SoftLayer": {
    #     "credentials": "SOFTLAYER",
    #     "size": "0",
    #     "name_prefix": "mpSoftLayer",
    #     "location": "ams01",
    #     "disk": 25
    # },
    # "EC2": {
    #     "credentials": "EC2",
    #     "size": "m1.small",
    #     "name_prefix": "mpec2",
    #     "location": "ap-northeast-1a"
    # },
    # "GCE": {
    #     "credentials": "GCE",
    #     "size": "1000",
    #     "name_prefix": "mpgce",
    #     "location": "2101",
    #     "location_name":"europe-west1-b"
    # },
    # "Rackspace": {
    #     "credentials": "RACKSPACE",
    #     "size": "2",
    #     "name_prefix": "mpRackspace_",
    #     "location": "0"
    # }
}


def update_json(mp_json, provider_title, image_id, image_name, success=True):
    if provider_title not in mp_json:
        mp_json[provider_title] = dict()
    mp_json[provider_title][image_id] = {
        'name': image_name,
        'result': 'success' if success else 'failure'
    }
    mp_json['updated'] = True


def test_machine_provisioning_test(mist_core, api_token, mp_json):
    import logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(threadName)s %(module)s - %(funcName)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    log = logging.getLogger(__name__)

    # log filtering helper
    def check_for_log(action):
        def check_log_action(machine_log):
            return action in machine_log.get('action', '').lower()
        return check_log_action

    # List clouds and choose which provider will be tested next
    available_providers = mist_core.list_clouds(api_token=api_token).get()
    list_of_providers = list()

    for provider in available_providers.json():
        if provider['provider'] == 'bare_metal' or \
                        provider['title'] not in provider_data:
            continue
        # filter out all the provider images that are starred and they have
        # not been tested before
        provider_images = filter(lambda el: el['star'] and el['id'] not in mp_json.get(provider['title'], {}),
                                 mist_core.list_images(cloud_id=provider['id'],
                                                       api_token=api_token).get().json())
        if not provider_images:
            log.info("There are no images left to test for provider %s" %
                     provider['title'])
            continue

        list_of_providers.append({
            'title': provider['title'],
            'id': provider['id'],
            'provider': provider['provider'],
            'images_left_to_test': provider_images,
            'images_tested_so_far': len(mp_json.get(provider['title'], {}))
        })

    if not list_of_providers:
        log.info("No providers left to test")

    list_of_providers = sorted(list_of_providers,
                               key=lambda el: el['images_tested_so_far'])

    provider_to_test = list_of_providers[0]

    cloud_id = provider_to_test['id']
    machine_name = provider_data[provider_to_test['title']]['name_prefix'] + \
                   str(random.randint(1, 10000))
    image_id = provider_to_test['images_left_to_test'][0]['id']
    location = provider_data[provider_to_test['title']]['location']
    size = provider_data[provider_to_test['title']]['size']
    provider = provider_to_test['provider']
    try:
        disk = provider_data[provider_to_test['title']]['disk']
    except:
        disk = ''
    image_extra = provider_to_test['images_left_to_test'][0]['extra']
    try:
        location_name = provider_data[provider_to_test['title']]['location_name']
    except:
        location_name = ''


    response = mist_core.create_machine(api_token=api_token,
                                        cloud_id=cloud_id,
                                        name=machine_name,
                                        provider=provider,
                                        image=image_id,
                                        size=size,
                                        disk=disk,
                                        image_extra=image_extra,
                                        key_id=config.KEY_ID,
                                        location=location,
                                        location_name=location_name,
                                        async=True,
                                        cron_enable=False,
                                        monitoring=False).post()
    try:
        assert_response_ok(response)
        log.info("\nMachine creation command has been submitted successfully."
                 " Now polling!\n")
    except AssertionError as e:
        log.error("Machine creation was not successful!")
        update_json(mp_json, provider_to_test['title'], image_id,
                    provider_to_test['images_left_to_test'][0]['name'], False)
        raise e

    job_id = json.loads(response.content)['job_id']

    # waiting for the creation of the machine to finish
    machine_id = None
    timeout = time() + 240
    while time() < timeout:
        response = mist_core.show_job(job_id=job_id,
                                      api_token=api_token).get()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        machine_logs = filter(check_for_log('machine_creation_finished'),
                              rjson.get('logs', []))
        if machine_logs:
            try:
                assert not machine_logs[0]['error'], \
                    "There was an error during machine creation:\n%s" % response.content
            except AssertionError as e:
                update_json(mp_json, provider_to_test['title'], image_id,
                            provider_to_test['images_left_to_test'][0]['name'],
                            False)
                mp_fail_notify(e, provider, provider_to_test['images_left_to_test'][0]['name'], 'provision')
                raise e
            machine_id = machine_logs[0]['machine_id']
            break
        sleep(5)

    assert_is_not_none(machine_id, "Machine creation has not finished")
    print "Machine creation has finished for machine with name %s and id " \
          "%s\n" % (machine_name, machine_id)
    update_json(mp_json, provider_to_test['title'], image_id,
                provider_to_test['images_left_to_test'][0]['name'])

    # waiting for the machine post deployment steps to finish
    timeout = time() + 480
    while time() < timeout:
        response = mist_core.show_job(job_id=job_id,
                                      api_token=api_token).get()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        machine_logs = filter(check_for_log('post_deploy_finished'),
                              rjson.get('logs', []))
        if machine_logs:
            break
        sleep(5)

    try:
        assert time() < timeout
    except AssertionError as e:
        print "Waited for too long for post deployment steps to finish"
        mp_fail_notify(e, provider, provider_to_test['images_left_to_test'][0]['name'], 'deploy')
        destroy_machine(log, mist_core, api_token, cloud_id, machine_id)
        raise e

    print "\nPost deployment steps have finished after %s seconds. Destroying" \
          " the machine\n" % (time() - timeout + 200)

    destroy_machine(log, mist_core, api_token, cloud_id, machine_id)
