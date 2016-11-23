from time import sleep

from behave import step

from .buttons import clicketi_click
from .buttons import click_button_from_collection

from .utils import safe_get_element_text

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException

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

    css_selector = "//paper-dialog[@id='%s']" % modal_id
    if action == 'appear':
        try:
            WebDriverWait(context.browser, int(seconds)).until(
                EC.visibility_of_element_located((By.XPATH, css_selector)))
        except TimeoutException:
            raise TimeoutException("Modal %s did not %s after %s seconds"
                                   % (modal_id, action, seconds))
    elif action == 'disappear':
        try:
            WebDriverWait(context.browser, int(seconds)).until(
                EC.invisibility_of_element_located((By.XPATH, css_selector)))
        except TimeoutException:
            raise TimeoutException("Modal %s did not %s after %s seconds"
                                   % (modal_id, action, seconds))
    else:
        raise ValueError("Action can be either appear or disappear. Duh!")


@step(u'I click the "{text}" button inside the "{modal_id}" modal')
def click_button_within_modal(context, text, modal_id):

    modal = context.browser.find_element_by_xpath("//paper-dialog[@id='%s']" % modal_id)
    modal_items = modal.find_elements_by_tag_name("paper-item")
    for item in modal_items:
        if text.lower() == item.text.lower():
            clicketi_click(context, item)
            return
        else:
            pass

    raise NoSuchElementException("Could not find the %s button inside the %s modal" % (text, modal_id))
