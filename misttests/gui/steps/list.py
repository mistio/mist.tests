from behave import step

from time import time
from time import sleep

from .utils import safe_get_element_text

from .buttons import click_button_from_collection

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


def get_list(context, resource_type):
    return context.browser.find_elements_by_css_selector('page-%ss iron-list div.row' % resource_type)


def get_list_item(context, resource_type, name):
    resource_type = resource_type.lower()
    item_name = name.lower()
    if resource_type not in ['machine', 'image', 'key', 'network',
                             'tunnel', 'script', 'template', 'stack',
                             'team']:
        raise ValueError('The resource type given is unknown')
    try:
        items = get_list(context, resource_type)
        for item in items:
            name = safe_get_element_text(item.find_element_by_css_selector('div.name')).strip().lower()
            if item_name == name:
                return item
    except (NoSuchElementException, StaleElementReferenceException):
        pass
    return None


# @step(u'"{expected_name}" {resource_type} should be {state} within {seconds}'
#       u' seconds')
# def wait_for_item_show(context, expected_name, resource_type, state, seconds):
#     expected_name = expected_name.strip().lower()
#     expected_name = context.mist_config.get(expected_name, expected_name)
#     state = state.lower()
#     if state not in ['present', 'absent']:
#         raise Exception('Unknown state %s' % state)
#     timeout = time() + int(seconds)
#     while time() < timeout:
#         item = get_list_item(context, resource_type, expected_name)
#         if state == 'present' and item:
#             return True
#         if state == 'absent' and not item:
#             return True
#         sleep(1)
#     assert False, 'Item %s is not %s in the list after %s seconds' \
#                   % (expected_name, state, seconds)


def get_machine(context, name):
    try:
        placeholder = context.browser.find_element_by_tag_name("page-machines")
        machines = placeholder.find_elements_by_tag_name("list-item")

        for machine in machines:
            machine_text = safe_get_element_text(machine)
            if name in machine_text:
                return machine

        return None
    except NoSuchElementException:
        return None
    except StaleElementReferenceException:
        return None


@step(u'"{name}" machine state should be "{state}" within {seconds} seconds')
def assert_machine_state(context, name, state, seconds):
    if context.mist_config.get(name):
        name = context.mist_config.get(name)

    end_time = time() + int(seconds)
    while time() < end_time:
        machine = get_machine(context, name)
        if machine:
            try:
                if state in safe_get_element_text(machine):
                    return
            except NoSuchElementException:
                pass
            except StaleElementReferenceException:
                pass
        sleep(2)

    assert False, u'%s state is not "%s"' % (name, state)


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
