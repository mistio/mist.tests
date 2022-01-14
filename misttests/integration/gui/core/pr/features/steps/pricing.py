from behave import step
from selenium.webdriver.common.by import By

from misttests.integration.gui.steps.utils import safe_get_element_text
from misttests.integration.gui.steps.buttons import clicketi_click


@step('there should be a message with text "{text}"')
def check_plan_overusage_message(context, text):
    plan_overusage = context.browser.find_element(By.CSS_SELECTOR, 'plan-overusage')
    assert safe_get_element_text(plan_overusage) == text, "Plan overusage message was not: %s, instead it was: %s" %(text, safe_get_element_text(plan_overusage))


@step('the current plan should be "{text}"')
def check_current_plan_message(context, text):
    plans = context.browser.find_elements(By.CSS_SELECTOR, 'plan-item')
    assert text in safe_get_element_text(plans[0]), "Current plan was not: %s, instead it was: %s" %(text, safe_get_element_text(plans[0]))


@step('I click the upgrade button under small plan')
def upgrate_to_small_plan(context):
    plans = context.browser.find_elements(By.CSS_SELECTOR, 'plan-item')
    small_plan = plans[1].find_element(By.CSS_SELECTOR, 'paper-button')
    clicketi_click(context, small_plan)


@step('I set the card details in the purchase plan dialog')
def set_card_details(context):
    purchase_plan = context.browser.find_element(By.CSS_SELECTOR, '#purchasePlan')
    form = purchase_plan.find_element(By.CSS_SELECTOR, '#form')
    dialog = form.find_element(By.CSS_SELECTOR, 'paper-dialog-scrollable')
    inputs = dialog.find_elements(By.CSS_SELECTOR, 'input')
    inputs[0].send_keys('4242424242424242')
    inputs[1].send_keys('10')
    inputs[2].send_keys('22')
    inputs[3].send_keys('007')
    inputs[4].send_keys('17675')


@step('the attention message should be absent')
def check_for_attention_message(context):
    plan_overusage = context.browser.find_element(By.CSS_SELECTOR, 'plan-overusage')
    assert safe_get_element_text(plan_overusage) == '', "Attention message is not absent"
