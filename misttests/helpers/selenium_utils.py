import json

from misttests import config

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.remote.errorhandler import NoSuchWindowException

import logging

log = logging.getLogger(__name__)


def choose_driver(flavor=None):
    """
    Returns an instance of a remote selenium driver
    """

    flavor = flavor if flavor is not None else config.BROWSER_FLAVOR

    log.info("Initializing driver")
    if flavor == "firefox":
        driver = webdriver.Firefox()
    elif flavor == "chrome":
        service_args = ['--verbose']
        chrome_options = Options()
        for opt in config.WEBDRIVER_OPTIONS:
            chrome_options.add_argument(opt)
        # driver = webdriver.Chrome(service_args=service_args,
        #                           chrome_options=chrome_options,
        #                           executable_path=config.WEBDRIVER_PATH,
        #                           service_log_path=config.WEBDRIVER_LOG)
        driver = webdriver.Chrome()

    elif flavor == "phantomjs":
        driver = webdriver.PhantomJS(executable_path=config.WEBDRIVER_PATH)
    else:
        raise Exception("%s is not supported!" % flavor)

    return driver


def get_screenshot(context):
    if context.mist_config['NON_STOP']:
        num = context.mist_config['ERROR_NUM'] = context.mist_config['ERROR_NUM'] + 1
        path = context.mist_config['SCREENSHOT_PATH'] + '.{0}.png'.format(str(num))
    else:
        path = context.mist_config['SCREENSHOT_PATH'] + '.png'
    try:
        context.browser.get_screenshot_as_file(path)
    except NoSuchWindowException:
        pass


def dump_js_console_log(context):
    if context.mist_config['BROWSER_FLAVOR'] == 'chrome':
        js_console_logs = context.mist_config['browser'].get_log('browser')
        formatted_js_console_logs = json.dumps(js_console_logs, indent=5)
        fp = open(context.mist_config['JS_CONSOLE_LOG'], 'w')
        fp.write(formatted_js_console_logs)
        fp.close()
