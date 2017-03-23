from time import sleep

from behave import step

from .utils import safe_get_element_text

from .buttons import clicketi_click
from .buttons import click_button_from_collection

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@step(u'I expect for "{popup_id}" popup to {action} within max {seconds} '
      u'seconds')
def popup_waiting_with_timeout(context, popup_id, action, seconds):
    """
    Function that wait for keyadd-popup to appear but for a maximum
    amount of time
    """
    if action == 'appear':
        css_selector = '#%s[class*="ui-popup-active"]' % popup_id
    elif action == 'disappear':
        css_selector = '#%s[class*="ui-popup-hidden"]' % popup_id
    else:
        raise ValueError("Action can be either appear or disappear. Duh!")
    try:
        WebDriverWait(context.browser, int(seconds)).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    except TimeoutException:
        raise TimeoutException("Popup %s did not %s after %s seconds"
                               % (popup_id, action, seconds))


@step(u'I click the "{text}" button inside the popup with id "{popup_id}"')
def click_button_within_popup_with_id(context, text, popup_id):
    if context.mist_config.get(text):
        text = context.mist_config.get(text)
    popup = context.browser.find_element_by_id(popup_id)
    if "ui-popup-active" not in popup.get_attribute('class'):
        raise Exception("Popup with id %s is not open" % popup_id)
    if text == '_x_':
        buttons = popup.find_elements_by_class_name("close")
        assert len(buttons) > 0, "Could not find the close button"
        for i in range(0, 2):
            try:
                clicketi_click(context, buttons[0])
                return
            except WebDriverException:
                sleep(1)
        assert False, 'Could not click the close button'
    else:
        buttons = popup.find_elements_by_class_name("ui-btn")
        click_button_from_collection(context, text, buttons,
                                     'Could not find %s button in popup'
                                     'with id  %s' % (text, popup_id))
        return


@step(u'I click the "{text}" button inside the "{popup}" popup')
def click_button_within_popup(context, text, popup):
    popups = context.browser.find_elements_by_class_name("ui-popup-active")
    for pop in popups:
        title = safe_get_element_text(pop.find_element_by_class_name('ui-title'))
        if popup.lower() in title.lower():
            if text == '_x_':
                buttons = pop.find_elements_by_class_name("close")
                assert len(buttons) > 0, "Could not find the close button"
                for i in range(0, 2):
                    try:
                        clicketi_click(context, buttons[0])
                        return
                    except WebDriverException:
                        sleep(1)
                assert False, 'Could not click the close button'
            else:
                buttons = pop.find_elements_by_class_name("ui-btn")
                click_button_from_collection(context, text, buttons,
                                             'Could not find %s button in %s '
                                             'popup' % (text, popup))
                return
    assert False, "Could not find popup with title %s" % popup


@step(u'I close the "{object_id}" popup')
def close_popup(context, object_id):
    objectId = 'modal' + object_id
    context.browser.find_element_by_id(objectId).find_element_by_class_name(
                   'modal-close').click()
