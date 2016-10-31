from behave import step

from selenium.common.exceptions import NoSuchElementException

import logging

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

@step(u'I ensure that there is at least one machine in the resources list')
def check_resources_list(context):
    try:
        context.browser.find_element_by_tag_name('stack-machine-item')
    except NoSuchElementException:
        raise NoSuchElementException("Unable to find machines in the resources list")
    