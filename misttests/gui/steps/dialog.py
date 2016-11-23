from behave import step

from time import time
from time import sleep

from .utils import safe_get_element_text

from .buttons import click_button_from_collection

from .forms import get_input_from_form
from .forms import clear_input_and_send_keys


def get_dialog(context, title):
    title = title.lower()
    dialogs = context.browser.find_elements_by_tag_name('paper-dialog')
    for dialog in dialogs:
        if dialog.is_displayed():
            try:
                t = safe_get_element_text(dialog.find_element_by_tag_name('h2')).strip().lower()
                if title in t:
                    return dialog
            except:
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


@step(u'I click the "{button_name}" button in the dialog "{dialog_title}"')
def click_button_in_dialog(context, button_name, dialog_title):
    dialog = get_dialog(context, dialog_title)
    assert dialog, "Could not find dialog with title %s" % dialog_title
    dialog_buttons = dialog.find_elements_by_tag_name('paper-button')
    click_button_from_collection(context, button_name, dialog_buttons)


@step(u'I set the value "{value}" to field "{name}" in "{title}" dialog')
def set_value_to_field(context, value, name, title):
    if context.mist_config.get(value):
        value = context.mist_config.get(value)
    dialog = get_dialog(context, title)
    input = get_input_from_form(dialog, name.lower())
    assert input, "Could not set value to field %s" % name
    clear_input_and_send_keys(input, value)
