# DEFAULT SETTINGS FOR THE TESTS
#
# ****     **** **  ******** **********
# /**/**   **/**/** **////// /////**///
# /**//** ** /**/**/**           /**
# /** //***  /**/**/*********    /**
# /**  //*   /**/**////////**    /**
# /**   /    /**/**       /**    /**
# /**        /**/** ********     /**
# //         // // ////////      //
#
# ********** ********  ******** ******************
# /////**/// /**/////  **////// /////**///**//////
#     /**    /**      /**           /**    /**
#     /**    /******* /*********    /**    /*********
#     /**    /**////  ////////**    /**    ////////**
#     /**    /**             /**    /**           /**
#     /**    /******** ********     /**     ********
#     //     //////// ////////      //     ////////


import os
import ast
import sys
import string
import random
import logging
import requests

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

settings_file = os.getenv('TEST_SETTINGS_FILE') or 'test_settings.py'
test_settings = {}
try:
    execfile(settings_file, test_settings)
except IOError:
    log.warning("No test_settings.py file found.")
except Exception as exc:
    log.error("Error parsing test_settings py: %r", exc)

# -- Use Vault in run_tests.sh (make it interactive, no need for test_settings.py)


def get_var_from_vault(path, var):

    print os.environ['username']

    re = requests.post(VAULT_SERVER + '/v1/auth/userpass/login/%s') %os.environ['username']

    headers = {"X-Vault-Token": VAULT_TOKEN}

    re = requests.get(VAULT_SERVER + '/v1/secret/%s' %path, headers=headers)

    json_data = re.json().get('data')
    return json_data.get(var)


def get_setting(setting, default_value=None, priority='config_file'):

    if default_value is None:
        default_value = ''

    if priority in ['env', 'environ', 'environment']:
        setting = os.environ.get(setting) or test_settings.get(setting, default_value)
    else:
        setting = test_settings.get(setting, os.environ.get(setting, default_value))

    if type(setting) == type(default_value):
        return setting

    if type(default_value) == str:
        return str(setting)
    elif type(default_value) == list:
        return [setting]
    elif type(default_value) == int:
        return int(setting)
    elif type(default_value) == dict:
        return ast.literal_eval(setting)
    elif type(default_value) == bool:
        return True if setting in ["True", "true"] else False

LOCAL = get_setting("LOCAL", True)

VAULT_TOKEN = get_setting("VAULT_TOKEN", "")

VAULT_SERVER = get_setting("VAULT_SERVER", "")

VAULT_USERNAME = get_setting("VAULT_USERNAME", "")

DEBUG = get_setting("DEBUG", False)

RECORD_SELENIUM = get_setting("RECORD_SELENIUM", False)

# Directories and paths used for the tests
BASE_DIR = get_setting("BASE_DIR", os.getcwd())

LOG_DIR = get_setting("LOG_DIR", '/var/log/')

MAIL_DIR = get_setting("MAIL_DIR", '/var/mail/')

TEST_DIR = get_setting("TEST_DIR",
                        os.path.join(BASE_DIR, 'tests'))

MAIL_PATH = get_setting("MAIL_PATH", MAIL_DIR)

JS_CONSOLE_LOG = get_setting("JS_CONSOLE_LOG", '/var/log/js_console.log')

SCREENSHOT_PATH = get_setting("SCREENSHOT_PATH", '/var/log/error')

DISPLAY_NUM = get_setting("DISPLAY_NUM", "1")

# This is the path to the json file used for the multi-provisioning tests
MP_DB_DIR = get_setting("MP_DB_DIR", os.path.join(BASE_DIR, 'mp_db.json'))

BROWSER_FLAVOR = get_setting("BROWSER_FLAVOR", "chrome")

default_browser_path = BASE_DIR
if BROWSER_FLAVOR == 'chrome':
    default_browser_path = os.path.join(default_browser_path,
                                        'parts/chromedriver/chromedriver')
    if 'darwin' in sys.platform:
        default_browser_path += '-mac'

elif BROWSER_FLAVOR == 'phantomjs':
    default_browser_path = os.path.join(default_browser_path, 'parts/envuiphantomjs')

WEBDRIVER_PATH = get_setting("WEBDRIVER_PATH", "/usr/local/bin/chromedriver")

WEBDRIVER_LOG = get_setting("WEBDRIVER_LOG",
                             os.path.join(BASE_DIR, LOG_DIR,
                                          'chromedriver.log'))

# ----------CREDENTIALS-----------
CREDENTIALS = get_setting("CREDENTIALS", {})

MIST_API_TOKEN = get_setting("MIST_API_TOKEN", "")

MIST_URL = get_setting("MIST_URL", "http://localhost:8000")
VPN_URL = get_setting("VPN_URL", "")

NAME = get_setting("NAME", "Atheofovos Gkikas")

# -----------MAYDAY------------------
MAYDAY_MACHINE = get_setting("MAYDAY_MACHINE", "")

# DEFAULT CREDENTIALS FOR ACCESSING MIST.CORE
BASE_EMAIL = get_setting("BASE_EMAIL", "fatboy.tester.mist.io")
GMAIL_FATBOY_USER = get_setting("GMAIL_FATBOY_USER", "%s@gmail.com" % BASE_EMAIL)
GMAIL_FATBOY_PASSWORD = get_setting("GMAIL_FATBOY_PASSWORD", "")
EMAIL = get_setting("EMAIL", "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1,200000)))
PASSWORD1 = get_setting("PASSWORD1",
                        ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)))
PASSWORD2 = get_setting("PASSWORD2",
                        ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)))

DEMO_EMAIL = get_setting("DEMO_EMAIL", "")
DEMO_PASSWORD = get_setting("DEMO_PASSWORD", "")

MIST_DEMO_REQUEST_EMAIL = get_setting("MIST_DEMO_REQUEST_EMAIL",
                                      "demo@mist.io")

# CREDENTIALS FOR TESTING RBAC
OWNER_EMAIL = get_setting("OWNER_EMAIL", "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1,200000)))
OWNER_PASSWORD = get_setting("OWNER_PASSWORD", ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)))

MEMBER1_EMAIL = get_setting("MEMBER1_EMAIL", "")
MEMBER1_PASSWORD = get_setting("MEMBER1_PASSWORD", PASSWORD1)

MEMBER2_EMAIL = get_setting("MEMBER2_EMAIL", "")
MEMBER2_PASSWORD = get_setting("MEMBER2_PASSWORD", PASSWORD1)

# CREDENTIALS FOR GOOGLE SSO
GOOGLE_TEST_EMAIL = get_setting("GOOGLE_TEST_EMAIL", "")
GOOGLE_TEST_PASSWORD = get_setting("GOOGLE_TEST_PASSWORD", "")

# CREDENTIALS FOR GITHUB SSO
GITHUB_TEST_EMAIL = get_setting("GITHUB_TEST_EMAIL", "")
GITHUB_TEST_PASSWORD = get_setting("GITHUB_TEST_PASSWORD", "")

# CREDENTIALS FOR TESTING REGISTRATION THROUGH SSO
GOOGLE_REGISTRATION_TEST_EMAIL = get_setting(
    "GOOGLE_REGISTRATION_TEST_EMAIL", "")
GOOGLE_REGISTRATION_TEST_PASSWORD = get_setting(
    "GOOGLE_REGISTRATION_TEST_PASSWORD", "")

GITHUB_REGISTRATION_TEST_EMAIL = get_setting(
    "GITHUB_REGISTRATION_TEST_EMAIL", "")
GITHUB_REGISTRATION_TEST_PASSWORD = get_setting(
    "GITHUB_REGISTRATION_TEST_PASSWORD", "")

API_TESTS_PRIVATE_KEY = get_setting("API_TESTS_PRIVATE_KEY", '')

API_TESTS_PUBLIC_KEY = get_setting("API_TESTS_PUBLIC_KEY", '')

API_TESTING_MACHINE_PRIVATE_KEY = get_setting(
    "API_TESTING_MACHINE_PRIVATE_KEY", '')

API_TESTING_MACHINE_PUBLIC_KEY = get_setting(
    "API_TESTING_MACHINE_PUBLIC_KEY", '')

API_TESTING_MACHINE_NAME = get_setting("API_TESTING_MACHINE_NAME", '')

API_TESTING_CLOUD = get_setting('API_TESTING_CLOUD', '')

API_TESTING_CLOUD_PROVIDER = get_setting('API_TESTING_CLOUD_PROVIDER', '')

ORG_NAME = get_setting('ORG_NAME', '')

ORG_ID = get_setting('ORG_ID', '')

SETUP_ENVIRONMENT = get_setting("SETUP_ENVIRONMENT", False)

WEBDRIVER_OPTIONS = get_setting('WEBDRIVER_OPTIONS',
                                 ['--dns-prefetch-disable'])

REGISTER_USER_BEFORE_FEATURE = get_setting('REGISTER_USER_BEFORE_FEATURE', True, priority='environment')

IMAP_SERVER = get_setting('IMAP_SERVER', 'imap.gmail.com', priority='environment')

IMAP_USE_SSL = get_setting('IMAP_USE_SSL', True, priority='environment')

IMAP_USER = get_setting('IMAP_USER', EMAIL)

IMAP_PASSWORD = get_setting('IMAP_PASSWORD', '')

KEY_ID = get_setting('KEY_ID', '')
