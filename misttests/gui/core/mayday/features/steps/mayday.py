from misttests.gui.steps.email import *
from misttests.gui.steps.sso import *
from misttests.gui.steps.navigation import *
from misttests.gui.steps.landing import *
from misttests.gui.steps.clouds import *
from misttests.gui.steps.search import *
from misttests.gui.steps.graphs import *
from misttests.gui.steps.machines import *
from misttests.gui.steps.popups import *
from misttests.gui.steps.modals import *
from misttests.gui.steps.ssh import *
from misttests.gui.steps.utils import focus_on_element

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from behave import step
from time import sleep, time


@step(u'I search for the mayday machine')
def search_for_mayday_machine(context):
    search_bar = context.browser.find_element_by_css_selector("input.top-search")
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
    button = context.browser.find_element_by_xpath("//a[contains(text(), '%s')]" % text)
    clicketi_click(context, button)

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

@step(u'I choose the mayday machine')
def choose_mayday_machine(context):
    if context.mist_config.get('MAYDAY_MACHINE'):
        name = context.mist_config.get('MAYDAY_MACHINE')

    end_time = time() + 20
    while time() < end_time:
        machine = get_machine(context, name)
        if machine:
            checkbox = machine.find_element_by_class_name("ui-checkbox")
            checkbox.click()
            return

        sleep(2)
    assert False, u'Could not choose/tick %s machine' % name

@step(u'I fill "{value}" as metric value')
def rule_value(context, value):
    value_input = context.browser.find_element_by_xpath("//paper-input[@id='metricValue']")
    actions = ActionChains(context.browser)
    actions.move_to_element(value_input)
    actions.click()
    actions.send_keys(Keys.BACK_SPACE)
    actions.perform()

    actions.move_to_element(value_input)
    actions.click()
    actions.send_keys("0")
    actions.perform()
#    context.execute_steps(u'When I wait for 2 seconds')
#    value_input.send_keys(u'\ue003')
#    context.execute_steps(u'When I wait for 2 seconds')
#    value_input.send_keys(value)
