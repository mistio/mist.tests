import logging

from config import LOG_DIR, MAIL_DIR

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

CHROMEDRIVER = "chromedriver"
CHROMEDRIVER_PATH = "parts/chromedriver/"


def chrome_driver_setup():
    import os

    log.info("Checking for chromedriver")
    make_dir_if_no_exist(CHROMEDRIVER_PATH)

    if (os.path.isfile(CHROMEDRIVER_PATH + CHROMEDRIVER)):
        log.info("Chromedriver exists in " + CHROMEDRIVER_PATH)
    else:
        log.info("Chromedriver does not exist in" + CHROMEDRIVER_PATH + ". Fetching it...")
        import urllib
        urllib.urlretrieve("http://chromedriver.storage.googleapis.com/2.24/chromedriver_linux64.zip","parts/chromedriver/chrome_driver")

        import zipfile
        with zipfile.ZipFile('parts/chromedriver/chrome_driver', "r") as z:
            z.extractall(CHROMEDRIVER_PATH)

    # fix_permissions(CHROMEDRIVER)
    os.chmod("parts/chromedriver/chromedriver", 0744)

    # export path
    os.system("export PATH=" + os.path.join(os.getcwd(), CHROMEDRIVER_PATH) + ":$PATH")

    make_dir_if_no_exist(MAIL_DIR)
    make_dir_if_no_exist(LOG_DIR)


def make_dir_if_no_exist(dir):
    import os
    if not os.path.exists(dir):
        log.info(dir + "does not exist")
        os.makedirs(dir)
    else:
        log.info(dir + " exists")