from behave import step

from .utils import safe_get_element_text


@step(u'I rename my script with "{name}" name')
def rename_script(context, name):
    script_name_holder = context.browser.find_element_by_id("script-edit")
    script_name_field = script_name_holder.find_element_by_id("script-edit-new-name")
    script_name_field.clear()
    script_name_field.send_keys(name)


@step(u'I write "{text}" in the script textfield')
def fill_script(context, text):
    script_textarea_holder = context.browser.find_element_by_id("add-script")
    script_textarea = script_textarea_holder.find_element_by_id("url-script-script")
    script_textarea.clear()
    script_textarea.send_keys('#!/bin/bash'+u'\ue007'+text)


@step(u'I should see a script called "{scriptname}"')
def check_if_script_is_listed(context, scriptname):
    scriptname = scriptname.lower()
    listed_scripts = context.browser.find_elements_by_class_name('checkbox-link')
    for script in listed_scripts:
        if safe_get_element_text(script.find_element_by_class_name('script-name')).lower() == scriptname:
            return
    assert False, "No script named %s is available" % scriptname


@step(u'there should be no script called "{scriptname}"')
def check_if_script_is_listed(context, scriptname):
    scriptname = scriptname.lower()
    listed_scripts = context.browser.find_elements_by_class_name('checkbox-link')
    for script in listed_scripts:
        assert not safe_get_element_text(script.find_element_by_class_name(
            'script-name')).lower() == scriptname, "Script %s has not been deleted" % scriptname


@step(u'I delete script "{scriptname}" script if it exists')
def delete_script_if_there(context, scriptname):
    scriptname = scriptname.lower()
    listed_scripts = context.browser.find_elements_by_class_name('checkbox-link')
    for script in listed_scripts:
        if safe_get_element_text(script.find_element_by_class_name('script-name')).lower() == scriptname:
            checkbox = script.find_element_by_class_name("ui-checkbox")
            checkbox.click()
            context.execute_steps(u'''
                Then I click the button "Delete"
                And I expect for "dialog-popup" popup to appear within max 4 seconds
                When I click the "Yes" button inside the "Delete Scripts" popup
                Then I expect for "dialog-popup" popup to disappear within max 4 seconds
            ''')
            break
