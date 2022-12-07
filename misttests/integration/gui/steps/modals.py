from behave import step

from misttests.integration.gui.steps.buttons import click_button_from_collection

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@step('I expect for "{modal_id}" modal to {action} within max {seconds} '
      'seconds')
def modal_waiting_with_timeout(context, modal_id, action, seconds):
    if action == 'appear':
        try:
            WebDriverWait(context.browser, int(seconds)).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#' + modal_id)))
        except TimeoutException:
            raise TimeoutException("Modal %s did not %s after %s seconds"
                                   % (modal_id, action, seconds))
    elif action == 'disappear':
        try:
            WebDriverWait(context.browser, int(seconds)).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, '#' + modal_id)))
        except TimeoutException:
            raise TimeoutException("Modal %s did not %s after %s seconds"
                                   % (modal_id, action, seconds))
    else:
        raise ValueError("Action can be either appear or disappear. Duh!")


@step('I click the "{text}" button inside the "{modal_id}" modal')
def click_button_within_modal(context, text, modal_id):
    try:
        modal = context.browser.find_element(By.CSS_SELECTOR, '#' + modal_id)
        buttons = modal.find_elements(By.CSS_SELECTOR, "paper-item")
        click_button_from_collection(context, text, buttons,
                                     'Could not find %s button in %s '
                                     'modal' % (text, modal_id))
        return
    except:
        assert False, "Could not find modal with id %s" % modal_id
