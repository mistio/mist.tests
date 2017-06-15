from behave import step
from time import time

from selenium.common.exceptions import NoSuchElementException


@step(u'the "{section}" section should be visible within {seconds} seconds')
def check_insights_element_visibility(context, section, seconds):
    end_time = time() + int(seconds)
    while time() < end_time:
        try:
            context.browser.find_element_by_id(section)
            return
        except NoSuchElementException:
            pass
    assert False, "Section %s is not visible after %s seconds" % (section,seconds)
