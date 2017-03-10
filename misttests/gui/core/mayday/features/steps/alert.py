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
