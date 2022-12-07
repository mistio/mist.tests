from behave import step, use_step_matcher

from misttests.integration.gui.steps.utils import focus_on_element, get_page_element, clear_input_and_send_keys, get_page
from misttests.integration.gui.steps.utils import safe_get_element_text, expand_shadow_root, expand_slot

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from time import time
from time import sleep

from random import randrange


def get_add_form(context, title):
    title = title.lower()
    if title not in ['cloud', 'machine', 'image', 'key', 'network', 'tunnel',
                     'script', 'schedule', 'template', 'stack', 'team',
                     'members', 'zone', 'record', 'volume']:
        raise ValueError('The title given is unknown {}'.format(title))
    if title == 'members':
        page_element = get_page_element(context, 'teams')
    elif title == 'record':
        _, page_element = get_page_element(context, 'zones', 'zone')
    else:
        page_element = get_page_element(context, title + 's')
    page_shadow = expand_shadow_root(context, page_element)
    if title in ['stack', 'machine', 'network', 'record', 'volume']:
        add_form_selector = '%s-create' % title
    else:
        add_form_selector = '%s-add' % title
    return page_shadow.find_element(By.CSS_SELECTOR, add_form_selector)


def get_edit_form(context, title):
    title = title.lower()
    if title not in ['machine', 'image', 'key', 'network', 'tunnel', 'script',
                     'template', 'stack', 'team', 'policy', 'cloud', 'schedule', 'zone']:
        raise Exception('The title given is unknown')
    try:
        if title == 'policy':
            page_teams_element = get_page_element(context, 'teams')
            page_teams_shadow = expand_shadow_root(context, page_teams_element)
            return expand_shadow_root(context, page_teams_shadow.find_element(By.CSS_SELECTOR, 'team-page'))
            # return context.browser.find_element(By.CSS_SELECTOR, 'team-policy')
        page_shadow = expand_shadow_root(context, get_page_element(context, title + 's'))
        return page_shadow
    except NoSuchElementException:
        return None


@step('I expect the "{page}" {form_type} form to be visible within max '
      '{seconds} seconds')
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
    input_containers = form.find_elements(By.CSS_SELECTOR, 'paper-input, paper-textarea')
    form_containers = form.find_elements(By.CSS_SELECTOR, 'cloud-edit, cloud-dns')
    form_containers_shadow = [expand_shadow_root(context, f) for f in form_containers]
    form_containers_shadow.append(form)
    for form in form_containers_shadow:
        try:
            app_form = form.find_element(By.CSS_SELECTOR, 'app-form, multi-inputs')
            app_form_shadow = expand_shadow_root(context, app_form)
            input_containers += app_form_shadow.find_elements(By.CSS_SELECTOR, 'paper-input, paper-textarea')
            sub_forms = app_form_shadow.find_elements(By.CSS_SELECTOR, 'sub-form, multi-inputs')
            for sub in sub_forms:
                sub_shadow = expand_shadow_root(context, sub)
                sub_app_form = sub_shadow.find_element(By.CSS_SELECTOR, 'app-form')
                sub_app_form_shadow = expand_shadow_root(context, sub_app_form)
                input_containers += sub_app_form_shadow.find_elements(By.CSS_SELECTOR, 'paper-input, paper-textarea')
        except NoSuchElementException:
            pass
    for container in input_containers:
        container_shadow = expand_shadow_root(context, container)
        text = safe_get_element_text(
            container_shadow.find_element(By.CSS_SELECTOR, 'label')).lower().strip().rstrip(' *')
        if input_name in text:
            if 'textarea' in container.tag_name:
                selector = 'textarea'
            else:
                selector = 'input'
            try:
                input_element = container_shadow.find_element(By.CSS_SELECTOR, selector)
            except NoSuchElementException:
                input_container_shadow = expand_shadow_root(context, container_shadow.find_element(By.CSS_SELECTOR, 'paper-input-container'))
                input_slot = input_container_shadow.find_element(By.CSS_SELECTOR, 'slot[name="input"]')
                for expanded_slot in expand_slot(context, input_slot):
                    expanded_slot_shadow = expand_shadow_root(context,  expanded_slot)
                    try:
                        input_element = expanded_slot_shadow.find_element(By.CSS_SELECTOR, selector)
                    except NoSuchElementException:
                        print(e)
            if input_element and input_name == text:
                break
    return input_element


def get_button_from_form(context, form, button_name, tag_name='paper-button:not([hidden])'):
    all_buttons = []
    form_containers = form.find_elements(By.CSS_SELECTOR, 'cloud-edit, cloud-dns, network-create, mist-monitoring, mist-rules, team-policy, metric-menu, rule-metrics')
    form_containers_shadow = [expand_shadow_root(context, f) for f in form_containers]
    form_containers_shadow.append(form)
    for form in form_containers_shadow:
        all_buttons += form.find_elements(By.CSS_SELECTOR, '%s' % tag_name)
        try:
            sub_forms = form.find_elements(By.CSS_SELECTOR, 'app-form, add-graph, metric-menu, rule-metrics')
            for sub_form in sub_forms:
                sub_form_shadow = expand_shadow_root(context, sub_form)
                all_buttons += sub_form_shadow.find_elements(By.CSS_SELECTOR, '%s' % tag_name)
                sub_fieldgroups = sub_form_shadow.find_elements(By.CSS_SELECTOR, 'sub-fieldgroup')
                for sub_fieldgroup in sub_fieldgroups:
                    sub_field_shadow = expand_shadow_root(context, sub_fieldgroup)
                    all_buttons += sub_field_shadow.find_elements(By.CSS_SELECTOR, '%s' % tag_name)
        except NoSuchElementException:
            pass
    assert all_buttons, "Could not find any buttons in the form"
    button = None
    for b in all_buttons:
        if safe_get_element_text(b).lower().strip() == button_name.lower():
            return b
    assert button, "Could not find button %s" % button_name


@step('I expect the field "{field_name}" in the {title} {form_type} form to'
      ' be visible within max {seconds} seconds')
def check_that_field_is_visible(context, field_name, title, form_type, seconds):
    field_name = field_name.lower()
    add_form = get_add_form(context, title) if form_type == 'add' else \
        get_edit_form(context, title)
    add_form_shadow = expand_shadow_root(context, add_form)
    form_input = None
    timeout = time() + int(seconds)
    while time() < timeout:
        form_input = get_input_element_from_form(context, add_form_shadow, field_name)
        if form_input and form_input.is_displayed():
            return True
        sleep(1)
    assert form_input, "Could not find field %s after %s seconds" % (
        field_name, seconds)


use_step_matcher("re")
@step('I set the "(?P<script_input>[A-Za-z ]+)" script "(?P<script>[A-Za-z0-9 \-/,._#!<>+:=\{\}@%\*\"\n~\\\\\[\]]+)"')
def set_script_to_field(context, script_input, script):
    form = get_add_form(context, 'machine')
    form_shadow = expand_shadow_root(context, form)
    form_input = get_input_element_from_form(context, form_shadow, script_input.lower())
    n = 70
    script.replace('\"', '"')
    chunks = [script[i:i+n] for i in range(0, len(script), n)]
    for chunk in chunks:
        if '\\n' in chunk:
            _chunks = chunk.split('\\n')
            for _chunk in _chunks:
                form_input.send_keys(_chunk)
                from selenium.webdriver.common.keys import Keys
                if _chunk not in _chunks[-1]:
                    form_input.send_keys(Keys.RETURN)
        else:
            form_input.send_keys(chunk)


use_step_matcher("re")
@step('I set the value "(?P<value>[A-Za-z0-9 \-\/,._#!<>+:=\{\}@%\*\"\n~\\\(\]]+)" to field "(?P<name>[A-Za-z _]+)" in the "(?P<title>[A-Za-z]+)" (?P<form_type>[A-Za-z]+) form')
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
    if name == 'Script':
        app_form = form_shadow.find_element(By.CSS_SELECTOR, 'app-form, multi-inputs')
        app_form_shadow = expand_shadow_root(context, app_form)
        code_viewer = app_form_shadow.find_elements(By.CSS_SELECTOR, 'code-viewer')[0]
        code_viewer_shadow = expand_shadow_root(context, code_viewer)
        monaco_element = code_viewer_shadow.find_element(By.CSS_SELECTOR, 'monaco-element')
        monaco_element_shadow = expand_shadow_root(context, monaco_element)
        context.browser.switch_to.frame(monaco_element_shadow.find_element(By.CSS_SELECTOR, '#iframe'))
        text_area = context.browser.find_element(By.CSS_SELECTOR, 'textarea')
        text_area.send_keys(Keys.CONTROL + 'a')
        text_area.send_keys(Keys.DELETE)
        clear_input_and_send_keys(text_area, value)
        text = text_area.get_attribute('value')
        assert text == value, 'Inserted {} instead of {} after all'.format(text, value)
        context.browser.switch_to.default_content()
        return
    form_input = get_input_element_from_form(context, form_shadow, name.lower())
    if not form_input:
        app_form = form_shadow.find_element(By.CSS_SELECTOR, 'app-form, multi-inputs')
        app_form_shadow = expand_shadow_root(context, app_form)
        form_checkboxes = app_form_shadow.find_elements(By.CSS_SELECTOR, 'paper-checkbox[name="%s"]' % name.lower())
        assert len(form_checkboxes), "Could not set value to field %s" % name
        from misttests.integration.gui.steps.buttons import click_button_from_collection
        click_button_from_collection(context, value, form_checkboxes)
    else:
        clear_input_and_send_keys(form_input, value)


@step('I set the value "(?P<value>[A-Za-z0-9 \-\/,._#!<>+:=\{\}@%\*\"\n~\\\(\]]+)" to field "(?P<name>[A-Za-z ]+)" in the Account page')
def set_value_to_field_in_account_page(context, value, name):
    if context.mist_config.get(value):
        value = context.mist_config.get(value)
    elif "random" in value:
        value_key = value
        value = value.replace("random", str(randrange(1000)))
        context.mist_config[value_key] = value
    page_element = get_page_element(context, 'my-account')
    page_shadow = expand_shadow_root(context, page_element)
    active_section = page_shadow.find_element(By.CSS_SELECTOR, 'iron-pages > .iron-selected')
    section_shadow = expand_shadow_root(context, active_section)
    form_input = get_input_element_from_form(context, section_shadow, name.lower())
    assert form_input, "Could not set value to field %s" % name
    clear_input_and_send_keys(form_input, value)


use_step_matcher('parse')
@step('I expect for the button "{button_name}" in the "{title}" {form_type} form'
      ' to be clickable within {seconds} seconds')
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


@step('I focus on the button "{button_name}" in the "{title}" {form_type} form')
def focus_on_form_button(context, button_name, title, form_type):
    form = get_add_form(context, title) if form_type == 'add' else \
        get_edit_form(context, title)
    form_shadow = expand_shadow_root(context, form)
    button = get_button_from_form(context, form_shadow, button_name.lower())
    focus_on_element(context, button)
    sleep(.1)


use_step_matcher("re")
@step('I click the button "(?P<button_name>[A-Za-z _]+)" in the "(?P<title>[A-Za-z]+)" add form')
def click_button_in_form(context, button_name, title):
    form = get_add_form(context, title)
    form_shadow = expand_shadow_root(context, form)
    button = get_button_from_form(context, form_shadow, button_name.lower())
    from misttests.integration.gui.steps.buttons import clicketi_click
    clicketi_click(context, button)


@step('I click the button "(?P<button_name>[A-Za-z ]+)" in the "(?P<title>[A-Za-z]+)" page')
def click_button_in_resource_page(context, button_name, title):
    form = get_page(context, title)
    form_shadow = expand_shadow_root(context, form)
    button = get_button_from_form(context, form_shadow, button_name.lower())
    from misttests.integration.gui.steps.buttons import clicketi_click
    clicketi_click(context, button)


use_step_matcher('parse')
def get_text_of_dropdown(el):
    try:
        return safe_get_element_text(
            el.find_element(By.CSS_SELECTOR, 'paper-input')).strip().lower()
    except NoSuchElementException:
        return ''


def get_current_value_of_dropdown(el):
    try:
        return el.find_element(By.CSS_SELECTOR, '#labelAndInputContainer').\
            find_element(By.CSS_SELECTOR, 'input').\
            get_attribute('value').strip().lower()
    except:
        return ''


def find_dropdown(context, container, dropdown_text):
    dropdown_text = dropdown_text.lower().rstrip(' *')
    all_dropdowns = container.find_elements(By.CSS_SELECTOR, 'paper-dropdown-menu:not([hidden])')
    try:
        app_form = container.find_element(By.CSS_SELECTOR, 'app-form')
        app_form_shadow = expand_shadow_root(context, app_form)
        all_dropdowns += app_form_shadow.find_elements(By.CSS_SELECTOR, 'paper-dropdown-menu:not([hidden])')
        try:
            size = app_form_shadow.find_element(By.CSS_SELECTOR, '#app-form-createForm-size')
            shadow = expand_shadow_root(context, size)
            size_dropdown = shadow.find_element(By.CSS_SELECTOR, 'paper-dropdown-menu:not([hidden])')
            all_dropdowns.append(size_dropdown)
        except NoSuchElementException:
            pass
        sub_forms = app_form_shadow.find_elements(By.CSS_SELECTOR, 'sub-form')
        for sub in sub_forms:
            sub_shadow = expand_shadow_root(context, sub)
            sub_app_form = sub_shadow.find_element(By.CSS_SELECTOR, 'app-form')
            sub_app_form_shadow = expand_shadow_root(context, sub_app_form)
            all_dropdowns += sub_app_form_shadow.find_elements(By.CSS_SELECTOR, 'paper-dropdown-menu:not([hidden])')
    except NoSuchElementException:
        pass
    for dropdown in all_dropdowns:
        if dropdown.get_attribute('label').lower().rstrip(' *') == dropdown_text:
            return dropdown
    assert False, 'There is no dropdown with text %s' % dropdown_text


@step('I open the "{dropdown_text}" dropdown in the "{resource_type}" add form')
def open_drop_down_in_add_form(context, dropdown_text, resource_type):
    from misttests.integration.gui.steps.buttons import clicketi_click
    page = get_add_form(context, resource_type)
    page_shadow = expand_shadow_root(context, page)
    dropdown = find_dropdown(context, page_shadow, dropdown_text.lower())
    clicketi_click(context, dropdown)


use_step_matcher("re")
@step('I click the "(?P<button_name>[A-Za-z ]+)" button in the "(?P<dialog_title>[A-Za-z? ]+)" dialog')
def click_button_in_dialog(context, button_name, dialog_title):
    from misttests.integration.gui.steps.buttons import clicketi_click
    from misttests.integration.gui.steps.dialog import get_dialog
    dialog = get_dialog(context, dialog_title)
    dialog_shadow = expand_shadow_root(context, dialog)
    button = get_button_from_form(context, dialog_shadow, button_name.lower(), tag_name='paper-button:not([hidden]), paper-item:not([hidden])')
    clicketi_click(context, button)


@step('I click the "(?P<button_name>[A-Za-z0-9_ ]+)" button in the "(?P<dropdown_title>[A-Za-z ]+)" dropdown in the "(?P<dialog_title>[A-Za-z ]+)" dialog')
def click_button_in_dropdown_in_dialog(context, button_name, dropdown_title, dialog_title):
    from misttests.integration.gui.steps.buttons import clicketi_click
    from misttests.integration.gui.steps.dialog import get_dialog
    if context.mist_config.get(button_name):
        button_name = context.mist_config.get(button_name)
    dialog = get_dialog(context, dialog_title)
    dialog_shadow = expand_shadow_root(context, dialog)
    button = get_button_from_form(context, dialog_shadow, button_name.lower(), tag_name='paper-item')
    clicketi_click(context, button)


use_step_matcher('parse')
@step('I open the "{dropdown_text}" dropdown in the "{dialog_title}" dialog')
def open_drop_down_in_dialog(context, dropdown_text, dialog_title):
    from misttests.integration.gui.steps.buttons import clicketi_click
    from misttests.integration.gui.steps.dialog import get_dialog
    dialog = get_dialog(context, dialog_title)
    dialog_shadow = expand_shadow_root(context, dialog)
    dropdown = find_dropdown(context, dialog_shadow, dropdown_text.lower())
    clicketi_click(context, dropdown)

@step('I expect the "{dropdown_text}" dropdown to be absent in the "{resource_type}" add form')
def dropdown_is_absent(context, dropdown_text, resource_type):
    page = get_add_form(context, resource_type)
    page_shadow = expand_shadow_root(context, page)
    try:
        dropdown = find_dropdown(context, page_shadow, dropdown_text.lower())
    except AssertionError:
        # no dropdown found, it is what we wanted
        return
    if dropdown:
        assert False, "A dropdown was found with text: {}".format(dropdown.get_attribute('label'))

@step('I expect the "{slider_name}" slider of the size field to be absent in the "{resource_type}" add form')
def field_is_absent(context, slider_name, resource_type):
    page = get_add_form(context, resource_type)
    page_shadow = expand_shadow_root(context, page)
    form = page_shadow.find_element(By.CSS_SELECTOR, 'app-form')
    form_shadow = expand_shadow_root(context, form)
    size_field = form_shadow.find_element(By.CSS_SELECTOR, 'mist-size-field')
    size_field_shadow = expand_shadow_root(context, size_field)
    all_labels = size_field_shadow.find_elements(By.CSS_SELECTOR, '.label')
    for label in all_labels:
        if safe_get_element_text(label) == slider_name:
            assert False, "A slider was found with {} name in the size field!!!".format(slider_name)
