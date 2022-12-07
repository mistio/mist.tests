from behave import step, use_step_matcher

from selenium.webdriver.common.by import By

from time import time
from time import sleep

from misttests.integration.gui.steps.utils import safe_get_element_text, get_page_element, expand_shadow_root
from misttests.integration.gui.steps.utils import get_list_item_from_checkbox
from misttests.integration.gui.steps.utils import get_list_filtered_items

from misttests.integration.gui.steps.buttons import clicketi_click

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


def get_list_items(context, resource_type):
    if resource_type in ['machine', 'image', 'team', 'key', 'network',
                         'script', 'schedule', 'template', 'stack',
                         'zone', 'volume']:
        container = get_page_element(context, resource_type + 's')
    elif resource_type in ['record']:
        _, container = get_page_element(context, 'zones', 'zone')
    container_shadow = expand_shadow_root(context, container)
    mist_list = container_shadow.find_element(By.CSS_SELECTOR, 'mist-list')
    return get_list_filtered_items(context, mist_list)


def get_list_item(context, resource_type, name):
    resource_type = resource_type.strip().lower()
    item_name = name.strip().lower()
    if resource_type not in ['machine', 'image', 'key', 'network',
                             'tunnel', 'script', 'template', 'stack',
                             'team', 'schedule', 'zone', 'record',
                             'volume']:
        raise ValueError('The resource type given is unknown')
    if resource_type == 'zone':
        primary_field = 'domain'
    else:
        primary_field = 'name'
    try:
        items = get_list_items(context, resource_type)
        for item in items:
            if item and isinstance(item, dict) and \
                    item.get(primary_field).strip().lower() == item_name:
                return item
    except (NoSuchElementException, StaleElementReferenceException):
        pass
    return None


@step('"{name}" machine state has to be "{state}" within {seconds} seconds')
def assert_machine_state(context, name, state, seconds):
    if context.mist_config.get(name):
        name = context.mist_config.get(name)
    end_time = time() + int(seconds)
    while time() < end_time:
        machine = get_list_item(context, 'machine', name)
        if machine:
            if state in machine.get('state').strip().lower():
                return
        sleep(2)
    assert False, '%s state is not "%s"' % (name, state)


@step('I select list item "{item_name}" {resource_type}')
def select_item_from_list(context, item_name, resource_type):
    if context.mist_config.get(item_name):
        item_name = context.mist_config.get(item_name)
    if resource_type in ['record']:
        _, container = get_page_element(context, 'zones', 'zone')
        item_name = item_name + '.' + \
            context.mist_config.get('test-zone-random.com.')
    else:
        container = get_page_element(context, resource_type + 's')
    container_shadow = expand_shadow_root(context, container)
    mist_list = container_shadow.find_element(By.CSS_SELECTOR, 'mist-list')
    list_shadow = expand_shadow_root(context, mist_list)
    grid = list_shadow.find_element(By.CSS_SELECTOR, 'vaadin-grid')
    checkboxes = grid.find_elements(By.CSS_SELECTOR, 'mist-check.item-check')
    for checkbox in checkboxes:
        item = get_list_item_from_checkbox(context, checkbox)
        if item and item.get('name') == item_name:
            clicketi_click(context, checkbox)
            sleep(.1)
            return True
    assert False, "Could not select from list item %s" % item_name


@step('I click on list item "{item_name}" {resource_type}')
def click_list_item(context, item_name, resource_type):
    if context.mist_config.get(item_name):
        item_name = context.mist_config.get(item_name)
    if resource_type in ['record']:
        _, container = get_page_element(context, 'zones', 'zone')
        item_name = item_name + '.' + \
            context.mist_config.get('test-zone-random.com.')
    else:
        container = get_page_element(context, resource_type + 's')
    container_shadow = expand_shadow_root(context, container)
    mist_list = container_shadow.find_element(By.CSS_SELECTOR, 'mist-list')
    list_shadow = expand_shadow_root(context, mist_list)
    list_item_names = list_shadow.find_elements(By.CSS_SELECTOR, 'strong.name')
    for item in list_item_names:
        item_text = safe_get_element_text(item)
        if item_text.strip().lower() == item_name.strip().lower():
            clicketi_click(context, item)
            return True
    assert False, "Could not click item %s" % item_name


use_step_matcher("re")
@step('"(?P<name>[A-Za-z0-9()-_. ]+)" (?P<resource_type>[A-Za-z]+) should be '
      '(?P<state>[A-Za-z]+) within (?P<seconds>[0-9]+) seconds')
def wait_for_item_show(context, name, resource_type, state, seconds):
    if context.mist_config.get(name):
        name = context.mist_config.get(name)
    else:
        name = name.lower()
    if resource_type in ['record']:
        name = name + '.' + context.mist_config.get('test-zone-random.com.')
    state = state.lower()
    if state not in ['present', 'absent']:
        raise Exception('Unknown state %s' % state)
    timeout = time() + int(seconds)
    while time() < timeout:
        item = get_list_item(context, resource_type, name)
        if state == 'present' and item:
            return True
        if state == 'absent' and not item:
            return True
        sleep(1)
    assert False, 'Item %s is not %s in the list after %s seconds' \
                  % (name, state, seconds)


use_step_matcher("parse")
