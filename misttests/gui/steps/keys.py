from behave import step

from .utils import safe_get_element_text
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException



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


def find_key(context, key_title):
    context.execute_steps(u'''
            When I visit the Keys page
    ''')
    key_items = context.browser.find_elements_by_tag_name('list-item')
    keys = []
    for key in key_items:
        try:
             if key.is_displayed:
                 keys.append(key)
        except StaleElementReferenceException:
             pass
    for key in keys:
        try:
            title = key.find_element_by_class_name('name')
            if safe_get_element_text(title).lower().strip() == key_title:
                return key
        except (NoSuchElementException, StaleElementReferenceException):
            pass
    return None


@step(u'"{key}" key has been added')
def given_key(context, key):
    if find_key(context, key.lower()):
        return True

    context.execute_steps(u'''
            When I visit the keys page
            When I click the button "+"
            Then I expect the "Key" add form to be visible within max 10 seconds
            When I set the value "%s" to field "Name" in "key" add form
            Then I click the button "Generate" in "key" add form
            And I wait for 5 seconds
            And I expect for the button "Add" in "key" add form to be clickable within 9 seconds
            When I focus on the button "Add" in "key" add form
            And I click the button "Add" in "key" add form
            Then I expect the "key" edit form to be visible within max 5 seconds
            When I visit the Home page
            When I wait for the dashboard to load
            When I visit the Keys page
            Then "%s" key should be present within 15 seconds
    ''' % (key, key))

