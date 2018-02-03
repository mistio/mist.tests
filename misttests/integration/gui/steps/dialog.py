from behave import step

from time import time
from time import sleep

from .utils import safe_get_element_text

from .buttons import click_button_from_collection, clicketi_click

from .forms import get_input_from_form
from .forms import clear_input_and_send_keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException


def get_dialog(context, title):
    title = title.lower()
    dialogs = context.browser.find_elements_by_tag_name('paper-dialog')
    for dialog in dialogs:
        try:
            if dialog.is_displayed():
                try:
                    t = safe_get_element_text(dialog.find_element_by_tag_name(
                        'h2')).strip().lower()
                except NoSuchElementException:
                    # single cloud page
                    t = safe_get_element_text(dialog.find_element_by_tag_name(
                        'h3')).strip().lower()
                if title in t:
                    return dialog
        except StaleElementReferenceException:
            pass
    return None


@step(u'I expect the dialog "{dialog_title}" is {state} within {seconds}'
      u' seconds')
def wait_for_dialog(context, dialog_title, state, seconds):
    state = state.lower()
    if state not in ['open', 'closed']:
        raise Exception('Unknown state %s' % state)
    timeout = time() + int(seconds)
    while time() < timeout:
        dialog = get_dialog(context, dialog_title)
        if state == 'open' and dialog:
            return True
        if state == 'closed' and not dialog:
            return True
        sleep(1)
    assert False, "Dialog with title %s has not %s after %s seconds" \
                  % (dialog_title, state, seconds)


@step(u'I expect the field "{field_name}" in the dialog with title '
      u'"{dialog_title}" to be visible within max {seconds} seconds')
def check_that_field_is_visible(context, field_name, dialog_title, seconds):
    field_name = field_name.lower()
    dialog = get_dialog(context, dialog_title)
    input = None
    timeout = time() + int(seconds)
    while time() < timeout:
        input = get_input_from_form(dialog, field_name)
        if input.is_displayed():
            return True
        sleep(1)
    assert input, "Could not find field %s after %s seconds" % field_name
    assert False, "Field %s did not become visible after %s seconds" \
                  % (field_name, seconds)


@step(u'I set the value "{value}" to field "{name}" in "{title}" app-form dialog')
def set_value_to_app_form_dialog(context, value, name, title):
    dialog = get_dialog(context, title)
    inputs = dialog.find_elements_by_class_name('input-content')
    for element in inputs:
        if name in element.text:
            input = element.find_element_by_tag_name('input')
            clear_input_and_send_keys(input, value)
            return

    assert False, "Could not set value to field %s" % name


@step(u'I click the "{button_name}" button in the dialog "{dialog_title}"')
def click_button_in_dialog(context, button_name, dialog_title):
    dialog = get_dialog(context, dialog_title)
    assert dialog, "Could not find dialog with title %s" % dialog_title
    dialog_buttons = dialog.find_elements_by_tag_name('paper-button')
    click_button_from_collection(context, button_name, dialog_buttons)


@step(u'I click the toggle button with id "{btn_id}" in the dialog "{dialog}"')
def click_toggle_button_in_dialog(context, btn_id, dialog):
    open_dialog = get_dialog(context, dialog)
    assert open_dialog, "Could not find dialog with title %s" % dialog
    button_to_click = open_dialog.find_element_by_id(btn_id)
    clicketi_click(context, button_to_click)


@step(u'I set the value "{value}" to field "{name}" in "{title}" dialog')
def set_value_to_field(context, value, name, title):
    if context.mist_config.get(value):
        value = context.mist_config.get(value)
    dialog = get_dialog(context, title)
    input = get_input_from_form(dialog, name.lower())
    assert input, "Could not set value to field %s" % name
    clear_input_and_send_keys(input, value)


@step(u'there should be a "{error_code}" error message'
      u' in "{dialog_title}" dialog')
def check_errormsg_in_dialog(context, error_code, dialog_title):
    dialog = get_dialog(context, dialog_title)
    error_msg = dialog.find_element_by_id('errormsg')
    if error_code in safe_get_element_text(error_msg):
        return
    assert False, "%s is not part of the error message" % error_code
