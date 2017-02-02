from misttests.gui.steps.modals import *
from misttests.gui.steps.navigation import *
from misttests.gui.steps.setup import *
from misttests.gui.steps.buttons import *


@step(u'I select {action} action in schedules add form')
def select_action_for_schedule(context, action):
    actions = context.browser.find_elements_by_tag_name('paper-radio-group')
    buttons = []
    for action in actions:
        buttons.append(action.find_elements_by_tag_name('paper-radio-button'))
    import pdb
    pdb.set_trace()
    clicketi_click(context, buttons[0])

