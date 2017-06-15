from behave import step
from time import time

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from .utils import safe_get_element_text


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


@step(u'"{element}" in "{section}" section should be "{value}"')
def check_value_in_section(context, element, section, value):
    section_element = context.browser.find_element_by_id(section)
    data_element = section_element.find_element_by_id(section + '-data')
    element_to_check = data_element.find_element_by_id(section + '-' + element)
    assert value in safe_get_element_text(element_to_check), "%s was not %s, but instead it was %s" \
                                                             % (element, value, safe_get_element_text(element_to_check))


@step(u'I refresh the Insights page until data are available')
def refresh_until_data_are_available(context):
    section_element = context.browser.find_element_by_id('quick-overview')
    data_element = section_element.find_element_by_id('quick-overview-data')
    end_time = time() + 250
    while time() < end_time:
        try:
            cost = data_element.find_element_by_id('quick-overview-cost')
            if safe_get_element_text(cost) == 'COST\n$':
                context.execute_steps(u'When I wait for 2 seconds')
                context.execute_steps(u'When I refresh the page')
                context.execute_steps(u'When I wait for 3 seconds')
            else:
                return
        except StaleElementReferenceException:
            pass
    assert False, "No insights data have arrived after 25 seconds"
