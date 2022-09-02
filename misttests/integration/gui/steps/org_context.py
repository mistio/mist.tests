from behave import step

from selenium.webdriver.common.by import By

from misttests.integration.gui.steps.utils import safe_get_element_text
from misttests.integration.gui.steps.utils import get_page_element
from misttests.integration.gui.steps.utils import expand_shadow_root
from misttests.integration.gui.steps.buttons import \
    click_button_from_collection


def get_current_org(user_menu):
    return safe_get_element_text(
        user_menu.find_element(
            By.CSS_SELECTOR, 'div.current.context').find_element(
                By.CSS_SELECTOR, 'h4')).\
        strip().lower()


@step('I ensure that I am in the "{organization}" organization context')
def ensure_organizational_context(context, organization):
    from misttests.integration.gui.steps.navigation import get_user_menu
    context.execute_steps('''
        Then I open the user menu
    ''')
    user_menu = get_user_menu(context)
    organization = context.mist_config[organization].strip().lower()
    if get_current_org(user_menu) == organization:
        return True
    else:
        buttons = user_menu.find_elements(By.CSS_SELECTOR, 'paper-item')
        click_button_from_collection(context, organization, buttons)
        context.execute_steps('''
            Then I wait for the dashboard to load
            And I open the user menu
        ''')


@step('I should see the form to set name for new organization')
def ensure_onboarding_form_is_visible(context):
    dashboard = get_page_element(context, 'dashboard')
    dashboard_shadow = expand_shadow_root(context, dashboard)
    onb_element = dashboard_shadow.find_element(By.CSS_SELECTOR, 'onb-element')
    assert onb_element.is_displayed(), "Form to set name for new org \
        is not displayed"
