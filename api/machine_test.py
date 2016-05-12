import json
import random

from time import sleep, time

from mist.io.tests.api.utils import *


def test_machine_async_lifecycle_with_cronjob(pretty_print, mist_core,
                                              expires,
                                              valid_api_token,
                                              random_ssh_key,
                                              random_bash_script):
    print "\n>>> GETing /clouds to find one that I will use"
    response = mist_core.list_clouds(api_token=valid_api_token).get()
    assert_response_ok(response)
    cloud_list = json.loads(response.content)
    assert_list_not_empty(cloud_list)
    test_cloud = None
    for cloud in cloud_list:
        if cloud['title'] == 'EC2':
            test_cloud = cloud
            break
    assert_is_not_none(test_cloud)
    cloud_id = test_cloud['id']
    print "\n>>> POSTing /create machine with async=True and cronjob\n"
    machine_name = "testlikeapro" + \
                   str(random.randint(1, 10000)) + \
                   "_async_cron"
    cronjob_name = "cronjob" + str(random.randint(1, 10000))
    response = mist_core.create_machine(api_token=valid_api_token,
                                        cloud_id=cloud_id,
                                        name=machine_name,
                                        provider='ec2_ap_northeast',
                                        image='ami-27f90e27',
                                        size='t1.micro',
                                        key_id=random_ssh_key['id'],
                                        location='0',
                                        async=True,
                                        cron_enable=True,
                                        cron_type='one_off',
                                        cron_entry=expires,
                                        cron_script=random_bash_script[
                                            'script_id'],
                                        cron_name=cronjob_name).post()
    assert_response_ok(response)
    print "\nMachine creation command has been submitted successfully. " \
          "Now polling!\n"
    job_id = json.loads(response.content)['job_id']

    # waiting for the creation of the machine to finish
    machine_id = None
    timeout = time() + 120
    while time() < timeout:
        response = mist_core.show_job(job_id=job_id,
                                      api_token=valid_api_token).get()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        log = filter(lambda log: log.get('action', '') == 'machine_creation_finished',
                     rjson.get('logs', []))
        if len(log) > 0:
            assert not log[0]['error'], "There was an error during machine " \
                                        "creation:\n%s" % response.content
            machine_id = log[0]['machine_id']
            break
        sleep(5)

    assert_is_not_none(machine_id, "Machine creation has not finished")
    print "\nMachine creation has finished for machine with name %s and id " \
          "%s\n" % (machine_name, machine_id)

    # waiting for the machine post deployment steps to finish
    timeout = time() + 240
    while time() < timeout:
        response = mist_core.show_job(job_id=job_id,
                                      api_token=valid_api_token).get()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        log = filter(lambda log: log.get('action', '') == 'post_deploy_finished',
                     rjson.get('logs', []))
        if len(log) > 0:
            break
        sleep(5)

    assert time() < timeout, "Waited for too long for post deployment steps " \
                             "to finish"
    print "\nPost deployment steps have finished after %s seconds. Destroying" \
          " the machine\n" % (time() - timeout + 200)

    response = mist_core.destroy_machine(api_token=valid_api_token,
                                         cloud_id=cloud_id,
                                         machine_id=machine_id).post()

    assert_response_ok(response)
    print "\nMachine destruction command has been submitted successfully"
    print "Success!!!!"
