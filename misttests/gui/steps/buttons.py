from behave import step

from time import sleep

import logging

from .utils import safe_get_element_text
from .utils import focus_on_element

from .forms import find_dropdown
from .forms import get_current_value_of_dropdown

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.color import Color

from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


@step(u'I expect for "{element_id}" to be clickable within max {seconds} '
      u'seconds')
def become_visible_waiting_with_timeout(context, element_id, seconds):
    try:
        WebDriverWait(context.browser, int(seconds)).until(EC.element_to_be_clickable((By.ID, element_id)))
    except TimeoutException:
        raise TimeoutException("element with id %s did not become clickable "
                               "after %s seconds" % (element_id, seconds))


def clicketi_click(context, button):
    """
    trying two different ways of clicking a button because sometimes the
    Chrome driver for no apparent reason misinterprets the offset and
    size of the button
    """
    try:
        button.click()
    except WebDriverException:
        from selenium.webdriver.common import action_chains, keys
        action_chain = ActionChains(context.browser)
        action_chain.move_to_element(button)
        action_chain.click()
        action_chain.perform()


def clicketi_click_list_row(context, item):
    """
    This is a special clicketi click for list items that might not be clickable
    in the middle.
    """
    action_chain = ActionChains(context.browser)
    action_chain.move_to_element_with_offset(item, item.size['width'] / 4, item.size['height'] / 2)
    action_chain.click()
    action_chain.perform()


def click_button_from_collection(context, text, button_collection=None,
                                 error_message="Could not find button"):
    if not button_collection:
        try:
            button_collection = context.browser.find_elements_by_tag_name('paper-button')
        except NoSuchElementException:
            button_collection = context.browser.find_elements_by_class_name('ui-btn')
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


@step(u'I click the button "{button}" in the "{name}" dropdown')
def click_button_in_dropdown(context, button, name):
    button = button.strip().lower()
    dropdown = find_dropdown(context, name.lower())
    if button == get_current_value_of_dropdown(dropdown):
        return True
    buttons = dropdown.find_elements_by_tag_name('paper-item')
    click_button_from_collection(context, button.lower(), buttons)


@step(u'I click the "{button}" button in the dropdown with id "{dropdown_id}"')
def click_button_in_dropdown_with_id(context, button, dropdown_id):
    button = button.strip().lower()
    dropdown = context.browser.find_element_by_xpath('//paper-menu[@id="%s"]' % dropdown_id)
    if button == get_current_value_of_dropdown(dropdown):
        return True
    buttons = dropdown.find_elements_by_tag_name('paper-item')
    click_button_from_collection(context, button.lower(), buttons)


@step(u'I click the button "{button}" in the tag menu')
def click_button_in_tag_model(context, button):
    from .tags import get_open_tag_modal
    buttons = get_open_tag_modal(context, False).\
        find_elements_by_tag_name('paper-button')
    click_button_from_collection(context, button, buttons)


@step(u'I click the button "{button}" in the user menu')
def click_the_user_menu_button(context, button):
    dropdown = context.browser.find_element_by_css_selector('app-user-menu #dropdown')
    buttons = dropdown.find_elements_by_tag_name('paper-item')
    click_button_from_collection(context, button, buttons)


@step(u'I click the action "{button}" from the {resource_type} list actions')
def click_action_of_list(context,button,resource_type):
    resource_type = resource_type.lower()
    if resource_type not in ['machine', 'key', 'script', 'network', 'team', 'template', 'stack', 'image', 'schedule', 'record']:
        raise Exception('Unknown resource type')
    if resource_type == 'record':
        records = context.browser.find_element_by_tag_name('list-records')
        actions = records.find_element_by_id('actions')
        div = actions.find_element_by_tag_name('div')
        buttons = div.find_elements_by_tag_name('paper-button')
    else:
        buttons = context.browser.find_elements_by_css_selector('page-%ss mist-list mist-actions > paper-button' % resource_type)
    click_button_from_collection(context, button.lower(), buttons)


@step(u'I click the "{text}" "{type_of_item}"')
def click_item(context, text, type_of_item):
    type_of_item = type_of_item.lower()
    if type_of_item not in ['machine', 'key', 'script', 'network', 'team', 'template', 'stack', 'image', 'schedule', 'zone']:
        raise Exception('Unknown type of button')
    if context.mist_config.get(text):
        text = context.mist_config[text]
    text = text.lower()
    if type_of_item in ['machine', 'team', 'key', 'script', 'network', 'template', 'stack', 'schedule', 'zone']:
        item_selector = 'page-%ss mist-list vaadin-grid-table-body#items > vaadin-grid-table-row' % type_of_item
    else:
        item_selector = 'page-%ss iron-list div.row' % type_of_item
    items = context.browser.find_elements_by_css_selector(item_selector)
    for item in items:
        if type_of_item in ['machine', 'team', 'key', 'script', 'network', 'template', 'stack', 'schedule', 'zone']:
            name = safe_get_element_text(item.find_element_by_css_selector('strong.name')).strip().lower()
            if text in name:
                clicketi_click_list_row(context, item)
                return True
        else:
            name = safe_get_element_text(item.find_element_by_css_selector('div.name')).strip().lower()
            if text == name:
                clicketi_click_list_row(context, item)
                return True
    assert False, "Could not click item %s" % text


@step(u'cloud "{search_cloud}" should be "{state}"')
def state_of_cloud(context,search_cloud,state):
    from .clouds import find_cloud
    cloud = find_cloud(context,search_cloud.lower())
    if not cloud:
        assert False, "Cloud %s is not added" % cloud
    if state not in ['enabled','disabled']:
        raise Exception('Unknown type of state')
    button_state = cloud.find_element_by_class_name('icon').value_of_css_property('background-color')

    color = Color.from_string(button_state).hex
    actual_state = get_color_from_state(state)
    if color != actual_state:
        assert False, "Cloud should be %s, but it is not" % state


def get_color_from_state(state):
    if state == 'enabled':
        return '#69b46c'
    elif state == 'disabled':
        return '#d96557'
    return None


@step(u'I click the mist.io button')
def click_mist_io(context):
    clicketi_click(context, context.browser.find_element_by_id('logo-link'))


@step(u'I click the "{button}" button')
def click_button_by_class(context,button):
    if button == 'more options':
        button_to_click = context.browser.find_element_by_class_name('more')
    elif button == 'Add graph':
        button_to_click = context.browser.find_element_by_class_name('add-button')
    else:
        raise Exception('Unknown type of button')


@step(u'I click the "{button}" button with id "{button_id}"')
def click_button_by_id(context, button, button_id):
    button_to_click = context.browser.find_element_by_id(button_id)
    clicketi_click(context, button_to_click)


@step(u'I click the mist-logo')
def visit_home_url(context):
    save_title_button = context.browser.find_element_by_id('logo-link')
    clicketi_click(context, save_title_button)


@step(u'I click the Gravatar')
def click_the_gravatar(context):
    try:
        gravatar = context.browser.find_element_by_css_selector('paper-icon-button.gravatar')
        clicketi_click(context, gravatar)
    except NoSuchElementException:
        get_old_gravatar(context)


def get_old_gravatar(context):
    from .popups import popup_waiting_with_timeout
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
