from behave import step

from .utils import safe_get_element_text


@step(u'key "{key_name}" should be default key')
def check_if_default_key(context, key_name):
    from .list import get_list_item
    item = get_list_item(context, 'key', key_name)
    assert safe_get_element_text(item.find_element_by_css_selector('div.default')).strip().lower() == 'default', \
        "Key %s is not default key" % key_name


@step(u'I add new machine key with name "{key_name}" or I select it')
def add_or_select_key(context, key_name):
    if context.mist_config.get(key_name):
        key_name = context.mist_config.get(key_name)

    keys = context.browser.find_element_by_id('key').find_elements_by_tag_name('li')
    for key in keys:
        if key_name == safe_get_element_text(key):
            key.click()
            return

    context.execute_steps(u'''
        When I click the "Add Key" button inside the "Create Machine" panel
        Then I expect for "key-add-popup" popup to appear within max 4 seconds
        When I fill "%s" as key name
        And I click the "Generate" button inside the "Add key" popup
        Then I expect for "key-generate-loader" loader to finish within max 10 seconds
        When I click the "Add" button inside the "Add key" popup
        Then I expect for "key-add-popup" popup to disappear within max 4 seconds
    ''' % key_name)
