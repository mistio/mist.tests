from behave import step

from .utils import focus_on_element
from .utils import safe_get_element_text

from .buttons import clicketi_click

# from tests.api.core import MistCoreApi as mist_core


@step(u'I revoke all api tokens')
def revoke_all_api_tokens(context):
    token_items = context.browser.find_elements_by_class_name('token-record')
    for token_item in token_items:
        revoke_btn = token_item.find_element_by_class_name('ui-btn')
        focus_on_element(context, revoke_btn)
        clicketi_click(context, revoke_btn)
        context.execute_steps(u'''
            Then I expect for "dialog-popup" popup to appear within max 4 seconds
            And I click the button "Yes"
            And I expect for "dialog-popup" popup to disappear within max 4 seconds
        ''')


@step(u'I revoke the api token with name {name}')
def revoke_all_api_tokens(context, name):
    token_items = context.browser.find_elements_by_class_name('token-record')
    for token_item in token_items:
        token_name = token_item.find_element_by_class_name('token-name')
        if name == safe_get_element_text(token_name):
            revoke_btn = token_item.find_element_by_class_name('ui-btn')
            focus_on_element(context, revoke_btn)
            clicketi_click(context, revoke_btn)
            context.execute_steps(u'''
                Then I expect for "dialog-popup" popup to appear within max 4 seconds
                And I click the button "Yes"
                And I expect for "dialog-popup" popup to disappear within max 4 seconds
                ''')


@step(u'I get the new api token value "{token_name}"')
def get_new_token_value(context, token_name):
    token_text_area = context.browser.find_element_by_id('new-token-value')
    context.mist_config[token_name] = token_text_area.get_attribute('value')


@step(u'I test the api token "{token_value}". It should {work_or_fail}.')
def test_api_token(context, token_value, work_or_fail):
    if work_or_fail not in ['work', 'fail']:
        raise ValueError('Token can either work or fail.')
    response = mist_core(context.mist_config['MIST_URL']).ping(api_token=context.mist_config[token_value]).post()
    if work_or_fail == 'work':
        assert response.status_code == 200, "Api token with value %s did not " \
                                            "work" % context.mist_config[token_value]
    if work_or_fail == 'fail':
        assert response.status_code == 401, "Api token with value %s did not " \
                                            "fail. Returned %s" \
                                            % (context.mist_config[token_value],
                                               response.status_code)


@step(u'I click the button "Never" from the ttl dropdown')
def click_inside_the_ttl_dropdown(context):
    dropbox = context.browser.find_element_by_id('new-token-ttl')
    options = dropbox.find_elements_by_tag_name('option')
    for option in options:
        if 'Never' in safe_get_element_text(option):
            option.click()