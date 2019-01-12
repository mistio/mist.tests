from behave import step

from .utils import safe_get_element_text
from .buttons import click_button_from_collection


def get_current_org(user_menu):
    return safe_get_element_text(user_menu.find_element_by_css_selector(
            'div.current.context').find_element_by_tag_name('h4')).\
        strip().lower()


@step(u'I ensure that I am in the "{organization}" organization context')
def ensure_organizational_context(context, organization):
    from .navigation import get_user_menu
    context.execute_steps(u'''
        Then I open the user menu
    ''')
    user_menu = get_user_menu(context)
    organization = context.mist_config[organization].strip().lower()
    if get_current_org(user_menu) == organization:
        return True
    else:
        buttons = user_menu.find_elements_by_css_selector('paper-item')
        click_button_from_collection(context, organization, buttons)
        context.execute_steps(u'''
            Then I wait for the dashboard to load
            And I open the user menu
        ''')
    assert get_current_context(user_menu) == organization, \
        "Organizational context has not been changed"


@step(u'I should see the form to set name for new organization')
def ensure_onboarding_form_is_visible(context):
    context.browser.find_element_by_css_selector(
        'div.onboarding-form-inputs').is_displayed()
