import sys
import json
import requests
import logging

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
    context.mist_config['EMAIL'] = config.EMAIL
    context.mist_config['PASSWORD1'] = config.PASSWORD1
    context.mist_config['PASSWORD2'] = config.PASSWORD2
    context.mist_config['SETUP_ENVIRONMENT'] = config.SETUP_ENVIRONMENT
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
    context.mist_config['ORG_NAME'] = config.ORG_NAME
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
    log.info("Finished with the bulk of the test settings")
    if config.LOCAL:
        log.info("Initializing behaving mail for path: %s" % config.MAIL_PATH)
        from behaving.mail import environment as behaving_mail
        # with this behaving will get the path to save and retrieve mails
        context.mail_path = config.MAIL_PATH
        # calling behaving to setup it's context variables.
        behaving_mail.before_all(context)

    if config.RECORD_SELENIUM:
        start_recording()

    context.mist_config['recording_session'] = config.RECORD_SELENIUM
    log.info("Finished with before_all hook. Starting tests")


def before_feature(context, feature):
    if config.REGISTER_USER_BEFORE_FEATURE:
        payload = {
            'email': context.mist_config['EMAIL'],
            'password': context.mist_config['PASSWORD1'],
            'name': "Atheofovos Gkikas"
        }

        re = requests.post("%s/api/v1/dev/register" % context.mist_config['MIST_URL'], data=json.dumps(payload))
        log.error("REEEEEEEE")
        log.error(re.status)

        # try:
        #     context.execute_steps(u'Given user with email "EMAIL" is registered')
        # except Exception as e:
        #     finish_and_cleanup(context)
        #     raise e


def after_all(context):
    log.error("USER: %s" % context.mist_config['EMAIL'])
    log.error("PASSWORD1: %s" % context.mist_config['PASSWORD1'])
    log.error(context.mist_config['REGISTER_USER_BEFORE_FEATURE'])
    finish_and_cleanup(context)


def finish_and_cleanup(context):
    dump_js_console_log(context)
    try:
        get_screenshot(context)
    except Exception as e:
        log.error("Could not get screen shot: %s" % repr(e))
        pass
    context.mist_config['browser'].quit()
    if context.mist_config.get('browser2'):
        context.mist_config['browser2'].quit()
    if context.mist_config.get('recording_session', False):
        stop_recording()
