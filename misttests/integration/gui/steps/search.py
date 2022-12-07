import logging

from time import sleep
from behave import step

from selenium.webdriver.common.by import By

from misttests.integration.gui.steps.forms import clear_input_and_send_keys
from misttests.integration.gui.steps.buttons import clicketi_click
from misttests.integration.gui.steps.utils import expand_shadow_root

log = logging.getLogger(__name__)


@step('I search for "{search_text}"')
def search_for_something(context, search_text):
    sleep(.5)
    mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    mist_header = mist_app_shadow.find_element(By.CSS_SELECTOR, 'mist-header')
    mist_header_shadow = expand_shadow_root(context, mist_header)
    top_search = mist_header_shadow.find_element(By.CSS_SELECTOR, 'top-search')
    top_search_shadow = expand_shadow_root(context, top_search)
    mist_filter = top_search_shadow.find_element(By.CSS_SELECTOR, 'mist-filter')
    mist_filter_shadow = expand_shadow_root(context, mist_filter)
    search_field = mist_filter_shadow.find_element(By.CSS_SELECTOR, 'paper-input#searchInput')
    if context.mist_config.get(search_text):
        search_text = context.mist_config.get(search_text)
    # focused = context.browser.execute_script('return arguments[0].focused', search_field)
    # log.info('Search field focused before: %s' % focused)
    top_search.click()
    sleep(.5)
    focused = context.browser.execute_script('return arguments[0].focused', search_field)
    # log.info('Search field focused after: %s' % focused)
    if not focused:
        search_field.click()
        sleep(.5)
        expand_shadow_root(context, search_field).find_element(By.CSS_SELECTOR, 'input').send_keys('')
        focused = context.browser.execute_script('return arguments[0].focused', search_field)
        log.info('Search field focused after2: %s' % focused)
        if not focused:
            expand_shadow_root(context, search_field).find_element(By.CSS_SELECTOR, 'input').send_keys('')
    search_value = search_field.get_attribute('value')
    search_field.send_keys(search_text)
    sleep(.5)
    search_value = search_field.get_attribute('value')
    if search_text not in search_value:  # This shouldn't happen but sometimes it does
        top_search.click()  # Refocus
        # If search_field.send_keys() does not update the filter, try doing it with JS code instead
        context.browser.execute_script('arguments[0].set("value", "%s")' % search_text, search_field)
        sleep(.5)
        search_value = search_field.get_attribute('value')
    assert search_text in search_field.get_attribute('value'), "Cannot set search term"


@step('I clear the search bar')
def clear_search(context):
    mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    mist_header = mist_app_shadow.find_element(By.CSS_SELECTOR, 'mist-header')
    mist_header_shadow = expand_shadow_root(context, mist_header)
    top_search = mist_header_shadow.find_element(By.CSS_SELECTOR, 'top-search')
    top_search_shadow = expand_shadow_root(context, top_search)
    mist_filter = top_search_shadow.find_element(By.CSS_SELECTOR, 'mist-filter')
    mist_filter_shadow = expand_shadow_root(context, mist_filter)
    search_field = mist_filter_shadow.find_element(By.CSS_SELECTOR, 'paper-input#searchInput')
    clicketi_click(context, top_search)
    clear_icons = mist_filter_shadow.find_elements(By.CSS_SELECTOR, 
        'paper-icon-button[icon="close"]')
    clear_icons = [el for el in clear_icons if el.is_displayed()]
    if clear_icons:
        clicketi_click(context, clear_icons[0])
    search_value = search_field.get_attribute('value')
    assert not search_value, "Cannot clear search: %s" % search_value
