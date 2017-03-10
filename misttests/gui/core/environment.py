import sys
import json
import requests
import logging
import random

from .requirements import chrome_driver_setup

from misttests import config

from misttests.helpers.selenium_utils import choose_driver
from misttests.helpers.selenium_utils import get_screenshot
from misttests.helpers.selenium_utils import dump_js_console_log

from misttests.helpers.recording import start_recording
from misttests.helpers.recording import stop_recording


log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def before_all(context):
    """
    Load the configuration config and setup the context
    """
    chrome_driver_setup()
    log.info("Starting before all hook")
    log.info("Webdriver path:" + config.WEBDRIVER_PATH)
    log.info("Webdriver log:" + config.WEBDRIVER_LOG)
    log.info("JS console log:" + config.JS_CONSOLE_LOG)

    context.mist_config = dict()
    context.mist_config['browser'] = choose_driver()
    context.browser = context.mist_config['browser']
    context.mist_config['NAME'] = config.NAME
    context.mist_config['BASE_EMAIL'] = config.BASE_EMAIL
    context.mist_config['EMAIL'] = config.EMAIL
    context.mist_config['PASSWORD1'] = config.PASSWORD1
    context.mist_config['PASSWORD2'] = config.PASSWORD2
    context.mist_config['SETUP_ENVIRONMENT'] = config.SETUP_ENVIRONMENT
    context.mist_config['MAYDAY_MACHINE'] = config.MAYDAY_MACHINE
    context.mist_config['DEMO_EMAIL'] = config.DEMO_EMAIL
    context.mist_config['DEMO_PASSWORD'] = config.DEMO_PASSWORD
    context.mist_config['MIST_DEMO_REQUEST_EMAIL'] = config.MIST_DEMO_REQUEST_EMAIL
    context.mist_config['OWNER_EMAIL'] = config.OWNER_EMAIL
    context.mist_config['OWNER_PASSWORD'] = config.OWNER_PASSWORD
    context.mist_config['MEMBER1_EMAIL'] = config.MEMBER1_EMAIL
    context.mist_config['MEMBER1_PASSWORD'] = config.MEMBER1_PASSWORD
    context.mist_config['MEMBER2_EMAIL'] = config.MEMBER2_EMAIL
    context.mist_config['MEMBER2_PASSWORD'] = config.MEMBER2_PASSWORD
    context.mist_config['LOCAL'] = config.LOCAL
    context.mist_config['DEBUG'] = config.DEBUG
    context.mist_config['ORG_NAME'] = config.ORG_NAME + str(random.randint(1, 10000000))
    context.mist_config['NON_STOP'] = '--stop' not in sys.argv
    context.mist_config['ERROR_NUM'] = 0
    context.mist_config['MIST_URL'] = config.MIST_URL
    context.mist_config['MP_DB_DIR'] = config.MP_DB_DIR
    context.mist_config['MAIL_PATH'] = config.MAIL_PATH
    context.mist_config['SCREENSHOT_PATH'] = config.SCREENSHOT_PATH
    context.mist_config['JS_CONSOLE_LOG'] = config.JS_CONSOLE_LOG
    context.mist_config['BROWSER_FLAVOR'] = config.BROWSER_FLAVOR
    context.mist_config['CREDENTIALS'] = config.CREDENTIALS
    context.mist_config['GOOGLE_TEST_EMAIL'] = config.GOOGLE_TEST_EMAIL
    context.mist_config['GOOGLE_TEST_PASSWORD'] = config.GOOGLE_TEST_PASSWORD
    context.mist_config['GITHUB_TEST_EMAIL'] = config.GITHUB_TEST_EMAIL
    context.mist_config['GITHUB_TEST_PASSWORD'] = config.GITHUB_TEST_PASSWORD
    context.mist_config['GOOGLE_REGISTRATION_TEST_EMAIL'] = config.GOOGLE_REGISTRATION_TEST_EMAIL
    context.mist_config['GOOGLE_REGISTRATION_TEST_PASSWORD'] = config.GOOGLE_REGISTRATION_TEST_PASSWORD
    context.mist_config['GITHUB_REGISTRATION_TEST_EMAIL'] = config.GITHUB_REGISTRATION_TEST_EMAIL
    context.mist_config['GITHUB_REGISTRATION_TEST_PASSWORD'] = config.GITHUB_REGISTRATION_TEST_PASSWORD
    context.mist_config['GMAIL_FATBOY_USER'] = config.GMAIL_FATBOY_USER
    context.mist_config['GMAIL_FATBOY_PASSWORD'] = config.GMAIL_FATBOY_PASSWORD
    context.mist_config['recording_session'] = config.RECORD_SELENIUM
    context.link_inside_email = ''
    context.mist_config['ORG_ID'] = ''

    log.info("Finished with the bulk of the test settings")
    if config.LOCAL:
        log.info("Initializing behaving mail for path: %s" % config.MAIL_PATH)
        from behaving.mail import environment as behaving_mail
        # with this behaving will get the path to save and retrieve mails
        context.mail_path = config.MAIL_PATH
        # calling behaving to setup it's context variables.
        behaving_mail.before_all(context)

    if context.mist_config.get('recording_session', False):
        start_recording()

    log.info("Finished with before_all hook. Starting tests")


def before_feature(context, feature):
    if config.REGISTER_USER_BEFORE_FEATURE:
        payload = {
            'email': context.mist_config['EMAIL'],
            'password': context.mist_config['PASSWORD1'],
            'name': "Atheofovos Gkikas"
        }

        re = requests.post("%s/api/v1/dev/register" % context.mist_config['MIST_URL'], data=json.dumps(payload))

        context.mist_config['ORG_ID'] = re.json().get('org_id')
        context.mist_config['ORG_NAME'] = re.json().get('org_name')


def after_step(context, step):
    if step.status == "failed":
        try:
            get_screenshot(context)
        except Exception as e:
            log.error("Could not get screen shot: %s" % repr(e))
            pass


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
            payload= {'action': 'destroy'}
            uri = context.mist_config['MIST_URL'] + '/api/v1/clouds/' + cloud_id + '/machines/' + machine['id']
            requests.post(uri, data=json.dumps(payload), headers=headers)


def kill_orchestration_machines(context):
    api_token = get_api_token(context)
    headers = {'Authorization': api_token}

    response = requests.get("%s/api/v1/clouds" % context.mist_config['MIST_URL'], headers=headers)
    for cloud in response.json():
        if 'digitalocean' in cloud['provider']:
            cloud_id = cloud['id']
            uri = context.mist_config['MIST_URL'] + '/api/v1/clouds/' + cloud_id + '/machines'
            response = requests.get(uri, headers=headers)
            kill_yolomachine(context, response.json(), headers, cloud_id)


def delete_schedules(context):
    log.info('Deleting schedule...')
    api_token = get_api_token(context)
    headers = {'Authorization': api_token}

    response = requests.get("%s/api/v1/schedules" % context.mist_config['MIST_URL'], headers=headers)
    for schedule in response.json():
        uri = context.mist_config['MIST_URL'] + '/api/v1/schedules/' + schedule['id']
        requests.delete(uri, headers=headers)


def start_ui_machines(context):
    log.info('Starting ui-docker machines...')
    api_token = get_api_token(context)
    headers = {'Authorization': api_token}
    response = requests.get("%s/api/v1/clouds" % context.mist_config['MIST_URL'], headers=headers)
    for cloud in response.json():
        if 'docker' in cloud['provider']:
            uri = context.mist_config['MIST_URL'] + '/api/v1/clouds/' + cloud['id'] + '/machines'
            response = requests.get(uri, headers=headers)
            for machine in response.json():
                if 'ui-testing' in machine['name']:
                    log.info('Starting ui-testing machine...')
                    payload = {'action': 'start'}
                    uri = context.mist_config['MIST_URL'] + '/api/v1/clouds/' + cloud['id'] + '/machines/' + machine['id']
                    requests.post(uri, data=json.dumps(payload), headers=headers)


def finish_and_cleanup(context):
    dump_js_console_log(context)
    context.mist_config['browser'].quit()
    if context.mist_config.get('browser2'):
        context.mist_config['browser2'].quit()
    if context.mist_config.get('recording_session', False):
        stop_recording()


def after_feature(context, feature):
    if 'Orchestration' in feature.name:
        kill_orchestration_machines(context)
    if 'Schedulers' in feature.name:
        delete_schedules(context)
        start_ui_machines(context)