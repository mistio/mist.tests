from behave import step

from time import time
from time import sleep

from .utils import safe_get_element_text

from .buttons import clicketi_click

from .forms import clear_input_and_send_keys


def get_tag_modal(context):
    return context.browser.find_element_by_css_selector('paper-dialog#tagsModal')


def get_tags_list(tag_modal):
    return tag_modal.find_elements_by_tag_name('tag-item')


def get_empty_tag(tag_modal):
    tags = get_tags_list(tag_modal)
    for tag in tags:
        inputs = tag.find_elements_by_id('input')
        if not inputs[0].get_attribute('value').strip():
            return tag
    return None


def get_tag_with_key(tag_modal, key):
    key = key.lower()
    tags = get_tags_list(tag_modal)
    for tag in tags:
        inputs = tag.find_elements_by_id('input')
        if inputs[0].get_attribute('value').strip().lower() == key:
            return tag
    return None


def set_key_and_value(tag, key, value):
    inputs = tag.find_elements_by_id('input')
    clear_input_and_send_keys(inputs[0], key)
    clear_input_and_send_keys(inputs[1], value)


def close_tag(context, tag):
    clicketi_click(context, tag.find_element_by_tag_name('paper-icon-button'))


@step(u'I remove all the previous tags')
def delete_previous_tags(context):
    for tag in get_tags_list(get_tag_modal(context)):
        close_tag(context, tag)


@step(u'I add a tag with key "{key}" and value "{value}"')
def add_a_new_tag(context, key, value):
    tag_modal = get_tag_modal(context)
    tag = get_empty_tag(tag_modal)
    if not tag:
        context.execute_steps(u'When I click the button "Add Tag" in the tag menu')
        tag = get_empty_tag(tag_modal)
    set_key_and_value(tag, key, value)


@step(u'I remove the tag with key "{key}"')
def close_some_tag(context, key):
    tag_modal = get_tag_modal(context)
    tag = get_tag_with_key(tag_modal, key)
    close_tag(context, tag)


@step(u'I expect for the tag popup to {action} within {seconds} seconds')
def wait_for_tag_dialog(context, action, seconds):
    action = action.lower()
    if action not in ['open', 'close']:
        raise Exception('Unknown action')
    timeout = time() + int(seconds)
    while time() < timeout:
        tag_modal = get_tag_modal(context)
        if action == 'open' and tag_modal.is_displayed():
            return True
        if action == 'close' and not tag_modal.is_displayed():
            return True
        sleep(1)
    assert False, "Tag menu did not become %s after %s seconds" \
                  % (action, seconds)


@step(u'I ensure that the "{type_of_item}" has the tags "{tags}"')
def ensure_tags_are_present(context, type_of_item, tags):
    from .forms import get_edit_form
    form = get_edit_form(context, type_of_item)
    existing_tags = form.find_elements_by_class_name('tag')
    expected_tags = dict(map(lambda t: (t.split(':')[0], t.split(':')[1]), tags.strip().lower().split(',')))
    for existing_tag in existing_tags:
        key = safe_get_element_text(existing_tag).lower().strip().split('=')[0]
        if key in expected_tags:
            del expected_tags[key]
    assert len(expected_tags) == 0, "These keys are not available: %s" % expected_tags.keys()


