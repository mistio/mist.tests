from behave import step

from misttests.gui.steps.utils import safe_get_element_text
from misttests.gui.steps.buttons import clicketi_click

@step(u'there should be a message with text "{text}"')
def check_plan_overusage_message(context, text):
    plan_overusage = context.browser.find_element_by_tag_name('plan-overusage')
    assert safe_get_element_text(plan_overusage) == text, "Plan overusage message was not: %s, instead it was: %s" %(text, safe_get_element_text(plan_overusage))


@step(u'the current plan should be "{text}"')
def check_current_plan_message(context, text):
    plans = context.browser.find_elements_by_tag_name('plan-item')
    assert text in safe_get_element_text(plans[0]), "Current plan was not: %s, instead it was: %s" %(text, safe_get_element_text(plans[0]))


@step(u'I click the upgrade button under small plan')
def upgrate_to_small_plan(context):
    plans = context.browser.find_elements_by_tag_name('plan-item')
    small_plan = plans[1].find_element_by_tag_name('paper-button')
    clicketi_click(context, small_plan)


@step(u'I set the card details in the purchase plan dialog')
def set_card_details(context):
    purchase_plan = context.browser.find_element_by_id('purchasePlan')
    form = purchase_plan.find_element_by_id('form')
    dialog = form.find_element_by_tag_name('paper-dialog-scrollable')
    inputs = dialog.find_elements_by_tag_name('input')
    inputs[0].send_keys('4242424242424242')
    inputs[1].send_keys('10')
    inputs[2].send_keys('22')
    inputs[3].send_keys('007')
    inputs[4].send_keys('17675')
