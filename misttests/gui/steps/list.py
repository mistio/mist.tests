from behave import step

from time import time
from time import sleep

from .utils import safe_get_element_text

from .buttons import click_button_from_collection

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


# TODO: below method doesn't bring all the items, as you scroll more items become visible
def get_list(context, resource_type):
    if resource_type in ['machine', 'team', 'key', 'network', 'script', 'schedule', 'template', 'stack', 'zone']:
        return context.browser.find_elements_by_css_selector('page-%ss mist-list vaadin-grid-table-body#items > vaadin-grid-table-row' % resource_type)
    elif resource_type == 'record':
        return context.browser.find_elements_by_css_selector('page-zones iron-list div.row')
    else:
        return context.browser.find_elements_by_css_selector('page-%ss iron-list div.row' % resource_type)


def get_list_item(context, resource_type, name):
    resource_type = resource_type.lower()
    item_name = name.lower()
    if resource_type not in ['machine', 'image', 'key', 'network',
                             'tunnel', 'script', 'template', 'stack',
                             'team', 'schedule', 'zone', 'record']:
        raise ValueError('The resource type given is unknown')
    try:
        items = get_list(context, resource_type)
        for item in items:
            if resource_type in ['machine', 'team', 'key', 'network', 'script', 'schedule', 'template', 'stack', 'zone']:
                name = safe_get_element_text(item.find_element_by_css_selector('strong.name')).strip().lower()
            else:
                name = safe_get_element_text(item.find_element_by_css_selector('div.name')).strip().lower()
            if item_name == name:
                    return item
    except (NoSuchElementException, StaleElementReferenceException):
        pass
    return None


def get_machine(context, name):
    try:
        placeholder = context.browser.find_element_by_tag_name("page-machines")
        machines = placeholder.find_elements_by_tag_name("vaadin-grid-table-row")

        for machine in machines:
            machine_text = safe_get_element_text(machine.find_element_by_css_selector('.name')).strip().lower()
            if name in machine_text:
                return machine

        return None
    except NoSuchElementException:
        return None
    except StaleElementReferenceException:
        return None


@step(u'"{name}" machine state has to be "{state}" within {seconds} seconds')
def assert_machine_state(context, name, state, seconds):
    if context.mist_config.get(name):
        name = context.mist_config.get(name)
    end_time = time() + int(seconds)
    while time() < end_time:
        machine = get_machine(context, name)
        if machine:
            try:
                if state in safe_get_element_text(machine.find_element_by_css_selector('.state span')).strip().lower():
                    return
            except NoSuchElementException:
                pass
            except StaleElementReferenceException:
                pass
        sleep(2)
    assert False, u'%s state is not "%s"' % (name, state)


@step(u'I select list item "{item_name}" {resource_type}')
def select_item_from_list(context, item_name, resource_type):
    if context.mist_config.get(item_name):
        item_name = context.mist_config.get(item_name)
    if resource_type in ['record']:
        item_name = item_name + '.' + context.mist_config.get('test-zone-random.com.')
    item = get_list_item(context, resource_type, item_name)
    if item:
        from .buttons import clicketi_click
        if resource_type == 'record':
            select_button = item.find_element_by_id('check')
        else:
            select_button = item.find_element_by_css_selector('mist-check')
        clicketi_click(context, select_button)
        sleep(1)
        return True
    assert False, "Could not select from list item %s" % item_name


@step(u'I click the button "{button_name}" from the menu of the "{item_name}"'
      u' {resource_type}')
def click_menu_button_of_list_item(context, button_name, item_name,
                                   resource_type):

    item = get_list_item(context, resource_type, item_name)
    if item:
        more_dialog = context.browser.find_element_by_css_selector('page-%ss item-list paper-dialog#select-action' % resource_type)
        more_button = item.find_element_by_css_selector('paper-button.more')
        from .buttons import clicketi_click
        clicketi_click(context, more_button)
        sleep(1)
        more_buttons = more_dialog.find_elements_by_tag_name('paper-button')
        click_button_from_collection(context, button_name, more_buttons)
        return True
    assert False, "Could not click button %s" % button_name


@step(u'"{name}" {resource_type} should be {state} within {seconds}'
      u' seconds')
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
