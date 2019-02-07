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
    mist_filter_shadow.find_element_by_css_selector('iron-icon[icon="search"]').click()
    sleep(.5)
    search_field.send_keys(search_text)
    sleep(.5)


@step(u'I clear the search bar')
def clear_search(context):
    sleep(.5)
    mist_app = context.browser.find_element_by_tag_name('mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    mist_header = mist_app_shadow.find_element_by_css_selector('mist-header')
    mist_header_shadow = expand_shadow_root(context, mist_header)
    top_search = mist_header_shadow.find_element_by_css_selector('top-search')
    top_search_shadow = expand_shadow_root(context, top_search)
    mist_filter = top_search_shadow.find_element_by_css_selector('mist-filter')
    mist_filter_shadow = expand_shadow_root(context, mist_filter)
    mist_filter_shadow.find_element_by_css_selector('iron-icon').click()
    sleep(.5)
    clear_icons = mist_filter_shadow.find_elements_by_css_selector(
        'paper-icon-button[icon="close"]')
    clear_icons = filter(lambda el: el.is_displayed(), clear_icons)
    assert len(clear_icons) > 0, "No clear icon found"
    clicketi_click(context, clear_icons[0])
