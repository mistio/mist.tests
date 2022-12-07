from time import time
from time import sleep

from behave import step, use_step_matcher

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

from misttests.integration.gui.steps.utils import safe_get_element_text, expand_shadow_root

from misttests.integration.gui.steps.buttons import click_button_from_collection, clicketi_click

from misttests.integration.gui.steps.forms import get_input_element_from_form
from misttests.integration.gui.steps.forms import clear_input_and_send_keys, get_button_from_form


def get_dialog(context, title):
    title = title.lower()
    if "rename machine" in title:
        try:
            # Machine rename dialog opens in iron-overlay inside machine-edit element
            # opposed to the rest of the dialogs which open on the vaadin-overlay
            mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
            mist_app_shadow = expand_shadow_root(context, mist_app)
            page_machines = mist_app_shadow.find_element(By.CSS_SELECTOR, 'page-machines')
            page_machines_shadow = expand_shadow_root(context, page_machines)
            machine_page = page_machines_shadow.find_element(By.CSS_SELECTOR, 'machine-page')
            machine_page_shadow = expand_shadow_root(context, machine_page)
            machine_actions = machine_page_shadow.find_element(By.CSS_SELECTOR, 'machine-actions')
            machine_actions_shadow = expand_shadow_root(context, machine_actions)
            machine_edit = machine_actions_shadow.find_element(By.CSS_SELECTOR, 'machine-edit')
            return machine_edit
        except NoSuchElementException:
            pass

    try:
        overlay = context.browser.find_element(By.CSS_SELECTOR, 'vaadin-dialog-overlay')
        overlay_shadow = expand_shadow_root(context, overlay)
        dialog = overlay_shadow.find_element(By.CSS_SELECTOR, 'div#content')
        dialog_shadow = expand_shadow_root(context, dialog)
        if dialog.is_displayed():
            try:
                dialog = dialog_shadow.find_element(By.CSS_SELECTOR, 'team-add-element, custom-graph')
                dialog_shadow = expand_shadow_root(context, dialog)
            except NoSuchElementException:
                pass
            try:
                t = safe_get_element_text(dialog_shadow.find_element(
                    By.CSS_SELECTOR, 'h2')).strip().lower()
            except NoSuchElementException:
                # single cloud page
                t = safe_get_element_text(dialog_shadow.find_element(
                    By.CSS_SELECTOR, 'h3')).strip().lower()
            if title in t:
                return dialog
    except NoSuchElementException:
        pass
    return None


@step('I expect the "{dialog_title}" dialog to be {state} within {seconds}'
      ' seconds')
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


@step('I expect the field "{field_name}" in the dialog with title '
      '"{dialog_title}" to be visible within max {seconds} seconds')
def check_that_field_is_visible(context, field_name, dialog_title, seconds):
    field_name = field_name.lower()
    dialog = get_dialog(context, dialog_title)
    dialog_shadow = expand_shadow_root(context, dialog)
    input_element = None
    timeout = time() + int(seconds)
    while time() < timeout:
        input_element = get_input_element_from_form(context, dialog_shadow, field_name)
        if input_element.is_displayed():
            return True
        sleep(1)
    assert input_element, "Could not find field %s after %s seconds" % field_name
    assert False, "Field %s did not become visible after %s seconds" \
                  % (field_name, seconds)


#@step(u'I click the "{button_name}" button in the "{dialog_title}" dialog')
use_step_matcher("re")
@step('I click the "(?P<button_name>[A-Za-z0-9_\. ]+)" button in the "(?P<dialog_title>[A-Za-z ]+)" dialog')
def click_button_in_dialog(context, button_name, dialog_title):
    dialog = get_dialog(context, dialog_title)
    assert dialog, "Could not find dialog with title %s" % dialog_title
    dialog_shadow = expand_shadow_root(context, dialog)
    button = get_button_from_form(context, dialog_shadow, button_name, tag_name='paper-button:not([hidden]), paper-item:not([hidden])')
    clicketi_click(context, button)


use_step_matcher("parse")
@step('I click the toggle button with id "{btn_id}" in the "{dialog}" dialog')
def click_toggle_button_in_dialog(context, btn_id, dialog):
    open_dialog = get_dialog(context, dialog)
    assert open_dialog, "Could not find dialog with title %s" % dialog
    dialog_shadow = expand_shadow_root(context, open_dialog)
    button_to_click = dialog_shadow.find_element(By.CSS_SELECTOR, '#%s' % btn_id)
    clicketi_click(context, button_to_click)


@step('I set the value "{value}" to field "{name}" in the "{title}" dialog')
def set_value_to_field(context, value, name, title):
    if context.mist_config.get(value):
        value = context.mist_config.get(value)
    dialog = get_dialog(context, title)
    dialog_shadow = expand_shadow_root(context, dialog)
    if "-random" in name:
        name = name.replace('-random', '')
    input_element = get_input_element_from_form(context, dialog_shadow, name.lower())
    assert input_element, "Could not set value to field %s" % name
    clear_input_and_send_keys(input_element, value)


@step('there should be a "{error_msg}" error message'
      ' in the "{dialog_title}" dialog')
def check_errormsg_in_dialog(context, error_msg, dialog_title):
    dialog = get_dialog(context, dialog_title)
    dialog_shadow = expand_shadow_root(context, dialog)
    error_element = dialog_shadow.find_element(By.CSS_SELECTOR, '#errormsg')
    if error_msg in safe_get_element_text(error_element):
        return
    assert False, "%s is not part of the error message" % error_msg
