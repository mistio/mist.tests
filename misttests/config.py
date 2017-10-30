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

# TODO: modify so that it can parse nested objects as well
def safe_get_var(vault_path, vault_key, test_settings_var = None):

    if VAULT_ENABLED:

        headers = {"X-Vault-Token": os.environ['VAULT_CLIENT_TOKEN']}

        re = requests.get(VAULT_SERVER + '/v1/secret/%s' % vault_path, headers=headers)

        json_data = re.json().get('data')

        return json_data.get(vault_key)

    else:

        return test_settings_var


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

VAULT_ENABLED = get_setting("VAULT_ENABLED", True, priority='environment')

VAULT_SERVER = get_setting("VAULT_SERVER", "https://vault.ops.mist.io:8200")

DEBUG = get_setting("DEBUG", False)

RECORD_SELENIUM = get_setting("RECORD_SELENIUM", True)

LOCAL_DOCKER = get_setting("LOCAL_DOCKER","api")

# Directories and paths used for the tests
BASE_DIR = get_setting("BASE_DIR", os.getcwd())

LOG_DIR = get_setting("LOG_DIR", '/var/log/')

MAIL_DIR = get_setting("MAIL_DIR", '/var/mail/')

TEST_DIR = get_setting("TEST_DIR",
                        os.path.join(BASE_DIR, 'tests'))

MAIL_PATH = get_setting("MAIL_PATH", MAIL_DIR)

JS_CONSOLE_LOG = get_setting("JS_CONSOLE_LOG", '/var/log/js_console.log')

SCREENSHOT_PATH = os.getenv('DATADIR') or get_setting("SCREENSHOT_PATH", 'artifacts/screenshot')

ARTIFACTS_PATH = os.getenv('DATADIR') or get_setting("ARTIFACTS_PATH", 'artifacts')

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

MIST_API_TOKEN = get_setting("MIST_API_TOKEN", "")

MIST_URL = get_setting("MIST_URL", "http://localhost:8000")
VPN_URL = get_setting("VPN_URL", "")

NAME = get_setting("NAME", "Atheofovos Gkikas")

# -----------MAYDAY------------------
MAYDAY_MACHINE = get_setting("MAYDAY_MACHINE", "")

# DEFAULT CREDENTIALS FOR ACCESSING MIST.CORE
BASE_EMAIL = get_setting("BASE_EMAIL", "thingirl.tester.mist.io")
GMAIL_THINGIRL_USER = get_setting("GMAIL_THINGIRL_USER", "%s@gmail.com" % BASE_EMAIL)
GMAIL_THINGIRL_PASSWORD = get_setting("GMAIL_THINGIRL_PASSWORD", "")
EMAIL = get_setting("EMAIL", "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1,200000)))
PASSWORD1 = get_setting("PASSWORD1",
                        ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20)))
PASSWORD2 = get_setting("PASSWORD2",
                        ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20)))
CHANGED_PASSWORD = get_setting("CHANGED_PASSWORD",
                        ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20)))

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

TESTING_PRIVATE_KEY = get_setting(
    "TESTING_PRIVATE_KEY", '')

API_TESTING_MACHINE_PUBLIC_KEY = get_setting(
    "API_TESTING_MACHINE_PUBLIC_KEY", '')

API_TESTING_MACHINE_NAME = get_setting("API_TESTING_MACHINE_NAME", '')

API_TESTING_CLOUD = get_setting('API_TESTING_CLOUD', '')

API_TESTING_CLOUD_PROVIDER = get_setting('API_TESTING_CLOUD_PROVIDER', '')

ORG_NAME = get_setting('ORG_NAME', '')

ORG_ID = get_setting('ORG_ID', '')

SETUP_ENVIRONMENT = get_setting("SETUP_ENVIRONMENT", False)

WEBDRIVER_OPTIONS = get_setting('WEBDRIVER_OPTIONS',
                                ['headless', 'no-sandbox', 'disable-gpu',
                                 'window-size=1920x1080'])

REGISTER_USER_BEFORE_FEATURE = get_setting('REGISTER_USER_BEFORE_FEATURE', True, priority='environment')

IMAP_SERVER = get_setting('IMAP_SERVER', 'imap.gmail.com', priority='environment')

IMAP_USE_SSL = get_setting('IMAP_USE_SSL', True, priority='environment')

IMAP_USER = get_setting('IMAP_USER', EMAIL)

IMAP_PASSWORD = get_setting('IMAP_PASSWORD', '')

KEY_ID = get_setting('KEY_ID', '')

DEFAULT_CREDENTIALS = {'AWS': {'api_key': '', 'api_secret': '', 'region': ''},
                       'AWS_2': {'api_key': '', 'api_secret': '', 'region': ''},
                       'KVM': {'key': """ """, 'hostname': ''},
                       'AZURE': {'certificate': """ """, 'subscription_id': ''},
                       'AZURE_ARM': {'client_key': '', 'client_secret': '', 'subscription_id': '', 'tenant_id': ''},
                       'DIGITALOCEAN': {'token': ''},
                       'DOCKER': {'authentication': '', 'ca': """ """, 'cert': """ """, 'host': '', 'key': """""", 'port': ''},
                       'EC2': {'api_key': '', 'api_secret': '', 'region': ''},
                       'LINODE': {'api_key': ''},
                       'NEPHOSCALE': {'password': '', 'username': ''},
                       'GCE': {'project_id': '', 'private_key': {}},
                       'OPENSTACK': {'auth_url': '', 'password': '', 'tenant': '', 'username': ''},
                       'DOCKER_ORCHESTRATOR':{"host": "", "port": ""},
                       'OPENSTACK_2': {'auth_url': '', 'password': '', 'tenant': '', 'username': ''},
                       'PACKET': {'api_key': ''},
                       'PACKET_2': {'api_key': ''},
                       'VMWARE': {'username': '', 'password': '', 'organization': '', 'host': '' },
                       'RACKSPACE': {'api_key': '', 'region': '', 'username': ''},
                       'SOFTLAYER': {'api_key': '', 'username': ''},
                       'VULTR': {'apikey': ''},
                       'DOCKER_MONITORING':{'host': '', 'port': ''},
                       'ONAPP':{'username':'', 'password':'', 'host':'', 'verify_ssl': False}
                       }

CREDENTIALS = get_setting("CREDENTIALS", DEFAULT_CREDENTIALS)
