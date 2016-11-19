from mist.core.tests.gui.steps.clouds import *
from mist.core.tests.gui.steps.user_actions import *
from mist.core.tests.gui.steps.general import *

from behave import *


@step('I select "{value}" from "{list_id}" drop down')
def accurate_select(context, value, list_id):

    item_list = context.browser.find_element_by_id(list_id)
    button = search_for_button(context, value,
                               button_collection=context.browser.find_element_by_id(list_id).find_elements_by_class_name('ui-btn'))

    list_start_height = item_list.location['y']
    while True:
        height = button.location['y']
        if abs(list_start_height - height) <= 20:
            break
        context.browser.execute_script(u"""
            var selector = document.querySelector("#%s .ui-listview"),
            scroll = %s;
            selector.scrollTop = scroll;
        """ % (list_id, 10))
        new_height = button.location['y']
        if height == new_height:
            break

    clicketi_click(context, button)

