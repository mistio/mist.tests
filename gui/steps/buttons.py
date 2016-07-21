from behave import step

from time import sleep
from time import time

from .utils import safe_get_element_text
from .utils import focus_on_element
from .utils import find_dropdown

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


@step(u'I expect for "{element_id}" to be clickable within max {seconds} '
      u'seconds')
def become_visible_waiting_with_timeout(context, element_id, seconds):
    try:
        WebDriverWait(context.browser, int(seconds)).until(EC.element_to_be_clickable((By.ID, element_id)))
    except TimeoutException:
        raise TimeoutException("element with id %s did not become clickable "
                               "after %s seconds" % (element_id, seconds))


@step(u'I click the button "{button}" in the "{name}" dropdown')
def click_button_in_dropdown(context, button, name):
    dropdown = find_dropdown(context, name.lower())
    buttons = dropdown.find_elements_by_tag_name('paper-item')
    click_button_from_collection(context, button.lower(), buttons)


def click_button_from_collection(context, text, button_collection=None,
                                 error_message="Could not find button"):
    button = search_for_button(context, text.lower(), button_collection)
    assert button, error_message
    for i in range(0, 2):
        try:
            clicketi_click(context, button)
            return
        except WebDriverException:
            sleep(1)
        assert False, 'Could not click button that says %s(%s)' % \
                      (safe_get_element_text(button), text)


def search_for_button(context, text, button_collection=None):
    if not button_collection:
        try:
            context.browser.find_element_by_id('app')
            button_collection = context.browser.find_elements_by_tag_name('paper-button')
        except NoSuchElementException:
            button_collection = context.browser.find_elements_by_class_name('ui-btn')

    # search for button with exactly the same text. sometimes the driver returns
    # the same element more than once and that's why we return the first
    # element of the list
    # also doing some cleaning if the text attribute also sends back texts
    # of sub elements
    button = filter(lambda el: safe_get_element_text(el).strip().lower() == text,
                    button_collection)

    if button:
        return button[0]

    # if we haven't found the exact text then we search for something that
    # looks like it
    for button in button_collection:
        button_text = safe_get_element_text(button).split('\n')
        if len(filter(lambda b: text in b.lower(), button_text)) > 0:
            return button

    return None


def clicketi_click(context, button):
    """
    trying two different ways of clicking a button because sometimes the
    Chrome driver for no apparent reason misinterprets the offset and
    size of the button
    """
    try:
        button.click()
    except WebDriverException:
        action_chain = ActionChains(context.browser)
        action_chain.move_to_element(button)
        action_chain.click()
        action_chain.perform()


@step(u'I expect for buttons inside "{element_id}" to be '
      u'clickable within max {seconds} seconds')
def become_clickable_waiting_with_timeout(context, element_id, seconds):
    try:
        wrapper = context.browser.find_element_by_id(element_id)
        WebDriverWait(wrapper, int(seconds)).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-btn')))
    except TimeoutException:
        raise TimeoutException("element with id %s did not become visible "
                               "after %s seconds" % (element_id, seconds))


@step(u'I click button "{button_text}" inside "{element_id}" when '
      u'it is clickable within max {seconds} seconds')
def button_become_clickable_waiting_with_timeout(context, button_text,
                                                 element_id, seconds):
    timeout = time() + int(seconds)
    wrapper = context.browser.find_element_by_id(element_id)
    button = search_for_button(context, button_text, wrapper.find_elements_by_class_name('ui-btn'))
    while time() < timeout:
        try:
            button.click()
            return
        except:
            pass
        assert time() + 1 < timeout, "Button %s inside element %s did not " \
                                     "become clickable after %s seconds" % \
                                     (button_text, element_id, seconds)
        sleep(1)


@step(u'I click the button by "{id_name}" id_name')
def click_button_id(context, id_name):
    """
    This function will try to click a button by id name.
    And use the function clicketi_click
    """
    my_element = context.browser.find_element_by_id(id_name)
    clicketi_click(context, my_element)


@step(u'I click the button "{text}"')
def click_button(context, text):
    """
    This function will try to click a button that says exactly the same thing as
    the text given. If it doesn't find any button like that then it will try
    to find a button that contains the text given. If text is a key inside
    mist_config dict then it's value will be used.
    """
    if context.mist_config.get(text):
        text = context.mist_config[text]
    if text == '+':
        plus_button = filter(
            lambda el: el.is_displayed() and el.get_attribute('icon') == 'add',
            context.browser.find_elements_by_tag_name('paper-fab'))
        assert plus_button, 'Could not find + button'
        clicketi_click(context, plus_button[0])
        return True
    click_button_from_collection(context, text.lower(),
                                 error_message='Could not find button that '
                                               'contains %s' % text)


@step(u'I click the mist.io button')
def click_mist_io(context):
    clicketi_click(context, context.browser.find_element_by_id('logo-link'))


@step(u'I click the Gravatar')
def click_the_gravatar(context):
    """
    This function tries to click the gravatar button. It has a ridiculous amount
    of code because there is a ridiculous amount of errors happening during
    this simple task. It tries to print the reasons why it didn't work
    """
    from .popups import popup_waiting_with_timeout
    msg = ""
    gravatar = context.browser.find_element_by_class_name("gravatar-image")
    focus_on_element(context, gravatar)
    me_button = context.browser.find_element_by_id('me-btn')
    try:
        clicketi_click(context, me_button)
        WebDriverWait(context.browser, int(2)).until(
            EC.visibility_of_element_located((By.ID, 'user-menu-popup-screen')))
        popup_waiting_with_timeout(context, 'user-menu-popup-popup', 'appear', 4)
        return
    except:
        pass
    try:
        clicketi_click(context, gravatar)
        WebDriverWait(context.browser, int(2)).until(
            EC.visibility_of_element_located((By.ID, 'user-menu-popup-screen')))
        popup_waiting_with_timeout(context, 'user-menu-popup-popup', 'appear', 4)
        return
    except:
        pass

    try:
        clicketi_click(context, gravatar)
        try:
            WebDriverWait(context.browser, int(2)).until(
                EC.visibility_of_element_located((By.ID,
                                                  'user-menu-popup-screen')))
            try:
                popup_waiting_with_timeout(context, 'user-menu-popup-popup',
                                           'appear', 4)
                return
            except Exception as e:
                msg = "After clicking the gravatar the grey background " \
                      "appeared but not the popup.(%s)" % type(e)
        except Exception as e:
            msg = "Grey background did not appear after 2 seconds." \
                  "(%s)" % type(e)
    except Exception as e:
        msg = "There was an exception(%s) when trying to click the Gravatar" \
              " image" % type(e)

    try:
        clicketi_click(context, me_button)
        try:
            WebDriverWait(context.browser, int(2)).until(
                EC.visibility_of_element_located((By.ID, 'user-menu-popup-screen')))
            try:
                popup_waiting_with_timeout(context, 'user-menu-popup-popup',
                                           'appear', 4)
                return
            except Exception as e:
                msg += "\nAfter clicking the me-btn the grey background " \
                       "appeared but not the popup.(%s)" % type(e)
        except Exception as e:
            msg += "\nGrey background did not appear after 2 seconds." \
                   "(%s)" % type(e)
    except Exception as e:
        msg += "\nThere was an exception(%s) when trying to click the " \
               "me-btn" % type(e)

    assert False, "I tried clicking the Gravatar but it did not work :(." \
                  "\n%s" % msg
