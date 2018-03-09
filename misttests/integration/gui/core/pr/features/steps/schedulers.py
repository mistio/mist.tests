from misttests.integration.gui.steps.team import *

from time import sleep


@step(u'I select {action} action in schedules add form')
def select_action_for_schedule(context, action):
    actions = context.browser.find_elements_by_tag_name('paper-radio-group')
    buttons = []
    for action in actions:
        buttons.append(action.find_elements_by_tag_name('paper-radio-button'))
    clicketi_click(context, buttons[0])


@step(u'I select "{option_to_select}" from "{radio_group}" radio-group')
def select_option_from_radiogroup(context, option_to_select, radio_group):
    base_btn = 'app-form-scheduleAddForm-'
    radio_group = base_btn + radio_group
    paper_radio_group = context.browser.find_element_by_id(radio_group)
    paper_radio_buttons = paper_radio_group.find_elements_by_tag_name('paper-radio-button')
    for button in paper_radio_buttons:
        if safe_get_element_text(button) == option_to_select:
            clicketi_click(context, button)
            return


@step(u'I select the "{option_to_select}" checkbox')
def select_checkbox(context, option_to_select):
    if context.mist_config.get(option_to_select):
        option_to_select = context.mist_config.get(option_to_select)
    sleep(1)
    paper_check_boxes = context.browser.find_elements_by_tag_name('paper-checkbox')
    for checkbox in paper_check_boxes:
        if safe_get_element_text(checkbox) == option_to_select:
            clicketi_click(context, checkbox)
            return
