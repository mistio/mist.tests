from behave import step

from utils import focus_on_element

from buttons import clicketi_click

from selenium.common.exceptions import NoSuchElementException


@step(u'I revoke all sessions')
def revoke_all_sessions(context):
    session_items = context.browser.find_elements_by_class_name('session-record')
    for session_item in session_items:
        try:
            revoke_btn = session_item.find_element_by_class_name('ui-btn')
            focus_on_element(context, revoke_btn)
            clicketi_click(context, revoke_btn)
            context.execute_steps(u'''
                Then I expect for "dialog-popup" popup to appear within max 4 seconds
                And I click the button "Yes"
                And I expect for "dialog-popup" popup to disappear within max 4 seconds
                ''')
        except NoSuchElementException:
            pass