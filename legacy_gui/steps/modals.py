from time import sleep

from behave import step

from buttons import clicketi_click
from buttons import click_button_from_collection

from utils import safe_get_element_text

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@step(u'I expect for "{modal_id}" modal to {action} within max {seconds} '
      u'seconds')
def modal_waiting_with_timeout(context, modal_id, action, seconds):
    # dialog-popup
    """
    Function that wait for keyadd-popup to appear but for a maximum
    amount of time
    """
    if action == 'appear':
        css_selector = '#%s[class*="md-show"]' % modal_id
    elif action == 'disappear':
        css_selector = '#%s[class*="md-hide"]' % modal_id
    else:
        raise ValueError("Action can be either appear or disappear. Duh!")
    try:
        WebDriverWait(context.browser, int(seconds)).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    except TimeoutException:
        raise TimeoutException("Modal %s did not %s after %s seconds"
                               % (modal_id, action, seconds))


@step(u'I click the "{text}" button inside the "{modal_title}" modal')
def click_button_within_modal(context, text, modal_title):
    modals = context.browser.find_elements_by_class_name("md-show")
    for modal in modals:
        title = safe_get_element_text(modal.find_element_by_class_name('md-title'))
        if modal_title.lower() in title.lower():
            if text == '_x_':
                buttons = modal.find_elements_by_class_name("close")
                assert len(buttons) > 0, "Could not find the close button"
                for i in range(0, 2):
                    try:
                        clicketi_click(context, buttons[0])
                        return
                    except WebDriverException:
                        sleep(1)
                assert False, 'Could not click the close button'
            else:
                buttons = modal.find_elements_by_class_name("ui-btn")
                click_button_from_collection(context, text, buttons,
                                             'Could not find %s button in %s '
                                             'modal' % (text, modal_title))
            return
    assert False, "Could not find modal with title %s" % modal_title
