from behave import step

from .utils import focus_on_element
from .utils import safe_get_element_text
from .buttons import clicketi_click


@step(u'I revoke all api tokens')
def revoke_all_api_tokens(context):
    tokens_list = context.browser.find_element_by_id('tokens-list')
    token_items = tokens_list.find_elements_by_tag_name('token-item')

    for token_item in token_items:
        revoke_btn = token_item.find_element_by_class_name('red')
        focus_on_element(context, revoke_btn)
        clicketi_click(context, revoke_btn)


@step(u'I get the new api token value "{token_name}"')
def get_new_token_value(context, token_name):
    token_text_area = context.browser.find_element_by_id('tokenValue')
    context.mist_config[token_name] = token_text_area.get_attribute('value')
    copy_token_dialog = context.browser.find_element_by_id('copyToken')
    ok_btn = copy_token_dialog.find_element_by_tag_name('paper-button')
    ok_btn.click()


@step(u'I test the api token "{token_value}". It should {work_or_fail}.')
def test_api_token(context, token_value, work_or_fail):
    from misttests.integration.api.plugin.core import MistCoreApi as mist_core
    if work_or_fail not in ['work', 'fail']:
        raise ValueError('Token can either work or fail.')
    response = mist_core(context.mist_config['MIST_URL']).check_token(api_token=context.mist_config[token_value]).post()
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
    dropbox = context.browser.find_element_by_id('tokenExpires')
    dropbox.click()
    options = dropbox.find_elements_by_tag_name('paper-item')
    for option in options:
        if option.get_attribute("value")=='0':
            option.click()
