from behave import step

from time import time
from time import sleep

from selenium.webdriver.common.by import By

from misttests.integration.gui.steps.utils import safe_get_element_text, expand_shadow_root, get_page_element

from misttests.integration.gui.steps.buttons import clicketi_click

from misttests.integration.gui.steps.forms import clear_input_and_send_keys
from misttests.integration.gui.steps.dialog import get_dialog


def get_tags_list(tags_dialog):
    return tags_dialog.find_elements(By.CSS_SELECTOR, 'tag-item')


def get_empty_tag(context, tags_dialog):
    tags_dialog_shadow = expand_shadow_root(context, tags_dialog)
    tags = get_tags_list(tags_dialog_shadow)
    for tag in tags:
        inputs = expand_shadow_root(context, tag).find_elements(By.CSS_SELECTOR, 'vaadin-combo-box')
        if not inputs[0].get_attribute('value').strip():
            return tag
    return None


def get_tag_with_key(context, tags_dialog, key):
    key = key.lower()
    tags_dialog_shadow = expand_shadow_root(context, tags_dialog)
    tags = get_tags_list(tags_dialog_shadow)
    for tag in tags:
        inputs = expand_shadow_root(context, tag).find_elements(By.CSS_SELECTOR, 'vaadin-combo-box.key')
        if inputs[0].get_attribute('value').strip().lower() == key:
            return tag
    return None


def set_key_and_value(context, tag, key, value):
    inputs = expand_shadow_root(context, tag).find_elements(By.CSS_SELECTOR, 'vaadin-combo-box')
    clear_input_and_send_keys(inputs[0], key)
    clear_input_and_send_keys(inputs[1], value)


def remove_tag(context, tag):
    clicketi_click(context, expand_shadow_root(context, tag).find_element(By.CSS_SELECTOR, 'paper-icon-button'))


@step('I remove all the previous tags')
def delete_previous_tags(context):
    for tag in get_tags_list(get_dialog(context, "Tags")):
        remove_tag(context, tag)


@step('I add a tag with key "{key}" and value "{value}"')
def add_a_new_tag(context, key, value):
    tags_dialog = get_dialog(context, "Tags")
    tag = get_empty_tag(context, tags_dialog)
    if not tag:
        context.execute_steps('When I click the "Add Tag" button in the "Tags" dialog')
        tag = get_empty_tag(context, tags_dialog)
    set_key_and_value(context, tag, key, value)


@step('I remove the tag with key "{key}"')
def close_some_tag(context, key):
    tags_dialog = get_dialog(context, "Tags")
    tag = get_tag_with_key(context, tags_dialog, key)
    remove_tag(context, tag)


@step('I ensure that the "{type_of_item}" has the tags "{tags}" within {seconds} seconds')
def ensure_tags_are_present(context, type_of_item, tags, seconds):
    from misttests.integration.gui.steps.forms import get_edit_form
    #form = get_edit_form(context, type_of_item)
    _, key_page = get_page_element(context, type_of_item + 's', type_of_item)
    key_page_shadow = expand_shadow_root(context, key_page)
    end_time = time() + int(seconds)
    while time() < end_time:
        existing_tags = key_page_shadow.find_elements(By.CSS_SELECTOR, '.tag')
        expected_tags = dict([(t.split(':')[0], t.split(':')[1]) for t in tags.strip().lower().split(',')])
        for existing_tag in existing_tags:
            key = safe_get_element_text(existing_tag).lower().split('=')[0].strip()
            if key.endswith('\n'):
                key = key[:-1]
            if key in expected_tags:
                del expected_tags[key]
            if len(expected_tags) == 0:
                return
            sleep(2)
    assert len(expected_tags) == 0, "These keys are not available: %s" % list(expected_tags.keys())
