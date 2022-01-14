from behave import step
from selenium.webdriver.common.by import By

from misttests.integration.gui.steps.buttons import clicketi_click
from misttests.integration.gui.steps.forms import clear_input_and_send_keys
from misttests.integration.gui.steps.utils import safe_get_element_text, expand_shadow_root

@step('I remove all whitelisted ips')
def remove_whitelisted_ips(context):
    whitelisted_ips_tag = context.browser.find_element(By.CSS_SELECTOR, 'multi-inputs')
    whitelisted_ips = whitelisted_ips_tag.find_elements(By.CSS_SELECTOR, '.input')
    for whitelisted_ip in whitelisted_ips:
        remove_btn = whitelisted_ip.find_element(By.CSS_SELECTOR, '.remove')
        clicketi_click(context, remove_btn)

@step('I add the IP "{ip}" as whitelisted')
def add_whitelisted_ip(context,ip):
    whitelisted_ips_tag = context.browser.find_element(By.CSS_SELECTOR, 'multi-inputs')
    new_whitelisted_ip_div = whitelisted_ips_tag.find_element(By.CSS_SELECTOR, 'div')
    whitelisted_ip_paper_input = new_whitelisted_ip_div.find_element(By.CSS_SELECTOR, 'paper-input')
    clear_input_and_send_keys(whitelisted_ip_paper_input, ip)

def get_forbidden_error_element(context):
    landing_app = context.browser.find_element(By.CSS_SELECTOR, "landing-app")
    shadow_root = expand_shadow_root(context, landing_app)
    landing_pages = shadow_root.find_element(By.CSS_SELECTOR, "landing-pages")
    page = landing_pages.find_element(By.CSS_SELECTOR, 'landing-sign-in')
    shadow_root = expand_shadow_root(context, page)
    sign_in_form = shadow_root.find_element(By.CSS_SELECTOR, '#signInForm')
    form = sign_in_form.find_element(By.CSS_SELECTOR, 'form')
    return form.find_element(By.CSS_SELECTOR, '.forbidden-error')


@step('I should see the error message "{error_msg}"')
def see_error_msg(context, error_msg):
    forbidden_error = get_forbidden_error_element(context)
    assert error_msg in safe_get_element_text(forbidden_error), "%s error message is not visible" %error_msg


@step('I click the forbidden link in the sign-in page')
def click_forbidden_link(context):
    forbidden_error = get_forbidden_error_element(context)
    forbidden_link = forbidden_error.find_element(By.CSS_SELECTOR, '#forbiddenlink')
    clicketi_click(context,forbidden_link)
