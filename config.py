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
import logging

log = logging.getLogger(__name__)
test_settings = {}
try:
    execfile("test_settings.py", test_settings)
except IOError:
    log.warning("No test_settings.py file found.")
except Exception as exc:
    log.error("Error parsing test_settings py: %r", exc)

LOCAL = test_settings.get("LOCAL", True)

BROWSER_LOCAL = test_settings.get("BROWSER_LOCAL", True)

DEBUG = test_settings.get("DEBUG", False)

BROWSER_FLAVOR = test_settings.get("BROWSER_FLAVOR", "chrome")

# If LOCAL == False, you have to provide the selenium-hub
selenium_hub = test_settings.get("selenium_hub", "")

# Directories and paths used for the tests
BASE_DIR = test_settings.get("BASE_DIR", os.getcwd())

LOG_DIR = test_settings.get("LOG_DIR", 'var/log/')

TEST_DIR = test_settings.get("TEST_DIR",
                             os.path.join(BASE_DIR, 'src/mist/io/tests'))

MAIL_PATH = test_settings.get("MAIL_PATH",
                              os.path.join(BASE_DIR, 'var/mail/'))

JS_CONSOLE_LOG = test_settings.get("JS_CONSOLE_LOG",
                                   os.path.join(BASE_DIR, LOG_DIR,
                                                'js_console.log'))

SCREENSHOT_PATH = test_settings.get("SCREENSHOT_PATH",
                                    os.path.join(BASE_DIR, 'error'))

# This is the path to the json file used for the multi-provisioning tests
MP_DB_DIR = test_settings.get("MP_DB_DIR", os.path.join(BASE_DIR, 'mp_db.json'))

if BROWSER_FLAVOR == 'chrome':
    if 'darwin' in sys.platform:
        WEBDRIVER_PATH = os.path.join(BASE_DIR,
                                      'parts/chromedriver-mac/chromedriver-mac')
    else:
        WEBDRIVER_PATH = os.path.join(BASE_DIR,
                                      'parts/chromedriver/chromedriver')
elif BROWSER_FLAVOR == 'phantomjs':
    WEBDRIVER_PATH = os.path.join(BASE_DIR, 'parts/envuiphantomjs')

WEBDRIVER_LOG = test_settings.get("WEBDRIVER_LOG",
                                  os.path.join(BASE_DIR, LOG_DIR,
                                               'chromedriver.log'))

# ----------CREDENTIALS-----------
CREDENTIALS = test_settings.get("CREDENTIALS", {})

MIST_API_TOKEN = test_settings.get("MIST_API_TOKEN", "")

MIST_URL = test_settings.get("MIST_URL", "http://localhost:8000")
VPN_URL = test_settings.get("VPN_URL", "")

NAME = test_settings.get("NAME", "Atheofovos Gkikas")

# DEFAULT CREDENTIALS FOR ACCESSING MIST.CORE
EMAIL = test_settings.get("EMAIL", "")
PASSWORD1 = test_settings.get("PASSWORD1", "")
PASSWORD2 = test_settings.get("PASSWORD2", "")

DEMO_EMAIL = test_settings.get("DEMO_EMAIL", "")
DEMO_PASSWORD = test_settings.get("DEMO_PASSWORD", "")

MIST_DEMO_REQUEST_EMAIL = test_settings.get("MIST_DEMO_REQUEST_EMAIL", "demo@mist.io")

# CREDENTIALS FOR TESTING RBAC
RBAC_OWNER_EMAIL = test_settings.get("RBAC_OWNER_EMAIL", "owner@dr.dr")
RBAC_OWNER_PASSWORD  = test_settings.get("RBAC_OWNER_PASSWORD ", "dr")

RBAC_MEMBER_EMAIL = test_settings.get("RBAC_MEMBER_EMAIL", "user@dr.dr")
RBAC_MEMBER_PASSWORD = test_settings.get("RBAC_MEMBER_PASSWORD", "dr")

# CREDENTIALS FOR GOOGLE SSO
GOOGLE_TEST_EMAIL = test_settings.get("GOOGLE_TEST_EMAIL", "")
GOOGLE_TEST_PASSWORD = test_settings.get("GOOGLE_TEST_PASSWORD", "")

# CREDENTIALS FOR GITHUB SSO
GITHUB_TEST_EMAIL = test_settings.get("GITHUB_TEST_EMAIL", "")
GITHUB_TEST_PASSWORD = test_settings.get("GITHUB_TEST_PASSWORD", "")

# CREDENTIALS FOR TESTING REGISTRATION THROUGH SSO
GOOGLE_REGISTRATION_TEST_EMAIL = test_settings.get(
    "GOOGLE_REGISTRATION_TEST_EMAIL", "")
GOOGLE_REGISTRATION_TEST_PASSWORD = test_settings.get(
    "GOOGLE_REGISTRATION_TEST_PASSWORD", "")

GITHUB_REGISTRATION_TEST_EMAIL = test_settings.get(
    "GITHUB_REGISTRATION_TEST_EMAIL", "")
GITHUB_REGISTRATION_TEST_PASSWORD = test_settings.get(
    "GITHUB_REGISTRATION_TEST_PASSWORD", "")

OWNER_EMAIL = test_settings.get("OWNER_EMAIL", "")
OWNER_PASSWORD = test_settings.get("OWNER_PASSWORD", "")

MEMBER1_EMAIL = test_settings.get("MEMBER1_EMAIL", "")
MEMBER1_PASSWORD = test_settings.get("MEMBER1_PASSWORD", "")

MEMBER2_EMAIL = test_settings.get("MEMBER2_EMAIL", "")
MEMBER2_PASSWORD = test_settings.get("MEMBER2_PASSWORD", "")

API_TESTS_PRIVATE_KEY = test_settings.get("API_TESTS_PRIVATE_KEY", '')

API_TESTS_PUBLIC_KEY = test_settings.get("API_TESTS_PUBLIC_KEY", '')

API_TESTING_MACHINE_PRIVATE_KEY = test_settings.get(
    "API_TESTING_MACHINE_PRIVATE_KEY", '')

API_TESTING_MACHINE_PUBLIC_KEY = test_settings.get(
    "API_TESTING_MACHINE_PUBLIC_KEY", '')

API_TESTING_MACHINE_NAME = test_settings.get("API_TESTING_MACHINE_NAME", '')

API_TESTING_CLOUD = test_settings.get('API_TESTING_CLOUD', '')

API_TESTING_CLOUD_PROVIDER = test_settings.get('API_TESTING_CLOUD_PROVIDER', '')

ORG_NAME = test_settings.get('ORG_NAME', '')

SETUP_ENVIRONMENT = test_settings.get("SETUP_ENVIRONMENT", False)

WEBDRIVER_OPTIONS = test_settings.get('WEBDRIVER_OPTIONS',
                                      ['--dns-prefetch-disable'])

REGISTER_USER_BEFORE_FEATURE = test_settings.get('REGISTER_USER_BEFORE_FEATURE',
                                                 False)
