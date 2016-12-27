from misttests.gui.steps.navigation import *
from misttests.gui.steps.machines import *
from misttests.gui.steps.modals import *
from misttests.gui.steps.tags import *
from misttests.gui.steps.popups import *
from misttests.gui.steps.ssh import *
from misttests.gui.steps.list import *


@step(u'I am in the legacy UI')
def am_in_legacy_UI(context):
    """
    Function that waits for the legacy UI to load. The maximum time for the page
    to load is 60 seconds in this case
    """
    try:
        context.browser.find_element_by_id("splash")
        return
    except:
        context.execute_steps(u'''
                When I wait for 15 seconds
                And I wait for the dashboard to load
                When I click the gravatar
                And I wait for 4 seconds
                And I click the button legacy_ui
                Then I wait for the mist.io splash page to load
            ''')


@step(u'I click the mayday machine')
def click_mayday_machine(context):
    """
    This function will try to click a button that says exactly the same thing as
    the text given. If it doesn't find any button like that then it will try
    to find a button that contains the text given. If text is a key inside
    mist_config dict then it's value will be used.
    """
    if context.mist_config.get('MAYDAY_MACHINE'):
        text = context.mist_config['MAYDAY_MACHINE']
    click_button_from_collection(context, 'mistio-mist-core',
                                 error_message='Could not find button that '
                                               'contains %s' % text)



@step(u'I click the button legacy_ui')
def click_legacy_ui(context):
    my_element = context.browser.find_element_by_id('legacy_ui')
    clicketi_click(context, my_element)
    