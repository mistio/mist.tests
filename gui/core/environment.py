import sys
import json
import logging

from tests import config

from tests.helpers.selenium_utils import choose_driver

from selenium.webdriver.remote.errorhandler import NoSuchWindowException

log = logging.getLogger(__name__)

logging.basicConfig(level=config.logging.INFO)


def before_all(context):
    """
    Load the configuration config and setup the context
    """
    log.info("Starting before all hook")

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
    context.mist_config['RBAC_OWNER_EMAIL'] = config.RBAC_OWNER_EMAIL
    context.mist_config['RBAC_OWNER_PASSWORD'] = config.RBAC_OWNER_PASSWORD
    context.mist_config['RBAC_MEMBER_EMAIL'] = config.RBAC_MEMBER_EMAIL
    context.mist_config['RBAC_MEMBER_PASSWORD'] = config.RBAC_MEMBER_PASSWORD
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
    log.info("Finished with before_all hook. Starting tests")
    log.info("Webdriver path:" + config.WEBDRIVER_PATH)
    log.info("Webdriver log:" + config.WEBDRIVER_LOG)
    log.info("JS console log:" + config.JS_CONSOLE_LOG)


def before_feature(context, feature):
    if config.REGISTER_USER_BEFORE_FEATURE:
        context.execute_steps(u'Given user with email "EMAIL" is registered')


def after_scenario(context, scenario):
    if scenario.status == 'failed':
        if context.mist_config['NON_STOP']:
            num = context.mist_config['ERROR_NUM'] = context.mist_config['ERROR_NUM'] + 1
            try:
                context.browser.get_screenshot_as_file(context.mist_config['SCREENSHOT_PATH'] + '.{0}.png'.format(str(num)))
            except NoSuchWindowException:
                pass
        else:
            try:
                context.browser.get_screenshot_as_file(context.mist_config['SCREENSHOT_PATH'] + '.png')
            except NoSuchWindowException:
                pass


def after_all(context):
    if context.mist_config['BROWSER_FLAVOR'] == 'chrome':
        js_console_logs = context.mist_config['browser'].get_log('browser')
        formatted_js_console_logs = json.dumps(js_console_logs, indent=5)
        fp = open(context.mist_config['JS_CONSOLE_LOG'], 'w')
        fp.write(formatted_js_console_logs)
        fp.close()
    context.mist_config['browser'].quit()
    if context.mist_config.get('browser2'):
        context.mist_config['browser2'].quit()
