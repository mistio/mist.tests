import sys
import json
import requests
import logging
import random
import shutil
import os

from subprocess import call

from distutils.util import strtobool as _bool

from misttests import config

from misttests.helpers.selenium_utils import choose_driver
from misttests.helpers.selenium_utils import get_screenshot
from misttests.helpers.selenium_utils import get_error_screenshot
from misttests.helpers.selenium_utils import produce_video_artifact
from misttests.helpers.selenium_utils import dump_js_console_log

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

BEHAVE_DEBUG_ON_ERROR = _bool(os.environ.get("BEHAVE_DEBUG_ON_ERROR", "no"))


def before_all(context):
    """
    Load the configuration config and setup the context
    """
    log.info("Starting before all hook")
    log.info("Webdriver path:" + config.WEBDRIVER_PATH)
    log.info("Webdriver log:" + config.WEBDRIVER_LOG)
    log.info("JS console log:" + config.JS_CONSOLE_LOG)

    context.mist_config = dict()
    context.mist_config['browser'] = choose_driver()
    context.browser = context.mist_config['browser']
    context.mist_config['MAYDAY_TOKEN'] = config.MAYDAY_TOKEN
    context.mist_config['NAME'] = config.NAME
    context.mist_config['BASE_EMAIL'] = config.BASE_EMAIL
    context.mist_config['EMAIL'] = config.EMAIL
    context.mist_config['PASSWORD1'] = config.PASSWORD1
    context.mist_config['PASSWORD2'] = config.PASSWORD2
    context.mist_config['CHANGED_PASSWORD'] = config.CHANGED_PASSWORD
    context.mist_config['SETUP_ENVIRONMENT'] = config.SETUP_ENVIRONMENT
    context.mist_config['MAYDAY_MACHINE'] = config.MAYDAY_MACHINE
    context.mist_config['MAYDAY_MACHINE_ID'] = config.MAYDAY_MACHINE_ID
    context.mist_config['OWNER_EMAIL'] = config.OWNER_EMAIL
    context.mist_config['OWNER_PASSWORD'] = config.OWNER_PASSWORD
    context.mist_config['MEMBER1_EMAIL'] = config.MEMBER1_EMAIL
    context.mist_config['MEMBER1_PASSWORD'] = config.MEMBER1_PASSWORD
    context.mist_config['MEMBER2_EMAIL'] = config.MEMBER2_EMAIL
    context.mist_config['MEMBER2_PASSWORD'] = config.MEMBER2_PASSWORD
    context.mist_config['AD_MEMBER_USERNAME'] = config.AD_MEMBER_USERNAME
    context.mist_config['AD_MEMBER_PASSWORD'] = config.AD_MEMBER_PASSWORD
    context.mist_config['AD_ORG_NAME'] = config.AD_ORG_NAME
    context.mist_config['LDAP_MEMBER_USERNAME'] = config.LDAP_MEMBER_USERNAME
    context.mist_config['LDAP_MEMBER_PASSWORD'] = config.LDAP_MEMBER_PASSWORD
    context.mist_config['LOCAL'] = config.LOCAL
    context.mist_config['ORG_NAME'] = (config.ORG_NAME or config.NAME) + str(random.randint(1, 10000000))
    context.mist_config['NON_STOP'] = '--stop' not in sys.argv
    context.mist_config['ERROR_NUM'] = 0
    context.mist_config['MIST_URL'] = config.MIST_URL
    context.mist_config['LOCAL_DOCKER'] = config.LOCAL_DOCKER
    context.mist_config['MP_DB_DIR'] = config.MP_DB_DIR
    context.mist_config['MAIL_PATH'] = config.MAIL_PATH
    context.mist_config['SCREENSHOT_PATH'] = config.SCREENSHOT_PATH
    context.mist_config['ARTIFACTS_PATH'] = config.ARTIFACTS_PATH
    context.mist_config['JS_CONSOLE_LOG'] = config.JS_CONSOLE_LOG
    context.mist_config['BROWSER_FLAVOR'] = config.BROWSER_FLAVOR
    context.mist_config['TESTING_PRIVATE_KEY'] = config.TESTING_PRIVATE_KEY
    context.mist_config['CREDENTIALS'] = config.CREDENTIALS
    context.mist_config['GOOGLE_TEST_EMAIL'] = config.GOOGLE_TEST_EMAIL
    context.mist_config['GOOGLE_TEST_PASSWORD'] = config.GOOGLE_TEST_PASSWORD
    context.mist_config['GITHUB_TEST_EMAIL'] = config.GITHUB_TEST_EMAIL
    context.mist_config['GITHUB_TEST_PASSWORD'] = config.GITHUB_TEST_PASSWORD
    context.mist_config['GOOGLE_REGISTRATION_TEST_EMAIL'] = config.GOOGLE_REGISTRATION_TEST_EMAIL
    context.mist_config['GOOGLE_REGISTRATION_TEST_PASSWORD'] = config.GOOGLE_REGISTRATION_TEST_PASSWORD
    context.mist_config['GITHUB_REGISTRATION_TEST_EMAIL'] = config.GITHUB_REGISTRATION_TEST_EMAIL
    context.mist_config['GITHUB_REGISTRATION_TEST_PASSWORD'] = config.GITHUB_REGISTRATION_TEST_PASSWORD
    context.mist_config['GMAIL_THINGIRL_USER'] = config.GMAIL_THINGIRL_USER
    context.mist_config['GMAIL_THINGIRL_PASSWORD'] = config.GMAIL_THINGIRL_PASSWORD
    context.mist_config['recording_session'] = config.RECORD_SELENIUM
    context.mist_config['IMAP_USE_SSL'] = config.IMAP_USE_SSL
    context.mist_config['IMAP_HOST'] = config.IMAP_HOST
    context.mist_config['IMAP_PORT'] = config.IMAP_PORT
    context.mist_config['CC_CVC'] = config.CC_CVC
    context.mist_config['CC_CC'] = config.CC_CC
    context.mist_config['CC_EXPIRE_MONTH'] = config.CC_EXPIRE_MONTH
    context.mist_config['CC_EXPIRE_YEAR'] = config.CC_EXPIRE_YEAR
    context.mist_config['CC_ZIP_CODE'] = config.CC_ZIP_CODE
    context.mist_config['SLACK_WEBHOOK_URL'] = config.SLACK_WEBHOOK_URL
    context.mist_config['SLACK_WEBHOOK_CHANNEL'] = config.SLACK_WEBHOOK_CHANNEL
    context.mist_config['SLACK_WEBHOOK_TOKEN'] = config.SLACK_WEBHOOK_TOKEN
    context.link_inside_email = ''
    context.mist_config['ORG_ID'] = config.ORG_ID
    context.mist_config['PRODUCE_VIDEO_SCREENCAST_ON_ERROR'] = config.PRODUCE_VIDEO_SCREENCAST_ON_ERROR
    context.mist_config['RULES_TEST_HOST'] = config.RULES_TEST_HOST
    context.mist_config['RULES_TEST_EMAIL'] = config.RULES_TEST_EMAIL
    context.mist_config['RULES_TEST_PASSWORD'] = config.RULES_TEST_PASSWORD

    if config.LOCAL:
        log.info("Initializing behaving mail for path: %s" % config.MAIL_PATH)
        from behaving.mail import environment as behaving_mail
        # with this behaving will get the path to save and retrieve mails
        context.mail_path = config.MAIL_PATH
        # calling behaving to setup it's context variables.
        behaving_mail.before_all(context)

    if config.REGISTER_USER_BEFORE_FEATURE:
        payload = {
            'email': context.mist_config['EMAIL'],
            'password': context.mist_config['PASSWORD1'],
            'name': "Atheofovos Gkikas",
            'org_name': context.mist_config['ORG_NAME']
        }

        response = requests.post(
            "%s/api/v1/dev/register" % context.mist_config['MIST_URL'],
            data=json.dumps(payload)
        )
        context.mist_config['ORG_ID'] = response.json().get('org_id')
        context.mist_config['ORG_NAME'] = response.json().get('org_name')

    # check whether hs repo is tested
    api_token = get_api_token(context)
    headers = {'Authorization': api_token}

    response = requests.get(
        "%s/api/v1/billing" % context.mist_config['MIST_URL'],
        headers=headers
    )

    if response.status_code == 404:
        context.mist_config['IS_HS_REPO'] = False
    else:
        context.mist_config['IS_HS_REPO'] = True

    log.info("Finished with before_all hook. Starting tests")
    log.info("EMAIL: %s" % context.mist_config['EMAIL'])
    log.info("PASSWORD1: %s" % context.mist_config['PASSWORD1'])
    log.info("MIST_URL: %s" % context.mist_config['MIST_URL'])


def after_step(context, step):
    if config.RECORD_SELENIUM:
        get_screenshot(context, step)

    if step.status == "failed":
        try:
            get_error_screenshot(context, step)
        except Exception as e:
            log.error("Could not get screen shot: %s" % repr(e))

        if config.PRODUCE_VIDEO_SCREENCAST_ON_ERROR:
            produce_video_artifact(context, step)

        # break into post mortem
        if BEHAVE_DEBUG_ON_ERROR:
            import ipdb
            ipdb.set_trace()
            ipdb.post_mortem(step.exc_traceback)


def after_all(context):
    log.info("USER: %s" % context.mist_config['EMAIL'])
    log.info("PASSWORD1: %s" % context.mist_config['PASSWORD1'])
    log.info("MEMBER_1: %s" % context.mist_config['MEMBER1_EMAIL'])
    log.info("MEMBER1_PASSWORD: %s" % context.mist_config['MEMBER1_PASSWORD'])
    log.info("MEMBER_2: %s" % context.mist_config['MEMBER2_EMAIL'])
    log.info("MEMBER2_PASSWORD: %s" % context.mist_config['MEMBER2_PASSWORD'])
    log.info("MIST_URL: %s" % context.mist_config['MIST_URL'])

    finish_and_cleanup(context)


def get_api_token(context):
    payload = {
        'email': context.mist_config['EMAIL'],
        'password': context.mist_config['PASSWORD1'],
        'org_id': context.mist_config['ORG_ID']
    }
    re = requests.post("%s/api/v1/tokens" % context.mist_config['MIST_URL'], data=json.dumps(payload))
    return re.json()['token']


def kill_yolomachine(context, machines, headers, cloud_id):
    for machine in machines:
        if 'yolomachine' in machine['name']:
            log.info('Killing yolomachine...')
            payload = {'action': 'destroy'}
            uri = context.mist_config['MIST_URL'] + '/api/v1/clouds/' + \
                  cloud_id + '/machines/' + machine['external_id']
            requests.post(uri, data=json.dumps(payload), headers=headers)


def kill_orchestration_machines(context):
    api_token = get_api_token(context)
    headers = {'Authorization': api_token}

    response = requests.get("%s/api/v1/clouds" % context.mist_config['MIST_URL'], headers=headers)
    for cloud in response.json():
        if 'docker' in cloud['provider']:
            cloud_id = cloud['id']
            uri = context.mist_config['MIST_URL'] + '/api/v1/clouds/' + cloud_id + '/machines'
            response = requests.get(uri, headers=headers)
            kill_yolomachine(context, response.json(), headers, cloud_id)


def delete_schedules(context):
    api_token = get_api_token(context)
    headers = {'Authorization': api_token}

    response = requests.get(
        "%s/api/v1/schedules" % context.mist_config['MIST_URL'],
        headers=headers
    )
    for schedule in response.json():
        log.info('Deleting schedule...')
        uri = context.mist_config['MIST_URL'] + '/api/v1/schedules/' + schedule['id']
        requests.delete(uri, headers=headers)


def kill_docker_machine(context, machine_to_destroy):
    api_token = get_api_token(context)
    headers = {'Authorization': api_token}
    response = requests.get("%s/api/v1/clouds" % context.mist_config['MIST_URL'], headers=headers)
    for cloud in response.json():
        if 'docker' in cloud['provider']:
            uri = context.mist_config['MIST_URL'] + '/api/v1/clouds/' + cloud['id'] + '/machines'
            response = requests.get(uri, headers=headers)
            if response.json():
                for machine in response.json():
                    if machine_to_destroy == machine['name']:
                        log.info('Killing docker machine %s ...' % str(machine['name']))
                        payload = {'action': 'destroy'}
                        uri = context.mist_config['MIST_URL'] + \
                                '/api/v1/clouds/' + cloud['id'] + \
                                '/machines/' + machine['external_id']
                        requests.post(uri, data=json.dumps(payload), headers=headers)

def delete_ec2_network(context, network_to_delete):
    api_token = get_api_token(context)
    headers = {'Authorization': api_token}
    response = requests.get("%s/api/v1/clouds" % context.mist_config['MIST_URL'], headers=headers)
    for cloud in response.json():
        if 'ec2' in cloud['provider']:
            uri = context.mist_config['MIST_URL'] + '/api/v1/clouds/' + cloud['id'] + '/networks'
            response = requests.get(uri, headers=headers)
            if response.json():
                for network in response.json():
                    if network_to_delete == network['name']:
                        log.info('Deleting ec2 network...')
                        uri = context.mist_config['MIST_URL'] + \
                                '/api/v1/clouds/' + cloud['id'] + \
                                '/networks/' + network['id']
                        requests.delete(uri, headers=headers)


def finish_and_cleanup(context):
    dump_js_console_log(context)
    context.mist_config['browser'].quit()
    if context.mist_config.get('browser2'):
        context.mist_config['browser2'].quit()


def mayday_cleanup(context):
    # delete mayday scheduler
    headers = {'Authorization': context.mist_config['MAYDAY_TOKEN']}

    response = requests.get(
        "%s/api/v1/schedules" % context.mist_config['MIST_URL'],
        headers=headers
    )

    for schedule in response.json():
        if schedule['name'] == 'MaydayScheduler':
            response = requests.delete(context.mist_config['MIST_URL'] + '/api/v1/schedules/' + schedule['id'],
                                       headers=headers)
            assert response.status_code == 200, "Could not delete schedule!"
            break

    # start mayday-test container
    response = requests.get("%s/api/v1/clouds" % context.mist_config['MIST_URL'], headers=headers)
    for cloud in response.json():
        if 'docker' in cloud['provider']:
            response = requests.get(context.mist_config['MIST_URL'] + '/api/v1/clouds/' + cloud['id'] + '/machines',
                                    headers=headers)
            for machine in response.json():
                if 'mayday-test' in machine['name']:
                    payload = {'action': 'start'}
                    uri = context.mist_config['MIST_URL'] + \
                            '/api/v1/clouds/' + cloud['id'] + \
                            '/machines/' + machine['external_id']
                    response = requests.post(uri, data=json.dumps(payload), headers=headers)
                    assert response.status_code == 200, "Could not start mayday-test container!"
                    break


def mp_cleanup(context):
    headers = {'Authorization': get_api_token(context)}
    response = requests.get(context.mist_config['MIST_URL'] + '/api/v1/machines',headers=headers)

    for machine in response.json():
        if 'mp-test' in machine['name'] and machine['state'] in ['running', 'stopped']:
            payload = {'action': 'destroy'}
            uri = context.mist_config['MIST_URL'] + \
                    '/api/v1/clouds/' + machine['cloud'] + \
                    '/machines/' + machine['external_id']
            log.info('Killing multiprovisioning machine %s' % str(machine['name']))
            response = requests.post(uri, data=json.dumps(payload), headers=headers)
            assert response.status_code == 200, "Could not destroy multiprovisioning machine %s"  % str(machine['name'])


def after_feature(context, feature):
    if feature.name == 'Orchestration':
        kill_orchestration_machines(context)
    if feature.name == 'Schedulers':
        delete_schedules(context)
        kill_docker_machine(context, context.mist_config.get('test-machine-random'))
    if feature.name == 'Schedulers-b':
        delete_schedules(context)
        kill_docker_machine(context, context.mist_config.get('test-ui-machine-random'))
        kill_docker_machine(context, context.mist_config.get('test-ui-machine-2-random'))
    if feature.name == 'Machines':
        kill_docker_machine(
            context,
            context.mist_config.get('ui-test-create-machine-random')
        )
    if feature.name == 'RBAC-rules-v2':
        kill_docker_machine(context, context.mist_config.get('rbac-test-machine-random'))
    if feature.name in ['Monitoring']:
        kill_docker_machine(context, context.mist_config.get('monitored-machine-random'))
    if feature.name in ['Rules']:
        kill_docker_machine(context, context.mist_config.get('rules-test-machine-random'))
        kill_docker_machine(context, context.mist_config.get('rules-test-machine-1-random'))
    if feature.name == 'Images-Networks':
        delete_ec2_network(context, context.mist_config.get('network_random'))
    #if feature.name == 'Production':
    #    mayday_cleanup(context)
    if feature.name == 'Multiprovisioning':
        mp_cleanup(context)
