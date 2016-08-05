from behave import step

from .utils import safe_get_element_text
from .navigation import get_gravatar


def get_current_context(context):
    return safe_get_element_text(context.browser.find_element_by_css_selector(
            'div.current.context').find_element_by_tag_name('h4')).strip().lower()


@step(u'I ensure that I am in the "{organization}" organization context')
def ensure_organizational_context(context, organization):
    context.execute_steps(u'''
        Then I click the Gravatar
        And I wait for 1 seconds
    ''')
    organization = organization.strip().lower()
    if get_current_context(context) == organization:
        return True
    else:
        buttons = context.browser.find_element_by_id('topBar'). \
            find_element_by_id('dropdown').\
            find_elements_by_tag_name('paper-item')
        click_button_from_collection(context, organization, buttons)
        context.execute_steps(u'''
            Then I wait for the dashboard to load
            And I click the Gravatar
            And I wait for 1 seconds
        ''')
    assert get_current_context(context) == organization, \
        "Organizational context has not been changed"


@step(u'I should see the form to set name for new organization')
def ensure_onboarding_form_is_visible(context):
    context.browser.find_element_by_css_selector('div.onboarding-form-inputs').\
        is_displayed()
