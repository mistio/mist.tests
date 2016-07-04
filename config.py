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
import sys
import json
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
test_settings = {}
try:
    execfile("test_settings.py", test_settings)
except IOError:
    log.warning("No test_settings.py file found.")
except Exception as exc:
    log.error("Error parsing test_settings py: %r", exc)


def get_value_of(name_of_variable, default_value):
    """
    Check in environment if the variable is set and return it's value
    otherwise check if it is available in the test_settings. Finally, use the
    default value if it's not available anywhere else.
    :param name_of_variable: the name of the variable to be searched in env or test_settings
    :param default_value: the default value if no other value is found
    :return:
    """
    env_var = os.environ.get(name_of_variable)
    if env_var is not None:
        try:
            env_var = json.loads(env_var)
        except ValueError as e:
            log.error("Could not decode value of variable %s(%s)" %
                      (name_of_variable, env_var))
            raise e
        log.info("Retrieved value from env for variable with name %s: %s" %
                 (name_of_variable, env_var))
        return env_var
    return test_settings.get(name_of_variable, default_value)

LOCAL = get_value_of("LOCAL", True)

BROWSER_LOCAL = get_value_of("BROWSER_LOCAL", True)

DEBUG = get_value_of("DEBUG", False)

BROWSER_FLAVOR = get_value_of("BROWSER_FLAVOR", "chrome")

# Directories and paths used for the tests
BASE_DIR = get_value_of("BASE_DIR", os.getcwd())

LOG_DIR = get_value_of("LOG_DIR", 'var/log/')

TEST_DIR = get_value_of("TEST_DIR",
                        os.path.join(BASE_DIR, 'src/mist/io/tests'))

MAIL_PATH = get_value_of("MAIL_PATH",
                         os.path.join(BASE_DIR, 'var/mail/'))

JS_CONSOLE_LOG = get_value_of("JS_CONSOLE_LOG",
                              os.path.join(BASE_DIR, LOG_DIR,
                                           'js_console.log'))

SCREENSHOT_PATH = get_value_of("SCREENSHOT_PATH",
                               os.path.join(BASE_DIR, 'error'))

# This is the path to the json file used for the multi-provisioning tests
MP_DB_DIR = get_value_of("MP_DB_DIR", os.path.join(BASE_DIR, 'mp_db.json'))

if BROWSER_FLAVOR == 'chrome':
    if 'darwin' in sys.platform:
        WEBDRIVER_PATH = os.path.join(BASE_DIR,
                                      'parts/chromedriver-mac/chromedriver-mac')
    else:
        WEBDRIVER_PATH = os.path.join(BASE_DIR,
                                      'parts/chromedriver/chromedriver')
elif BROWSER_FLAVOR == 'phantomjs':
    WEBDRIVER_PATH = os.path.join(BASE_DIR, 'parts/envuiphantomjs')

WEBDRIVER_LOG = get_value_of("WEBDRIVER_LOG",
                             os.path.join(BASE_DIR, LOG_DIR,
                                          'chromedriver.log'))

# ----------CREDENTIALS-----------
CREDENTIALS = get_value_of("CREDENTIALS", {})

MIST_API_TOKEN = get_value_of("MIST_API_TOKEN", "")

MIST_URL = get_value_of("MIST_URL", "http://localhost:8000")

NAME = get_value_of("NAME", "Atheofovos Gkikas")

# DEFAULT CREDENTIALS FOR ACCESSING MIST.CORE
EMAIL = get_value_of("EMAIL", "")
PASSWORD1 = get_value_of("PASSWORD1", "")
PASSWORD2 = get_value_of("PASSWORD2", "")

DEMO_EMAIL = get_value_of("DEMO_EMAIL", "")
DEMO_PASSWORD = get_value_of("DEMO_PASSWORD", "")

MIST_DEMO_REQUEST_EMAIL = get_value_of("MIST_DEMO_REQUEST_EMAIL",
                                       "demo@mist.io")

# CREDENTIALS FOR TESTING RBAC
RBAC_OWNER_EMAIL = get_value_of("RBAC_OWNER_EMAIL", "owner@dr.dr")
RBAC_OWNER_PASSWORD = get_value_of("RBAC_OWNER_PASSWORD ", "dr")

RBAC_MEMBER_EMAIL = get_value_of("RBAC_MEMBER_EMAIL", "user@dr.dr")
RBAC_MEMBER_PASSWORD = get_value_of("RBAC_MEMBER_PASSWORD", "dr")

# CREDENTIALS FOR GOOGLE SSO
GOOGLE_TEST_EMAIL = get_value_of("GOOGLE_TEST_EMAIL", "")
GOOGLE_TEST_PASSWORD = get_value_of("GOOGLE_TEST_PASSWORD", "")

# CREDENTIALS FOR GITHUB SSO
GITHUB_TEST_EMAIL = get_value_of("GITHUB_TEST_EMAIL", "")
GITHUB_TEST_PASSWORD = get_value_of("GITHUB_TEST_PASSWORD", "")

# CREDENTIALS FOR TESTING REGISTRATION THROUGH SSO
GOOGLE_REGISTRATION_TEST_EMAIL = get_value_of(
    "GOOGLE_REGISTRATION_TEST_EMAIL", "")
GOOGLE_REGISTRATION_TEST_PASSWORD = get_value_of(
    "GOOGLE_REGISTRATION_TEST_PASSWORD", "")

GITHUB_REGISTRATION_TEST_EMAIL = get_value_of(
    "GITHUB_REGISTRATION_TEST_EMAIL", "")
GITHUB_REGISTRATION_TEST_PASSWORD = get_value_of(
    "GITHUB_REGISTRATION_TEST_PASSWORD", "")

OWNER_EMAIL = get_value_of("OWNER_EMAIL", "")
OWNER_PASSWORD = get_value_of("OWNER_PASSWORD", "")

MEMBER1_EMAIL = get_value_of("MEMBER1_EMAIL", "")
MEMBER1_PASSWORD = get_value_of("MEMBER1_PASSWORD", "")

MEMBER2_EMAIL = get_value_of("MEMBER2_EMAIL", "")
MEMBER2_PASSWORD = get_value_of("MEMBER2_PASSWORD", "")

API_TESTS_PRIVATE_KEY = get_value_of("API_TESTS_PRIVATE_KEY", '')

API_TESTS_PUBLIC_KEY = get_value_of("API_TESTS_PUBLIC_KEY", '')

API_TESTING_MACHINE_PRIVATE_KEY = get_value_of(
    "API_TESTING_MACHINE_PRIVATE_KEY", '')

API_TESTING_MACHINE_PUBLIC_KEY = get_value_of(
    "API_TESTING_MACHINE_PUBLIC_KEY", '')

API_TESTING_MACHINE_NAME = get_value_of("API_TESTING_MACHINE_NAME", '')

API_TESTING_CLOUD = get_value_of('API_TESTING_CLOUD', '')

API_TESTING_CLOUD_PROVIDER = get_value_of('API_TESTING_CLOUD_PROVIDER', '')

ORG_NAME = get_value_of('ORG_NAME', '')

SETUP_ENVIRONMENT = get_value_of("SETUP_ENVIRONMENT", False)

WEBDRIVER_OPTIONS = get_value_of('WEBDRIVER_OPTIONS',
                                 ['--dns-prefetch-disable'])

REGISTER_USER_BEFORE_FEATURE = get_value_of('REGISTER_USER_BEFORE_FEATURE',
                                            False)
