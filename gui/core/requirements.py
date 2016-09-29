import logging

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

CHROMEDRIVER = "chromedriver"
CHROMEDRIVER_PATH = "parts/chromedriver/"
CHROMEDRIVER_MAIL_PATH = "var/mail/"
CHROMEDRIVER_LOG_PATH = "var/log/"


def setup():
    import os

    log.info("Fetching requirements...")
    os.system("bin/pip install -e tests")

    log.info("Checking for chromedriver")
    # chromedriver = which(CHROMEDRIVER)
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
    os.system("export PATH = " + os.getcwd() + )

    make_dir_if_no_exist(CHROMEDRIVER_MAIL_PATH)
    make_dir_if_no_exist(CHROMEDRIVER_LOG_PATH)


def make_dir_if_no_exist(dir):
    import os
    if not os.path.exists(dir):
        log.info(dir + "does not exist")
        os.makedirs(dir)
    else:
        log.info(dir + " exists")


def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) #and os.access(fpath, os.X_OK)

    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        exe_file = os.path.join(path, program)
        if is_exe(exe_file):
            return exe_file

    return None