import json

from time import time, sleep

from mist.io.tests.api.utils import *


#def test_001_machine_start(pretty_print, mist_core,
#                           valid_api_token, random_ssh_key):
#    print "\n>>> GETing /clouds to find Docker\n"
#    clouds = mist_io.list_clouds(api_token=valid_api_token).get()
#    assert_response_ok(clouds)
#    clouds = json.load(clouds.content)
#    assert_list_not_empty(clouds)
#
#    test_cloud = None
#    for cloud in clouds:
#        if cloud['title'] == 'Docker':
#            test_cloud = cloud
#            break
#    assert_is_not_none(test_cloud)
#    cloud_id = test_cloud['id']
#    machine_name = 'DockerActionsTest'
#
#    print "\n>>> POSTing /create machine in Docker cloud\n"
#    machine = mist_io.create_machine(api_token=valid_api_token,
#                                     async=False,
#                                     cloud_id=cloud_id,
#                                     name=machine_name,
#                                     provider='docker',
#                                     image='ubuntu:latest',
#                                     size='default',
#                                     key_id=random_ssh_key['id'],
#                                     location=None).post()
#    assert_response_ok(machine)
#    print "\nMachine creation has been successful\n"
#
#    job_id = json.loads(machine.content)['job_id']
#    machine_id = None
#    timeout = time() + 120
#    while time() < timeout:
#        response = mist_core.show_job(api_token=valid_api_token,
#                                      job_id=job_id).get()
#        assert_response_ok(response)
#        rjson = json.loads(response.content)
#        log = filter(lambda log: log.get('action', '') ==
# 'machine_creation_finished',
#                     rjson.get('logs', []))
#        if len(log) > 0:
#            assert not log[0]['error'], "There was an error during machine " \
#                                        "creation:\n%s" % response.content
#            machine_id = log[0]['machine_id']
#            break
#        sleep(5)
#
#    assert_is_not_none(machine_id, "Machine creation has not finished")
#    print "\nMachine creation has finished for machine with name %s and id " \
#          "%s\n" % (machine_name, machine_id)
#
#    # waiting for the machine post deployment steps to finish
#    timeout = time() + 240
#    while time() < timeout:
#        response = mist_core.show_job(api_token=valid_api_token,
#                                      job_id=job_id).get()
#        assert_response_ok(response)
#        rjson = json.loads(response.content)
#        log = filter(lambda log: log.get('action', '') == 'post_deploy_finished',
#                     rjson.get('logs', []))
#        if len(log) > 0:
#            break
#        sleep(5)
#
#    assert time() < timeout, "Waited for too long for post deployment steps " \
#                             "to finish"
#    print "\nPost deployment steps have finished after %s seconds. Destroying" \
#          " the machine\n" % (time() - timeout + 200)
#
#    response = mist_io.stop_machine(api_token=valid_api_token,
#                                    cloud_id=cloud_id,
#                                    machine_id=machine_id).post()
#    assert_response_ok(response)
#
#    response = mist_io.stop_machine(api_token=valid_api_token,
#                                    cloud_id=cloud_id,
#                                    machine_id=machine_id).post()
#    assert_response_ok(response)
#
#    print "\nDocker machines stopped and started successfully\n"
#    print "Success!!!"

# the dev docker is used as our cloud
def test_002_machine_reboot(pretty_print, mist_core,
                            valid_api_token, random_ssh_key):
    print "\n>>> GETing /clouds to find Docker\n"
    clouds = mist_core.list_clouds(api_token=valid_api_token).get()
    assert_response_ok(clouds)
    clouds = json.loads(clouds.content)
    assert_list_not_empty(clouds)

    test_cloud = None
    for cloud in clouds:
        if cloud['title'] == 'Docker':
            test_cloud = cloud
            break
    assert_is_not_none(test_cloud)
    cloud_id = test_cloud['id']
    machine_name = 'DockerActionsTest'

    print "\n>>> POSTing /create machine in Docker cloud\n"
    machine = mist_core.create_machine(api_token=valid_api_token,
                                       cloud_id=cloud_id,
                                       name=machine_name,
                                       provider='docker',
                                       image='mist/ubuntu-14.04',
                                       size='default',
                                       key_id=random_ssh_key['id'],
                                       async=True,
                                       location=None).post()
    assert_response_ok(machine)
    print "\nMachine /create request has been submitted\n"

    job_id = json.loads(machine.content)['job_id']
    machine_id = None
    timeout = time() + 120
    while time() < timeout:
        response = mist_core.show_job(api_token=valid_api_token,
                                      job_id=job_id).get()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        _log = rjson['logs'][-1]
        print _log
        assert not _log['error'], "There was an error during machine " \
                                  "creation:\n%s" % response.content
        machine_id = _log.get('machine_id', '')
        if machine_id:
            break
        sleep(5)

    assert_is_not_none(machine_id, "Machine creation has not finished")
    print "\nMachine creation has finished for machine with name %s and id " \
          "%s\n" % (machine_name, machine_id)

    # waiting for the machine post deployment steps to finish
    timeout = time() + 240
    while time() < timeout:
        response = mist_core.show_job(api_token=valid_api_token,
                                      job_id=job_id).get()
        assert_response_ok(response)
        rjson = json.loads(response.content)
        log = filter(lambda log: log.get('action', '') == 'post_deploy_finished',
                     rjson.get('logs', []))
        if len(log) > 0:
            break
        sleep(5)

    assert time() < timeout, "Waited for too long for post deployment steps " \
                             "to finish"
    print "\nPost deployment steps have finished after %s seconds. " \
          "Will attempt to reboot\n" % (time() - timeout + 200)

    response = mist_core.reboot_machine(api_token=valid_api_token,
                                        cloud_id=cloud_id,
                                        machine_id=machine_id).post()
    assert_response_ok(response)

    print "\nDocker machine rebooted successfully\n"
    print "Success!!!"
