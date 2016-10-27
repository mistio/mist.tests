from tests.legacy_gui.steps.email import *
from tests.legacy_gui.steps.sso import *
from tests.legacy_gui.steps.navigation import *
from tests.legacy_gui.steps.landing import *
from tests.legacy_gui.steps.clouds import *
from tests.legacy_gui.steps.search import *
from tests.legacy_gui.steps.graphs import *
from tests.legacy_gui.steps.machines import *
from tests.legacy_gui.steps.popups import *
from tests.legacy_gui.steps.modals import *
from tests.legacy_gui.steps.ssh import *
from tests.legacy_gui.steps.buttons import *

from behave import step
from time import sleep, time


@step(u'I search for the mayday machine')
def search_for_mayday_machine(context):
    search_bar = context.browser.find_elements_by_class_name("machine-search")
    assert len(search_bar) > 0, "Could not find the machine-search search input"
    assert len(search_bar) == 1, "Found more than one machine-search search input elements"
    search_bar = search_bar[0]
    if context.mist_config.get('MAYDAY_MACHINE'):
        text = context.mist_config['MAYDAY_MACHINE']
    for letter in text:
        search_bar.send_keys(letter)
    sleep(2)

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
    click_button_from_collection(context, text,
                                 error_message='Could not find button that '
                                               'contains %s' % text)

@step(u'Mayday machine state should be "{state}" within {seconds} seconds')
def assert_mayday_machine_state(context, state, seconds):
    if context.mist_config.get('MAYDAY_MACHINE'):
        name = context.mist_config.get('MAYDAY_MACHINE')

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
