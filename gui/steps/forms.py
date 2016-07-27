from behave import step

from .utils import focus_on_element
from .utils import safe_get_element_text

from selenium.common.exceptions import NoSuchElementException

from time import time
from time import sleep


def clear_input_and_send_keys(input_field, text):
    end_time = time() + 5
    while time() < end_time:
        while input_field.get_attribute('value') != '':
            input_field.send_keys(u'\ue003')
        if text == '':
            break
        input_field.send_keys(text)
        if input_field.get_attribute('value') != text:
            assert time() + 1 > end_time, "Could not input value %s" % text
            sleep(1)
        else:
            break


def get_add_form(context, title):
    title = title.lower()
    if title not in ['cloud', 'machine', 'image', 'key', 'network', 'tunnel',
                     'script', 'template', 'stack', 'team']:
        raise ValueError('The title given is unknown')
    add_form_selector = 'div#content.%s-add' % title
    return context.browser.find_element_by_css_selector(add_form_selector)


def get_edit_form(context, title):
    title = title.lower()
    if title == 'cloud':
        raise Exception
    if title not in ['machine', 'image', 'key', 'network', 'tunnel', 'script',
                     'template', 'stack', 'team']:
        raise Exception('The title given is unknown')
    try:
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
            if form.is_displayed():
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
        if text == input_name:
            return container.find_element_by_id('input')


def get_button_from_form(form, button_name):
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
    if input:
        clear_input_and_send_keys(input, value)
    else:
        assert False, "Could not set value to field %s" % name


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


def find_dropdown(context, dropdown_text):
    # get all the paper materials
    all_dropdowns = context.browser.find_elements_by_tag_name(
        'paper-dropdown-menu')
    # find the drop down with the text
    dropdown = filter(lambda el: get_text_of_dropdown(el) == dropdown_text,
                      all_dropdowns)
    if not dropdown:
        raise NoSuchElementException('There is no dropdown with text %s'
                                     % dropdown_text)
    return dropdown.pop()


@step(u'I open the "{dropdown_text}" drop down')
def open_drop_down(context, dropdown_text):
    from .buttons import clicketi_click
    dropdown = find_dropdown(context, dropdown_text.lower())
    clicketi_click(context, dropdown)
