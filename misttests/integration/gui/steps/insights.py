from behave import step
from time import time

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from .utils import safe_get_element_text, get_page_element, expand_shadow_root

def get_insights_element(context, shadow=False):
    insights_page = get_page_element(context, 'insights')
    insights_page_shadow = expand_shadow_root(context, insights_page)
    insights_element = insights_page_shadow.find_element_by_css_selector('mist-insights')
    if shadow:
        return expand_shadow_root(context, insights_element)
    return insights_element


@step(u'the "{section}" section should be visible within {seconds} seconds')
def check_insights_element_visibility(context, section, seconds):
    insights_element_shadow = get_insights_element(context, shadow=True)
    end_time = time() + int(seconds)
    while time() < end_time:
        try:
            target = insights_element_shadow.find_element_by_css_selector('#' + section )
            if target.is_displayed():
                return
        except NoSuchElementException:
            pass
    assert False, "Section %s is not visible after %s seconds" \
                  % (section, seconds)


@step(u'"{element}" in "{section}" section should be "{value}"')
def check_value_in_section(context, element, section, value):
    insights_element_shadow = get_insights_element(context, shadow=True)
    section_element = insights_element_shadow.find_element_by_css_selector('#%s' % section )
    data_element = section_element.find_element_by_css_selector('#%s-data' % section)
    element_to_check = data_element.find_element_by_css_selector('#%s-%s' % (section, element))
    if element == "machine_count" and value == "greater than 0":
        assert int(safe_get_element_text(element_to_check).
                   strip('MACHINE COUNT\n')) > 0,\
            "No machines are shown in machine count element"
    elif element == "cost" and value == "greater than $0.00":
        assert float(safe_get_element_text(element_to_check).
                     strip('COST\n').strip('$')) > 0.0,\
            "Cost is still 0.0 even though cost_per_month tag was added!"
    else:
        assert value in safe_get_element_text(element_to_check),\
            "%s was not %s, but instead it was %s" %\
            (element, value, safe_get_element_text(element_to_check))


@step(u'I refresh the Insights page until data are available')
def refresh_until_data_are_available(context):
    end_time = time() + 120
    while time() < end_time:
        context.execute_steps(u'When I refresh the page')
        context.execute_steps(u'When I wait for 3 seconds')
        try:
            insights_element_shadow = get_insights_element(context, shadow=True)
            section_element = insights_element_shadow.\
                find_element_by_css_selector('#quick-overview')
            data_element = section_element.\
                find_element_by_css_selector('#quick-overview-data')
            cost = data_element.find_element_by_css_selector('#quick-overview-cost')
            if 'COST\nNo data' not in safe_get_element_text(cost):
                return
        except StaleElementReferenceException:
            pass
    assert False, "No insights data have arrived after 120 seconds"
