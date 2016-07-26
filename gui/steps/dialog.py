from behave import step

from time import time
from time import sleep

from .utils import safe_get_element_text

from .buttons import click_button_from_collection


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


@step(u'I click the "{button_name}" button in the dialog "{dialog_title}"')
def click_button_in_dialog(context, button_name, dialog_title):
    dialog = get_dialog(context, dialog_title)
    assert dialog, "Could not find dialog with title %s" % dialog_title
    dialog_buttons = dialog.find_elements_by_tag_name('paper-button')
    click_button_from_collection(context, button_name, dialog_buttons)
