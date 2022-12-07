from behave import step

from selenium.webdriver.common.by import By

from misttests.integration.gui.steps.utils import focus_on_element, expand_shadow_root
from misttests.integration.gui.steps.utils import safe_get_element_text, get_page_element
from misttests.integration.gui.steps.buttons import clicketi_click


@step('I revoke token "{token}"')
def revoke_api_token(context, token):
    page_element = get_page_element(context, 'my-account')
    page_shadow = expand_shadow_root(context, page_element)
    active_section = page_shadow.find_element(By.CSS_SELECTOR, 'iron-pages > .iron-selected')
    section_shadow = expand_shadow_root(context, active_section)
    token_items = section_shadow.find_elements(By.CSS_SELECTOR, 'token-item')
    for token_item in token_items:
        if token in token_item.text:
            token_item_shadow = expand_shadow_root(context, token_item)
            revoke_btn = token_item_shadow.find_element(By.CSS_SELECTOR, '.red')
            focus_on_element(context, revoke_btn)
            clicketi_click(context, revoke_btn)
            break


@step('I get the new api token value "{token_name}"')
def get_new_token_value(context, token_name):
    from .dialog import get_dialog
    dialog = get_dialog(context, 'Copy your Token')
    dialog_shadow = expand_shadow_root(context, dialog)
    token_text_area = dialog_shadow.find_element(By.CSS_SELECTOR, 'paper-textarea#tokenValue')
    context.mist_config[token_name] = token_text_area.get_attribute('value')
    ok_btn = dialog_shadow.find_element(By.CSS_SELECTOR, 'paper-button')
    ok_btn.click()


@step('I test the api token "{token_value}". It should {work_or_fail}.')
def test_api_token(context, token_value, work_or_fail):
    from misttests.integration.api.main.io import MistIoApi as mist_api_v1
    if work_or_fail not in ['work', 'fail']:
        raise ValueError('Token can either work or fail.')
    response = mist_api_v1(context.mist_config['MIST_URL']).check_token(api_token=context.mist_config[token_value]).post()
    if work_or_fail == 'work':
        assert response.status_code == 200, "Api token with value %s did not " \
                                            "work" % context.mist_config[token_value]
    if work_or_fail == 'fail':
        assert response.status_code == 401, "Api token with value %s did not " \
                                            "fail. Returned %s" \
                                            % (context.mist_config[token_value],
                                               response.status_code)

