from behave import step, when, use_step_matcher

from time import sleep, time

import logging

from .utils import safe_get_element_text, scroll_into_view
from .utils import focus_on_element, get_page_element, expand_shadow_root

from .forms import find_dropdown, get_button_from_form
from .forms import get_current_value_of_dropdown

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.color import Color

from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def clicketi_click(context, button):
    """
    trying two different ways of clicking a button because sometimes the
    Chrome driver for no apparent reason misinterprets the offset and
    size of the button
    """
    try:
        button.click()
    except WebDriverException:
        try:
            scroll_into_view(context, button)
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
    button = search_for_button(context, text, button_collection)
    assert button, error_message
    for i in range(0, 2):
        try:
            button.click()
            return
        except WebDriverException:
            scroll_into_view(context, button)
            clicketi_click(context, button)
            return
        except WebDriverException:
            sleep(1)
        assert False, 'Could not click button that says %s(%s)' % \
                      (safe_get_element_text(button), text)


def search_for_button(context, text, button_collection):
    for button in button_collection:
        if safe_get_element_text(button).strip().lower() == text.lower():
            return button


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
        page_shadow = expand_shadow_root(context, get_page_element(context))
        fabs = page_shadow.find_elements_by_css_selector('paper-fab')
        assert fabs, 'Could not find + button'
        clicketi_click(context, fabs[0])
        return True
    click_button_from_collection(context, text.lower(),
                                 error_message='Could not find button that '
                                               'contains %s' % text)


@step(u'I click the "{button}" button in the "{name}" dropdown within "{container}"')
def click_button_in_dropdown_within_container(context, container, button, name):
    button = button.strip().lower()
    dropdown = find_dropdown(context, container, name.lower())
    if button == get_current_value_of_dropdown(dropdown):
        return True
    buttons = dropdown.find_elements_by_css_selector('paper-item')
    click_button_from_collection(context, button.lower(), buttons)


@step(u'I click the "{button_name}" button in the "{dropdown_name}" dropdown in the "{resource_type}" add form')
def click_button_in_dropdown(context, button_name, dropdown_name, resource_type):
    from .forms import get_add_form
    page = get_add_form(context, resource_type)
    page_shadow = expand_shadow_root(context, page)
    click_button_in_dropdown_within_container(context, page_shadow, button_name, dropdown_name)


use_step_matcher("re")
@step(u'I click the "(?P<button_name>[A-Za-z ]+)" toggle button in the "(?P<resource_type>[A-Za-z]+)" add form')
def click_toggle_button_in_add_form(context, button_name, resource_type):
    from .forms import get_add_form
    form = get_add_form(context, resource_type)
    form_shadow = expand_shadow_root(context, form)
    button = get_button_from_form(context, form_shadow, button_name, tag_name='paper-toggle-button')
    clicketi_click(context, button)

@step(u'I click the "(?P<button_name>[A-Za-z ]+)" radio button in the "(?P<resource_type>[A-Za-z]+)" add form')
def click_toggle_button_in_add_form(context, button_name, resource_type):
    from .forms import get_add_form
    form = get_add_form(context, resource_type)
    form_shadow = expand_shadow_root(context, form)
    button = get_button_from_form(context, form_shadow, button_name, tag_name='paper-radio-button')
    clicketi_click(context, button)


use_step_matcher("parse")
@step(u'I click the "{button}" button in the dropdown with id "{dropdown_id}" within "{container_id}"')
def click_button_in_dropdown_with_id_within_container(context, button, dropdown_id, container_id=None):
    button = button.strip().lower()
    if container_id:
        container = context.browser.find_element_by_id(container_id)
    else:
        container = context.browser
    dropdown = container.find_element_by_id(dropdown_id)
    if button == get_current_value_of_dropdown(dropdown):
        return True
    buttons = dropdown.find_elements_by_tag_name('paper-item')
    click_button_from_collection(context, button.lower(), buttons)


@step(u'I click the "{button}" button in the dropdown with id "{dropdown_id}"')
def click_button_in_dropdown_with_id(context, button, dropdown_id):
    click_button_in_dropdown_with_id_within_container(context, button, dropdown_id)


@step(u'I open the "{dropdown}" mist-dropdown within "{container_id}"')
def open_mist_dropdown(context, dropdown, container_id=None):
    if dropdown not in ['teams', 'members']:
        raise Exception('Unknown mist-dropdown')
    if container_id:
        mist_dropdowns = context.browser.find_element_by_id(container_id).find_elements_by_tag_name('mist-dropdown-multi')
    else:
        mist_dropdowns = context.browser.find_elements_by_tag_name('mist-dropdown-multi')
    if dropdown == 'teams':
        clicketi_click(context, mist_dropdowns[0])
    else:
        clicketi_click(context, mist_dropdowns[1])


@step(u'I select "{members}" in "{dropdown}" mist-dropdown within "{container_id}"')
def select_members_in_mist_dropdown(context, members, dropdown, container_id=None):
    if dropdown not in ['teams', 'members']:
        raise Exception('Unknown mist-dropdown')
    if container_id:
        mist_dropdowns = context.browser.find_element_by_id(container_id).find_elements_by_tag_name('mist-dropdown-multi')
    else:
        mist_dropdowns = context.browser.find_elements_by_tag_name('mist-dropdown-multi')
    if dropdown == 'teams':
        mist_dropdown = mist_dropdowns[0]
    else:
        mist_dropdown = mist_dropdowns[1]
    options = mist_dropdown.find_elements_by_tag_name('paper-checkbox')
    for option in options:
        if members in option.text:
            clicketi_click(context, option)
            return
    assert False, "Could not find %s option in %s mist-dropdown" % (members, dropdown)


@step(u'I click the button "{button}" in the tag dialog')
def click_button_in_tag_dialog(context, button):
    from .dialog import get_dialog
    buttons = get_dialog(context, "Tags").\
        find_elements_by_tag_name('paper-button')
    click_button_from_collection(context, button, buttons)


@step(u'I click the button "{button}" in the user menu')
def click_the_user_menu_button(context, button):
    from .navigation import click_user_icon_and_wait_for_menu, get_user_menu
    click_user_icon_and_wait_for_menu(context)
    user_menu = get_user_menu(context)
    timeout = time() + 5
    dimensions = None
    while time() < timeout:
        try:
            if dimensions is None:
                dimensions = user_menu.size
            elif dimensions['width'] == user_menu.size['width'] and \
                            dimensions['height'] == user_menu.size['height']:
                sleep(1)
                click_button_from_collection(context, button,
                                             user_menu.find_elements_by_css_selector(
                                                 'paper-item'))
                return True
            else:
                dimensions = user_menu.size
        except NoSuchElementException:
            pass
        sleep(1)
    assert False, "User menu has not appeared yet"


@step(u'I click the action "{button_text}" from the {resource_type} list actions')
def click_action_of_list(context, button_text, resource_type):
    resource_type = resource_type.lower()
    if resource_type not in ['machine', 'key', 'script', 'network', 'team', 'template', 'stack', 'image', 'schedule', 'record']:
        raise Exception('Unknown resource type')
    container = get_page_element(context, resource_type + 's')
    container_shadow = expand_shadow_root(context, container)
    mist_list = container_shadow.find_element_by_css_selector('mist-list')
    list_shadow = expand_shadow_root(context, mist_list)
    actions = list_shadow.find_element_by_css_selector('mist-list-actions')
    actions_shadow = expand_shadow_root(context, actions)
    buttons = actions_shadow.find_elements_by_css_selector(':host > paper-button:not([hidden])')
    button = search_for_button(context, button_text, buttons)
    if not button:
        try:
            more_menu_button = actions_shadow.find_element_by_css_selector(':host > paper-menu-button')
            clicketi_click(context, more_menu_button)
            sleep(.2)
            more_buttons = more_menu_button.find_elements_by_css_selector('.dropdown-content > paper-button')
            button = search_for_button(context, button_text, more_buttons)
        except NoSuchElementException:
            assert False, "Could not find %s action button"
    clicketi_click(context, button)


@step(u'I click the "{text}" "{resource_type}"')
def click_item(context, text, resource_type):
    resource_type = resource_type.lower()
    if resource_type not in ['machine', 'key', 'script', 'network', 'team', 'template', 'stack', 'image', 'schedule', 'zone']:
        raise Exception('Unknown type of button')
    if context.mist_config.get(text):
        text = context.mist_config[text]
    text = text.lower()
    container = get_page_element(context, resource_type + 's')
    container_shadow = expand_shadow_root(context, container)
    mist_list = container_shadow.find_element_by_css_selector('mist-list')
    list_shadow = expand_shadow_root(context, mist_list)
    items = list_shadow.find_elements_by_css_selector('strong.name')
    for item in items:
        if resource_type in ['machine', 'image', 'team', 'key', 'script', 'network', 'template', 'stack', 'schedule', 'zone']:
            name = safe_get_element_text(item).strip().lower()
            if text == name:
                clicketi_click(context, item)
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


@step(u'I click the mist logo')
def click_mist_logo(context):
    mist_app = context.browser.find_element_by_tag_name('mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    mist_header = mist_app_shadow.find_element_by_css_selector('mist-header')
    mist_header_shadow = expand_shadow_root(context, mist_header)
    clicketi_click(context, mist_header_shadow.find_element_by_css_selector('a#logo-link'))


@step(u'I click the "{button}" button')
def click_button_by_class(context,button):
    if button == 'more options':
        button_to_click = context.browser.find_element_by_class_name('more')
    elif button == 'Add graph':
        button_to_click = context.browser.find_element_by_class_name('add-button')
    else:
        raise Exception('Unknown type of button')


@step(u'I click the "{button}" button with id "{button_id}" within "{container_id}"')
def click_button_by_id_within_container(context, button, button_id, container_id=None):
    if container_id:
        container = context.browser.find_element_by_id(container_id)
    else:
        container = context.browser
    button_to_click = container.find_element_by_id(button_id)
    clicketi_click(context, button_to_click)


@step(u'I click the "{button}" button with id "{button_id}"')
def click_button_by_id(context, button, button_id):
    click_button_by_id_within_container(context, button, button_id)


@step(u'I click the toggle button in the "{page_title}" page')
def click_toggle_in_page(context, page_title):
    _, page_element = get_page_element(context, page_title + 's', page_title)
    page_shadow = expand_shadow_root(context, page_element)
    toggle_button = page_shadow.find_element_by_css_selector('paper-toggle-button')
    clicketi_click(context, toggle_button)


@step(u'I click the mist-logo')
def visit_home_url(context):
    save_title_button = context.browser.find_element_by_id('logo-link')
    clicketi_click(context, save_title_button)


@step(u'I click the user icon')
def click_the_user_icon(context):
    mist_app = context.browser.find_element_by_tag_name('mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    mist_header = mist_app_shadow.find_element_by_css_selector('mist-header')
    mist_header_shadow = expand_shadow_root(context, mist_header)
    app_user_menu = mist_header_shadow.find_element_by_css_selector('app-user-menu')
    app_user_menu_shadow = expand_shadow_root(context, app_user_menu)
    gravatar = app_user_menu_shadow.find_element_by_css_selector('paper-icon-button.gravatar')
    clicketi_click(context, gravatar)


use_step_matcher("re")
@step(u'I click the "(?P<action>[A-Za-z ]+)" action button in the "(?P<resource_type>[A-Za-z]+)" page')
def click_action_in_resource_page(context, action, resource_type):
    _, container = get_page_element(context, resource_type + 's', resource_type)
    container_shadow = expand_shadow_root(context, container)
    resource_actions = container_shadow.find_element_by_css_selector('%s-actions' % resource_type)
    resource_actions_shadow = expand_shadow_root(context, resource_actions)
    mist_list_actions = resource_actions_shadow.find_element_by_css_selector('mist-list-actions')
    mist_list_actions_shadow = expand_shadow_root(context, mist_list_actions)
    buttons = mist_list_actions_shadow.find_elements_by_css_selector(':host > paper-button')
    if search_for_button(context, action.lower(), buttons):
        click_button_from_collection(context, action.lower(), buttons)
    else:
        more_button = mist_list_actions_shadow.find_element_by_css_selector(':host > paper-menu-button')
        clicketi_click(context, more_button)
        sleep(.5)
        buttons = mist_list_actions_shadow.find_elements_by_css_selector(':host > paper-menu-button paper-button')
        click_button_from_collection(context, action.lower(), buttons)


use_step_matcher('parse')
@step(u'I click the fab button in the "{page_title}" page')
def click_fab_button_in_page(context, page_title):
    page_element = get_page_element(context, page_title)
    page_shadow = expand_shadow_root(context, page_element)
    fab = page_shadow.find_element_by_css_selector('paper-fab')
    clicketi_click(context, fab)


@step(u'I click the "{target}" tab in the account page')
def click_tab_in_page(context, target):
    page_element = get_page_element(context, 'my-account')
    page_shadow = expand_shadow_root(context, page_element)
    for tab in page_shadow.find_elements_by_css_selector('paper-tab:not([hidden])'):
        if target.lower() in tab.text.lower():
            clicketi_click(context, tab)
            return
    assert False, 'Cannot find tab "%s"' % target

@step(u'I click the "{target}" button in the account page')
def click_button_in_account_page(context, target):
    page_element = get_page_element(context, 'my-account')
    page_shadow = expand_shadow_root(context, page_element)
    active_section = page_shadow.find_element_by_css_selector('iron-pages > .iron-selected')
    section_shadow = expand_shadow_root(context, active_section)
    for button in section_shadow.find_elements_by_css_selector('paper-button:not([hidden])'):
        if target.lower() in button.text.lower():
            button.click()
            return
    assert False, 'Cannot find button "%s" in account page' % target
