from behave import step

from misttests.gui.steps.buttons import clicketi_click
from misttests.gui.steps.forms import clear_input_and_send_keys
from misttests.gui.steps.landing import get_shadow_root
from misttests.gui.steps.utils import safe_get_element_text

@step(u'I remove all whitelisted ips')
def remove_whitelisted_ips(context):
    whitelisted_ips_tag = context.browser.find_element_by_tag_name('multi-inputs')
    whitelisted_ips = whitelisted_ips_tag.find_elements_by_class_name('input')
    for whitelisted_ip in whitelisted_ips:
        remove_btn = whitelisted_ip.find_element_by_class_name('remove')
        clicketi_click(context, remove_btn)
        context.execute_steps(u'''
                    Then I expect the dialog "Remove Cidr" is open within 4 seconds
                    And I click the "Remove Cidr" button in the dialog "Remove Cidr"
                    And I expect the dialog "Remove Cidr" is closed within 4 seconds
                ''')

@step(u'I add the IP "{ip}" as whitelisted')
def add_whitelisted_ip(context,ip):
    whitelisted_ips_tag = context.browser.find_element_by_tag_name('multi-inputs')
    new_whitelisted_ip_field = whitelisted_ips_tag.find_element_by_tag_name('div')
    whitelisted_ip = new_whitelisted_ip_field.find_element_by_tag_name('paper-input')
    input = whitelisted_ip.find_element_by_id('input')
    clear_input_and_send_keys(input, ip)

def get_forbidden_error_element(context):
    landing_app = context.browser.find_element_by_tag_name("landing-app")
    shadow_root = get_shadow_root(context, landing_app)
    landing_pages = shadow_root.find_element_by_css_selector("landing-pages")
    page = landing_pages.find_element_by_tag_name('landing-sign-in')
    shadow_root = get_shadow_root(context, page)
    sign_in_form = shadow_root.find_element_by_id('signInForm')
    form = sign_in_form.find_element_by_tag_name('form')
    return form.find_element_by_class_name('forbidden-error')


@step(u'I should see the error message "{error_msg}"')
def see_error_msg(context, error_msg):
    forbidden_error = get_forbidden_error_element(context)
    assert error_msg in safe_get_element_text(forbidden_error), "%s error message is not visible" %error_msg


@step(u'I click the forbidden link in the sign-in page')
def click_forbidden_link(context):
    forbidden_error = get_forbidden_error_element(context)
    forbidden_link = forbidden_error.find_element_by_id('forbiddenlink')
    clicketi_click(context,forbidden_link)
