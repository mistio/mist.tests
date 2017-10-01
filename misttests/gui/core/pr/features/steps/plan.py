from behave import step

from misttests.gui.steps.utils import safe_get_element_text


@step(u'there should be a message with text "{text}"')
def check_plan_overusage_message(context, text):
    plan_overusage = context.browser.find_element_by_tag_name('plan-overusage')
    assert safe_get_element_text(plan_overusage) == text, "Plan overusage message was not: %s, instead it was: %s" %(text, safe_get_element_text(plan_overusage))
