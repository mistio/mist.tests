from behave import step, use_step_matcher

from .utils import focus_on_element, get_page_element, clear_input_and_send_keys
from .utils import safe_get_element_text, expand_shadow_root, expand_slot

from selenium.common.exceptions import NoSuchElementException

from time import time
from time import sleep

from random import randrange


def get_add_form(context, title):
    title = title.lower()
    if title not in ['cloud', 'machine', 'image', 'key', 'network', 'tunnel',
                     'script', 'schedule', 'template', 'stack', 'team',
                     'members', 'zone', 'record']:
        raise ValueError('The title given is unknown')
    if title == 'members':
        page_element = get_page_element(context, 'teams')
    else:
        page_element = get_page_element(context, title + 's')
    page_shadow = expand_shadow_root(context, page_element)
    if title in ['stack', 'machine', 'network']:
        add_form_selector = '%s-create' % title
    else:
        add_form_selector = '%s-add' % title
    return page_shadow.find_element_by_css_selector(add_form_selector)


def get_edit_form(context, title):
    title = title.lower()
    import ipdb;ipdb.set_trace()
    if title not in ['machine', 'image', 'key', 'network', 'tunnel', 'script',
                     'template', 'stack', 'team', 'policy', 'cloud', 'schedule', 'zone']:
        raise Exception('The title given is unknown')
    try:
        if title == 'policy':
            page_teams_element = get_page_element(context, 'teams')
            page_teams_shadow = expand_shadow_root(context, page_teams_element)
            return expand_shadow_root(context, page_teams_shadow.find_element_by_css_selector('team-page')) #.find_element_by_css_selector'team-policy')
            # return context.browser.find_element_by_tag_name('team-policy')
        page_shadow = expand_shadow_root(context, get_page_element(context, title + 's'))
        return page_shadow
    except NoSuchElementException:
        return None


@step(u'I expect the "{page}" {form_type} form to be visible within max '
      u'{seconds} seconds')
def check_form_is_visible(context, page, form_type, seconds):
    form_type = form_type.lower()
    if form_type not in ['add', 'edit']:
        raise Exception('Unknown type of form')
    msg = "%s %s form is not visible after %s seconds" \
          % (page, form_type, seconds)
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            form = get_add_form(context, page) if form_type == 'add' else \
                get_edit_form(context, page)
            form_shadow = expand_shadow_root(context, form)
            if form and form.is_displayed():
                return True
        except NoSuchElementException:
            pass
        sleep(1)
    assert False, msg


def get_input_element_from_form(context, form, input_name):
    input_element = None
    input_containers = form.find_elements_by_css_selector('paper-input, paper-textarea')
    form_containers = form.find_elements_by_css_selector('cloud-edit')
    form_containers_shadow = [expand_shadow_root(context, f) for f in form_containers]
    form_containers_shadow.append(form)
    for form in form_containers_shadow:
        try:
            app_form = form.find_element_by_css_selector('app-form')
            app_form_shadow = expand_shadow_root(context, app_form)
            input_containers += app_form_shadow.find_elements_by_css_selector('paper-input, paper-textarea')
            sub_forms = app_form_shadow.find_elements_by_css_selector('sub-form')
            for sub in sub_forms:
                sub_shadow = expand_shadow_root(context, sub)
                sub_app_form = sub_shadow.find_element_by_css_selector('app-form')
                sub_app_form_shadow = expand_shadow_root(context, sub_app_form)
                input_containers += sub_app_form_shadow.find_elements_by_css_selector('paper-input, paper-textarea')
        except NoSuchElementException:
            pass
    for container in input_containers:
        container_shadow = expand_shadow_root(context, container)
        text = safe_get_element_text(
            container_shadow.find_element_by_css_selector('label')).lower().strip().rstrip(' *')
        if text == input_name:
            if 'textarea' in container.tag_name:
                selector = 'textarea'
            else:
                selector = 'input'
            try:
                input_element = container_shadow.find_element_by_css_selector(selector)
            except NoSuchElementException:
                input_container_shadow = expand_shadow_root(context, container_shadow.find_element_by_css_selector('paper-input-container'))
                input_slot = input_container_shadow.find_element_by_css_selector('slot[name="input"]')
                for expanded_slot in expand_slot(context, input_slot):
                    expanded_slot_shadow = expand_shadow_root(context,  expanded_slot)
                    try:
                        input_element = expanded_slot_shadow.find_element_by_css_selector(selector)
                    except NoSuchElementException:
                        print(e)
                        import ipdb;ipdb.set_trace()
    return input_element


@step(u'I click the button "{button_name}" from the menu of the "{title}" '
      u'{form_type} form')
def click_menu_button_from_more_menu(context, button_name, title, form_type):
    from .buttons import clicketi_click
    from .buttons import click_button_from_collection
    form_type = form_type.lower()
    form = get_add_form(context, form_type) if form_type == 'add' else \
        get_edit_form(context, title)
    if title == 'machine':
        actions = context.browser.find_element_by_tag_name('mist-actions')
        buttons = actions.find_elements_by_tag_name('paper-button')
        for button in buttons:
            if safe_get_element_text(button).lower() == button_name.lower() and button.is_displayed():
                clicketi_click(context, button)
                return
        more_dropdown = actions.find_element_by_id('actionmenu')
        more_dropdown_button = actions.find_element_by_class_name('dropdown-trigger')
    else:
        more_dropdown = form.find_element_by_tag_name('paper-menu-button')
        more_dropdown_button = more_dropdown
    assert more_dropdown, "Could not find more button"
    clicketi_click(context, more_dropdown_button)
    more_dropdown_buttons = more_dropdown.find_elements_by_tag_name('paper-button')
    assert more_dropdown_buttons, "There are no buttons within the more dropdown"
    timeout = time() + 5
    while time() < timeout:
        displayed_buttons = 0
        for button in more_dropdown_buttons:
            if button.is_displayed():
                displayed_buttons += 1
        if displayed_buttons == len(more_dropdown_buttons):
            break
        sleep(1)
    else:
        assert False, "More dropdown buttons are not visible after 5 seconds"
    click_button_from_collection(context, button_name, more_dropdown_buttons)


def get_button_from_form(context, form, button_name, tag_name='paper-button:not([hidden])'):
    all_buttons = []
    form_containers = form.find_elements_by_css_selector('cloud-edit, network-create, mist-monitoring, mist-rules, team-policy, metric-menu')
    form_containers_shadow = [expand_shadow_root(context, f) for f in form_containers]
    form_containers_shadow.append(form)
    for form in form_containers_shadow:
        all_buttons += form.find_elements_by_css_selector('%s' % tag_name)
        try:
            sub_forms = form.find_elements_by_css_selector('app-form, add-graph, metric-menu')
            for sub_form in sub_forms:
                sub_form_shadow = expand_shadow_root(context, sub_form)
                all_buttons += sub_form_shadow.find_elements_by_css_selector('%s' % tag_name)
        except NoSuchElementException:
            pass
    assert all_buttons, "Could not find any buttons in the form"
    button = None
    for b in all_buttons:
        if safe_get_element_text(b).lower().strip() == button_name.lower():
            return b
    assert button, "Could not find button %s" % button_name


@step(u'I expect the field "{field_name}" in the {title} {form_type} form to'
      u' be visible within max {seconds} seconds')
def check_that_field_is_visible(context, field_name, title, form_type, seconds):
    field_name = field_name.lower()
    add_form = get_add_form(context, title) if form_type == 'add' else \
        get_edit_form(context, title)
    add_form_shadow = expand_shadow_root(context, add_form)
    form_input = None
    timeout = time() + int(seconds)
    while time() < timeout:
        form_input = get_input_element_from_form(context, add_form_shadow, field_name)
        if form_input.is_displayed():
            return True
        sleep(1)
    assert form_input, "Could not find field %s after %s seconds" % field_name
    assert False, "Field %s did not become visible after %s seconds" \
                  % (field_name, seconds)


use_step_matcher("re")
@step(u'I set the value "(?P<value>[A-Za-z0-9 \-/._#!>+:=\*\n~\\\\]+)" to field "(?P<name>[A-Za-z ]+)" in the "(?P<title>[A-Za-z]+)" (?P<form_type>[A-Za-z]+) form')
def set_value_to_field(context, value, name, title, form_type):
    if context.mist_config.get(value):
        value = context.mist_config.get(value)
    elif "random" in value:
        value_key = value
        value = value.replace("random", str(randrange(1000)))
        context.mist_config[value_key] = value
    form = get_add_form(context, title) if form_type == 'add' else \
        get_edit_form(context, title)
    form_shadow = expand_shadow_root(context, form)
    form_input = get_input_element_from_form(context, form_shadow, name.lower())
    assert form_input, "Could not set value to field %s" % name
    clear_input_and_send_keys(form_input, value)


use_step_matcher('parse')
@step(u'I expect for the button "{button_name}" in the "{title}" {form_type} form'
      u' to be clickable within {seconds} seconds')
def check_button_in_form_is_clickable(context, button_name, title, form_type,
                                      seconds):
    form = get_add_form(context, title) if form_type == 'add' else \
        get_edit_form(context, title)
    timeout = time() + int(seconds)
    form_shadow = expand_shadow_root(context, form)
    while time() < timeout:
        button = get_button_from_form(context, form_shadow, button_name.lower())
        if button.is_enabled() and button.get_attribute('disabled') == None:
            return True
        sleep(1)
    assert False, "Button %s did not become clickable" % button_name


@step(u'I focus on the button "{button_name}" in the "{title}" {form_type} form')
def focus_on_form_button(context, button_name, title, form_type):
    form = get_add_form(context, title) if form_type == 'add' else \
        get_edit_form(context, title)
    form_shadow = expand_shadow_root(context, form)
    button = get_button_from_form(context, form_shadow, button_name.lower())
    focus_on_element(context, button)
    sleep(.1)


use_step_matcher("re")
@step(u'I click the button "(?P<button_name>[A-Za-z ]+)" in the "(?P<title>[A-Za-z]+)" add form')
def click_button_in_form(context, button_name, title):
    form = get_add_form(context, title)
    form_shadow = expand_shadow_root(context, form)
    button = get_button_from_form(context, form_shadow, button_name.lower())
    from .buttons import clicketi_click
    clicketi_click(context, button)


@step(u'I click the button "(?P<button_name>[A-Za-z ]+)" in the "(?P<title>[A-Za-z]+)" page')
def click_button_in_resource_page(context, button_name, title):
    _, form = get_page_element(context, title + 's', title)
    form_shadow = expand_shadow_root(context, form)
    button = get_button_from_form(context, form_shadow, button_name.lower())
    from .buttons import clicketi_click
    clicketi_click(context, button)


use_step_matcher('parse')
def get_text_of_dropdown(el):
    try:
        return safe_get_element_text(
            el.find_element_by_css_selector('paper-input')).strip().lower()
    except NoSuchElementException:
        return ''


def get_current_value_of_dropdown(el):
    try:
        return el.find_element_by_id('labelAndInputContainer').\
            find_element_by_tag_name('input').\
            get_attribute('value').strip().lower()
    except:
        return ''


def find_dropdown(context, container, dropdown_text):
    dropdown_text = dropdown_text.lower().rstrip(' *')
    all_dropdowns = container.find_elements_by_css_selector('paper-dropdown-menu:not([hidden])')
    try:
        app_form = container.find_element_by_css_selector('app-form')
        app_form_shadow = expand_shadow_root(context, app_form)
        all_dropdowns += app_form_shadow.find_elements_by_css_selector('paper-dropdown-menu:not([hidden])')
        sub_forms = app_form_shadow.find_elements_by_css_selector('sub-form')
        for sub in sub_forms:
            sub_shadow = expand_shadow_root(context, sub)
            sub_app_form = sub_shadow.find_element_by_css_selector('app-form')
            sub_app_form_shadow = expand_shadow_root(context, sub_app_form)
            all_dropdowns += sub_app_form_shadow.find_elements_by_css_selector('paper-dropdown-menu:not([hidden])')
    except NoSuchElementException:
        pass
    for dropdown in all_dropdowns:
        if dropdown.get_attribute('label').lower().rstrip(' *') == dropdown_text:
            return dropdown
    assert False, 'There is no dropdown with text %s' % dropdown_text


@step(u'I open the "{dropdown_text}" dropdown in the "{resource_type}" add form')
def open_drop_down_in_add_form(context, dropdown_text, resource_type):
    from .buttons import clicketi_click
    page = get_add_form(context, resource_type)
    page_shadow = expand_shadow_root(context, page)
    dropdown = find_dropdown(context, page_shadow, dropdown_text.lower())
    clicketi_click(context, dropdown)


use_step_matcher("re")
@step(u'I click the "(?P<button_name>[A-Za-z ]+)" button in the "(?P<dialog_title>[A-Za-z]+)" dialog')
def click_button_in_dialog(context, button_name, dialog_title):
    from .buttons import clicketi_click
    from .dialog import get_dialog
    dialog = get_dialog(context, dialog_title)
    dialog_shadow = expand_shadow_root(context, dialog)
    button = get_button_from_form(context, dialog_shadow, button_name.lower(), tag_name='paper-button, paper-item')
    clicketi_click(context, button)


@step(u'I click the "(?P<button_name>[A-Za-z0-9_ ]+)" button in the "(?P<dropdown_title>[A-Za-z ]+)" dropdown in the "(?P<dialog_title>[A-Za-z ]+)" dialog')
def click_button_in_dropdown_in_dialog(context, button_name, dropdown_title, dialog_title):
    from .buttons import clicketi_click
    from .dialog import get_dialog
    dialog = get_dialog(context, dialog_title)
    dialog_shadow = expand_shadow_root(context, dialog)
    button = get_button_from_form(context, dialog_shadow, button_name.lower(), tag_name='paper-item')
    clicketi_click(context, button)


use_step_matcher('parse')
@step(u'I open the "{dropdown_text}" dropdown in the "{dialog_title}" dialog')
def open_drop_down_in_dialog(context, dropdown_text, dialog_title):
    from .buttons import clicketi_click
    from .dialog import get_dialog
    dialog = get_dialog(context, dialog_title)
    dialog_shadow = expand_shadow_root(context, dialog)
    dropdown = find_dropdown(context, dialog_shadow, dropdown_text.lower())
    clicketi_click(context, dropdown)
