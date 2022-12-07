from behave import step

from misttests.integration.gui.steps.utils import safe_get_element_text
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.common.by import By


@step('key "{key_name}" should be default key')
def check_if_default_key(context, key_name):
    from misttests.integration.gui.steps.list import get_list_item
    item = get_list_item(context, 'key', key_name)
    assert item.get('isDefault')


@step('I add new machine key with name "{key_name}" or I select it')
def add_or_select_key(context, key_name):
    if context.mist_config.get(key_name):
        key_name = context.mist_config.get(key_name)

    keys = context.browser.find_element(By.CSS_SELECTOR, '#key').find_elements(By.CSS_SELECTOR, 'li')
    for key in keys:
        if key_name == safe_get_element_text(key):
            key.click()
            return

    context.execute_steps('''
        When I click the "Add Key" button inside the "Create Machine" panel
        Then I expect for "key-add-popup" popup to appear within max 4 seconds
        When I fill "%s" as key name
        And I click the "Generate" button inside the "Add key" popup
        Then I expect for "key-generate-loader" loader to finish within max 10 seconds
        When I click the "Add" button inside the "Add key" popup
        Then I expect for "key-add-popup" popup to disappear within max 4 seconds
    ''' % key_name)


def find_key(context, key_title):
    context.execute_steps('''
            When I visit the Keys page
    ''')
    key_items = context.browser.find_elements(By.CSS_SELECTOR, 'list-item')
    keys = []
    for key in key_items:
        try:
             if key.is_displayed:
                 keys.append(key)
        except StaleElementReferenceException:
             pass
    for key in keys:
        try:
            title = key.find_element(By.CSS_SELECTOR, '.name')
            if safe_get_element_text(title).lower().strip() == key_title:
                return key
        except (NoSuchElementException, StaleElementReferenceException):
            pass
    return None


@step('"{key}" key has been added')
def given_key(context, key):
    if find_key(context, key.lower()):
        return True

    context.execute_steps('''
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
    ''' % (key))

