import os
import json
import logging

from misttests import config

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.errorhandler import NoSuchWindowException

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
        options = webdriver.ChromeOptions()
        options.binary_location = '/usr/bin/google-chrome'
        for opt in config.WEBDRIVER_OPTIONS:
            options.add_argument(opt)
        driver = webdriver.Chrome(chrome_options=options)

    elif flavor == "phantomjs":
        driver = webdriver.PhantomJS(executable_path=config.WEBDRIVER_PATH)

    else:
        raise Exception("%s is not supported!" % flavor)

    return driver


def produce_video_artifact(context, step):
    feature = context.feature.name.replace(' ', '_')
    filename = context.mist_config['ARTIFACTS_PATH'] + '/' + feature + '.mp4'
    if os.path.isfile(filename):
        os.remove(filename)
    log.info('Producing video...')
    os.system('ffmpeg -loglevel panic -framerate 4 -pattern_type glob \
                      -i "%s/%s-*.png" -c:v libx264 -r 30 %s' %
              (context.mist_config['ARTIFACTS_PATH'], feature, filename))
    log.info('http://172.17.0.1:8222/' + filename.replace('/data/', ''))


def get_screenshot(context, step):
    feature = context.feature.name.replace(' ', '_')
    if not os.path.isdir(context.mist_config['ARTIFACTS_PATH']):
        os.mkdir(context.mist_config['ARTIFACTS_PATH'])
    num = context.mist_config['ERROR_NUM'] = context.mist_config['ERROR_NUM'] + 1
    path = context.mist_config['ARTIFACTS_PATH'] + '/' + feature + '-{0}.png'.format(str(num).zfill(4))
    try:
        context.browser.save_screenshot(path)
    except NoSuchWindowException:
        pass


def get_error_screenshot(context, step):
    feature = context.feature.name.replace(' ', '_')
    try:
        path = context.mist_config['ARTIFACTS_PATH'] + '/' + feature + '__error.png'
        context.browser.save_screenshot(path)
    except NoSuchWindowException:
        pass
    log.info('http://172.17.0.1:8222/' + path.replace('/data/', ''))


def dump_js_console_log(context):
    if context.mist_config['BROWSER_FLAVOR'] == 'chrome':
        js_console_logs = context.mist_config['browser'].get_log('browser')
        formatted_js_console_logs = json.dumps(js_console_logs, indent=5)
        fp = open(context.mist_config['JS_CONSOLE_LOG'], 'w')
        fp.write(formatted_js_console_logs)
        fp.close()
