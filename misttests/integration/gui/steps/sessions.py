from behave import step

from selenium.webdriver.common.by import By

from misttests.integration.gui.steps.utils import focus_on_element

from misttests.integration.gui.steps.buttons import clicketi_click

from selenium.common.exceptions import NoSuchElementException


@step('I revoke all sessions')
def revoke_all_sessions(context):
    session_items = context.browser.find_elements(By.CSS_SELECTOR, '.session-record')
    for session_item in session_items:
        try:
            revoke_btn = session_item.find_element(By.CSS_SELECTOR, '.ui-btn')
            focus_on_element(context, revoke_btn)
            clicketi_click(context, revoke_btn)
            context.execute_steps('''
                Then I expect for "dialog-popup" popup to appear within max 4 seconds
                And I click the button "Yes"
                And I expect for "dialog-popup" popup to disappear within max 4 seconds
                ''')
        except NoSuchElementException:
            pass
