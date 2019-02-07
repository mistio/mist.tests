from time import sleep
from behave import step

from .forms import clear_input_and_send_keys
from .buttons import clicketi_click
from .utils import expand_shadow_root


@step(u'I search for "{search_text}"')
def search_for_something(context, search_text):
    sleep(.5)
    mist_app = context.browser.find_element_by_tag_name('mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    mist_header = mist_app_shadow.find_element_by_css_selector('mist-header')
    mist_header_shadow = expand_shadow_root(context, mist_header)
    top_search = mist_header_shadow.find_element_by_css_selector('top-search')
    top_search_shadow = expand_shadow_root(context, top_search)
    mist_filter = top_search_shadow.find_element_by_css_selector('mist-filter')
    mist_filter_shadow = expand_shadow_root(context, mist_filter)
    search_field = mist_filter_shadow.find_element_by_css_selector('paper-input#searchInput')
    if context.mist_config.get(search_text):
        search_text = context.mist_config.get(search_text)
    clicketi_click(context, top_search)
    sleep(.5)
    if not context.browser.execute_script('return arguments[0].focused', search_field):
        top_search.click()
        sleep(.5)
    assert context.browser.execute_script('return arguments[0].focused', search_field), "Search field not focused after 2 clicks"
    search_field.send_keys(search_text)
    sleep(.5)
    if search_text not in search_field.get_attribute('value'):
        top_search.click()
        expand_shadow_root(context, search_field).find_element_by_css_selector('input').send_keys(search_text)
    assert search_text in search_field.get_attribute('value'), "Cannot set search term"


@step(u'I clear the search bar')
def clear_search(context):
    mist_app = context.browser.find_element_by_tag_name('mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    mist_header = mist_app_shadow.find_element_by_css_selector('mist-header')
    mist_header_shadow = expand_shadow_root(context, mist_header)
    top_search = mist_header_shadow.find_element_by_css_selector('top-search')
    top_search_shadow = expand_shadow_root(context, top_search)
    mist_filter = top_search_shadow.find_element_by_css_selector('mist-filter')
    mist_filter_shadow = expand_shadow_root(context, mist_filter)
    clicketi_click(context, top_search)
    clear_icons = mist_filter_shadow.find_elements_by_css_selector(
        'paper-icon-button[icon="close"]')
    clear_icons = filter(lambda el: el.is_displayed(), clear_icons)
    assert len(clear_icons) > 0, "No clear icon found"
    clicketi_click(context, clear_icons[0])
