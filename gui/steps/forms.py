from behave import step

from .utils import focus_on_element
from .utils import safe_get_element_text

from selenium.common.exceptions import NoSuchElementException

from time import time
from time import sleep


def clear_input_and_send_keys(input_field, text):
    while input_field.get_attribute('value') != '':
        input_field.send_keys(u'\ue003')
    current_expected_value = ''
    n = 20
    chunks = [text[i:i+n] for i in xrange(0, len(text), n)]
    for chunk in chunks:
        current_expected_value += chunk
        input_field.send_keys(chunk)
        for _ in range(2):
            if input_field.get_attribute('value') != current_expected_value:
                sleep(1)
            else:
                break
        else:
            raise Exception('Sending keys to form unsuccessful')


def get_add_form(context, title):
    title = title.lower()
    if title not in ['cloud', 'machine', 'image', 'key', 'network', 'tunnel',
                     'script', 'template', 'stack', 'team', 'members']:
        raise ValueError('The title given is unknown')
    add_form_selector = 'div#content.%s-add' % title
    return context.browser.find_element_by_css_selector(add_form_selector)


def get_edit_form(context, title):
    title = title.lower()
    if title == 'cloud':
        raise Exception
    if title not in ['machine', 'image', 'key', 'network', 'tunnel', 'script',
                     'template', 'stack', 'team', 'policy']:
        raise Exception('The title given is unknown')
    try:
        if title == 'policy':
            return context.browser.find_element_by_tag_name('team-policy')
        return context.browser.find_element_by_tag_name('%s-page' % title)
    except:
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
            if form and form.is_displayed():
                return True
        except NoSuchElementException:
            pass
        sleep(1)
    assert False, msg


def get_input_from_form(form, input_name):
    input_containers = form.find_elements_by_id('labelAndInputContainer')
    for container in input_containers:
        text = safe_get_element_text(
            container.find_element_by_tag_name('label')).lower().strip()
        if text.endswith(' *'):
            text = text[:-2]
        if text == input_name:
            input = container.find_element_by_id('input')
            if 'textarea' in input.get_attribute('class'):
                input = container.find_element_by_id('textarea')
            return input


def get_button_from_form(form, button_name):
    if button_name == 'add a new rule':
        return form.find_element_by_css_selector('div.rules span.team-policy')
    buttons = form.find_elements_by_tag_name('paper-button')
    assert buttons, "Could not find any buttons in the form"
    button = None
    for b in buttons:
        if safe_get_element_text(b).lower().strip() == button_name:
            return b
    assert button, "Could not find button %s" % button_name


@step(u'I expect the field "{field_name}" in the {title} {form_type} form to'
      u' be visible within max {seconds} seconds')
def check_that_field_is_visible(context, field_name, title, form_type, seconds):
    field_name = field_name.lower()
    add_form = get_add_form(context, title) if form_type == 'add' else \
        get_edit_form(context, title)
    input = None
    timeout = time() + int(seconds)
    while time() < timeout:
        input = get_input_from_form(add_form, field_name)
        if input.is_displayed():
            return True
        sleep(1)
    assert input, "Could not find field %s after %s seconds" % field_name
    assert False, "Field %s did not become visible after %s seconds" \
                  % (field_name, seconds)


@step(u'I set the value "{value}" to field "{name}" in "{title}" {form_type}'
      u' form')
def set_value_to_field(context, value, name, title, form_type):
    if context.mist_config.get(value):
        value = context.mist_config.get(value)
    form = get_add_form(context, title) if form_type == 'add' else \
        get_edit_form(context, title)
    input = get_input_from_form(form, name.lower())
    assert input, "Could not set value to field %s" % name
    clear_input_and_send_keys(input, value)


@step(u'I expect for the button "{button_name}" in "{title}" {form_type} form'
      u' to be clickable within {seconds} seconds')
def check_button_in_form_is_clickable(context, button_name, title, form_type,
                                      seconds):
    add_form = get_add_form(context, title) if form_type == 'add' else \
        get_edit_form(context, title)
    timeout = time() + int(seconds)
    while time() < timeout:
        button = get_button_from_form(add_form, button_name.lower())
        if button.is_enabled():
            return True
        sleep(1)
    assert False, "Button %s did not become clickable" % button_name


@step(u'I focus on the button "{button_name}" in "{title}" {form_type} form')
def focus_on_form_button(context, button_name, title, form_type):
    form = get_add_form(context, title) if form_type == 'add' else \
        get_edit_form(context, title)
    button = get_button_from_form(form, button_name.lower())
    focus_on_element(context, button)


@step(u'I click the button "{button_name}" in "{title}" {form_type} form')
def click_button_in_form(context, button_name, title, form_type):
    form = get_add_form(context, title) if form_type == 'add' else \
        get_edit_form(context, title)
    button = get_button_from_form(form, button_name.lower())
    from .buttons import clicketi_click
    clicketi_click(context, button)


def get_text_of_dropdown(el):
    try:
        return safe_get_element_text(
            el.find_element_by_class_name('paper-input')).strip().lower()
    except NoSuchElementException:
        return ''


def get_current_value_of_dropdown(el):
    try:
        return el.find_element_by_id('labelAndInputContainer').\
            find_element_by_tag_name('input').\
            get_attribute('value').strip().lower()
    except:
        return ''


def find_dropdown(context, dropdown_text):
    # get all the paper materials
    dropdown_text = dropdown_text.lower()
    if dropdown_text.endswith(' *'):
        dropdown_text = dropdown_text[:-2]
    all_dropdowns = context.browser.find_elements_by_tag_name('paper-dropdown-menu')
    all_dropdowns = filter(lambda t: t[0],
                           map(lambda el: (get_text_of_dropdown(el).strip().lower(), el),
                               all_dropdowns))
    # find the drop down with the text
    dropdown = filter(lambda t: t[0] == dropdown_text or t[0][:-2] == dropdown_text,
                      all_dropdowns)
    assert dropdown, 'There is no dropdown with text %s' % dropdown_text
    return dropdown.pop()[1]


@step(u'I open the "{dropdown_text}" drop down')
def open_drop_down(context, dropdown_text):
    from .buttons import clicketi_click
    dropdown = find_dropdown(context, dropdown_text.lower())
    clicketi_click(context, dropdown)


@step(u'I click the button "{button_name}" from the menu of the "{title}" '
      u'{form_type} form')
def click_menu_button_from_more_menu(context, button_name, title, form_type):
    from .buttons import clicketi_click
    from .buttons import click_button_from_collection
    form_type = form_type.lower()
    form = get_add_form(context, form_type) if form_type == 'add' else \
        get_edit_form(context, title)
    more_dropdown = form.find_element_by_tag_name('paper-menu-button')
    assert more_dropdown, "Could not find more button"
    clicketi_click(context, more_dropdown)
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
