from time import sleep

from misttests.integration.gui.steps.utils import get_page_element, expand_shadow_root
from misttests.integration.gui.steps.forms import get_add_form, get_button_from_form
from misttests.integration.gui.steps.buttons import clicketi_click, safe_get_element_text


@step(u'I select the "{option_to_select}" radio button in the "{resource_type}" add form')
def select_option_from_radiogroup(context, option_to_select, resource_type):
    form = get_add_form(context, 'schedule')
    form_shadow = expand_shadow_root(context, form)
    button = get_button_from_form(context, form_shadow, option_to_select, tag_name='paper-radio-button')
    if button:
        clicketi_click(context, button)
        return
    assert False, 'Could not find "%s" radio button in "%s" add form' % (option_to_select, resource_type)


@step(u'I select the "{option_to_select}" checkbox in the "{resource_type}" add form')
def select_checkbox(context, option_to_select, resource_type):
    if context.mist_config.get(option_to_select):
        option_to_select = context.mist_config.get(option_to_select)
    form = get_add_form(context, 'schedule')
    form_shadow = expand_shadow_root(context, form)
    button = get_button_from_form(context, form_shadow, option_to_select, tag_name='paper-checkbox')
    if button:
        clicketi_click(context, button)
        return
    assert False, 'Could not find "%s" checkbox in "%s" add form' % (option_to_select, resource_type)