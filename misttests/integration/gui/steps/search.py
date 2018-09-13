from time import sleep
from behave import step

from .forms import clear_input_and_send_keys
from .buttons import clicketi_click


@step(u'I search for "{search_text}"')
def search_for_something(context, search_text):
    search_field = context.browser.find_element_by_id('query')
    if context.mist_config.get(search_text):
        search_text = context.mist_config.get(search_text)
    clear_input_and_send_keys(search_field, search_text)
    sleep(1)


@step(u'I clear the search bar')
def clear_search(context):
    clear_icons = context.browser.find_elements_by_css_selector(
        'top-search iron-icon[icon="close"]')
    clear_icons = filter(lambda el: el.is_displayed(), clear_icons)
    assert len(clear_icons) > 0, "No clear icon found"
    clicketi_click(context, clear_icons[0])
