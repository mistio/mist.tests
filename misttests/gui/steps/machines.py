from behave import step
from behave import given

from time import time
from time import sleep

from random import randrange

from .utils import safe_get_element_text

from .buttons import clicketi_click
from .buttons import click_button_from_collection

# from .tags import check_the_tags

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver import ActionChains

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


comparisons = {"==": lambda x, y: x == y,
               ">": lambda x, y: x > y,
               "<": lambda x, y: x < y,
               ">=": lambda x, y: x >= y,
               "<=": lambda x, y: x <= y,
               "!=": lambda x, y: x != y,
               }

machine_states_ordering = {
    'error': 6,
    'pending': 5,
    'rebooting': 4,
    'running': 3,
    'unknown': 2,
    'suspended': 2,
    'terminated': 1,
    'undefined': 1,
    'stopped': 0
}

# this dict contains image, size and location to be tested for each provider
machine_values_dict = {
    "aws": ["Ubuntu Server 16.04 Beta2 (PV)", "m1.small - Small Instance", "ap-northeast-1a "],
    "digital ocean": ["CentOS 5.11 x32", "512mb", "Amsterdam 2"],
    "packet": ["Ubuntu 14.04 LTS", "Type 0 - 8GB RAM", "Amsterdam, NL"],
    "openstack": ["CoreOS", "m1.tiny", "0"],
    "rackspace": ["Ubuntu 14.04 LTS (Trusty Tahr) (PV)", "512MB Standard Instance", "0"],
    "nephoscale": ["Ubuntu Server 14.04 LTS 64-bit", "CS05 - Cloud Server 0.5 GB RAM, 1 Core", "SJC-1"],
    "softlayer": ["Ubuntu - Latest (64 bit) ", "1 CPU, 1GB ram, 25GB ", "AMS01 - Amsterdam"],
    "azure": ["Ubuntu Server 14.04 LTS", "ExtraSmall (1 cores, 768 MB) ", "West Europe"],
    "docker": ["Ubuntu 14.04"]
}


def set_values_to_create_machine_form(context,provider,machine_name):
    context.execute_steps(u'''
                Then I set the value "%s" to field "Machine Name" in "machine" add form
                When I open the "Image" drop down
                And I click the button "%s" in the "Image" dropdown
                When I open the "Key" drop down
                And I click the button "TestKey " in the "Key" dropdown
            ''' % (machine_name,
                   machine_values_dict.get(provider)[0]))


# def set_values_to_create_machine_form(context,provider,machine_name):
#     context.execute_steps(u'''
#                 Then I set the value "%s" to field "Machine Name" in "machine" add form
#                 When I open the "Image" drop down
#                 And I click the button "%s" in the "Image" dropdown
#                 When I open the "Size" drop down
#                 And I click the button "%s" in the "Size" dropdown
#                 When I open the "Location" drop down
#                 And I click the button "%s" in the "Location" dropdown
#                 When I open the "Key" drop down
#                 And I click the button "TestKey " in the "Key" dropdown
#             ''' % (machine_name,
#                    machine_values_dict.get(provider)[0],
#                    machine_values_dict.get(provider)[1],
#                    machine_values_dict.get(provider)[2]))


@step(u'I select the proper values for "{provider}" to create the "{machine_name}" machine')
def cloud_creds(context, provider, machine_name):
    provider = provider.strip().lower()
    if provider not in machine_values_dict.keys():
        raise Exception("Unknown cloud provider")
    set_values_to_create_machine_form(context,provider,machine_name)


@step(u'I expect for "{key}" key to appear within max {seconds} seconds')
def key_appears(context, key, seconds):
    if context.mist_config.get(key):
        key_name = context.mist_config.get(key)
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            for key_in_list in context.browser.find_elements_by_class_name('small-list-item'):
                if key_name == safe_get_element_text(key_in_list):
                    actions = ActionChains(context.browser)
                    actions.send_keys(Keys.ESCAPE)
                    actions.perform()
                    return True
                else:
                    pass
        except:
            sleep(1)
    assert False, "Key %s did not appear after %s seconds" % (key,seconds)


@step(u'I expect for "{key}" key to appear within max {seconds} seconds')
def key_appears(context, key, seconds):
    if context.mist_config.get(key):
        key_name = context.mist_config.get(key)
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            for key_in_list in context.browser.find_elements_by_class_name('small-list-item'):
                if key_name == safe_get_element_text(key_in_list):
                    actions = ActionChains(context.browser)
                    actions.send_keys(Keys.ESCAPE)
                    actions.perform()
                    return True
                else:
                    pass
        except:
            sleep(1)
    assert False, "Key %s did not appear after %s seconds" % (key,seconds)


@step(u'I wait for max {seconds} seconds until tag with key "{key}" and value'
      u' "{value}" is available')
def wait_for_tags(context, seconds, key,value):
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            check_the_tags(context, key, value)
            return
        except:
            sleep(1)
    assert False, "Tag with key %s and value %s was not available after %s" \
                  " seconds" % (key. value, seconds)


@step(u'I check the sorting by "{sorting_field}"')
def check_sorting(context, sorting_field):
    """
    Check the sorting for name, state or cloud in the machines list. This
    function checks basically if the machines have the desired vertical

    """
    sorting_field = sorting_field.lower()
    machines_elements = context.browser.find_elements_by_css_selector(
        '#machine-list li.checkbox-link ')
    machines = []
    for machine in machines_elements:
        name = safe_get_element_text(
            machine.find_element_by_class_name('machine-name')).lower()
        state = safe_get_element_text(
            machine.find_element_by_class_name('machine-state')).lower()
        if state == '':
            state = 'unknown'
        cloud = safe_get_element_text(machine.find_element_by_css_selector(
            '.machine-tags .tag:first-child')).lower()
        machines.append((name, state, cloud, machine.location['y']))

    # sort the list of machine tuples
    if sorting_field == 'name':
        machines = sorted(machines, key=lambda x: x[0])
    elif sorting_field == 'state':
        machines = sorted(machines, key=lambda x: x[1],
                          cmp=lambda x, y: machine_states_ordering[y] -
                                           machine_states_ordering[x])
    elif sorting_field == 'cloud':
        machines = sorted(machines, key=lambda x: x[2])

    # make sure that the list is also sorted by element height
    for i in range(len(machines) - 1):
        assert machines[i][3] < machines[i + 1][3], "Machine list is not" \
                                                    " properly sorted by %s." \
                                                    " Expected field was %s " \
                                                    "and actual field was " \
                                                    "%s" % (sorting_field,
                                                            machines[i],
                                                            machines[i + 1])


@step(u'I clear the machines search bar')
def clear_machines_search_bar(context):
    search_bar_machine = context.browser.find_element_by_css_selector(
        "div.machine-search-container "
        "input.machine-search")
    search_bar_machine.clear()


@step(u'I fill in a "{name}" machine name')
def fill_machine_mame(context, name):
    """
    This step will create a random machine name and a suitable name for an
    accompanying ssh key and will update the context.
    """
    if 'random' in name or context.mist_config.get(name):
        if not context.mist_config.get(name):
            if 'random ' in name:
                name = name.lstrip('random ')
            machine_name = context.mist_config[name] = "testlikeapro%s" % randrange(10000)
        else:
            machine_name = context.mist_config[name]
    else:
        machine_name = name
    textfield = context.browser.find_element_by_id("create-machine-name")
    textfield.send_keys(machine_name)
    context.mist_config[name + "_machine_key"] = machine_name + "_key"
    sleep(1)


@step(u'I choose the "{name}" machine')
def choose_machine(context, name):
    if context.mist_config.get(name):
        name = context.mist_config.get(name)

    end_time = time() + 20
    while time() < end_time:
        machine = get_machine(context, name)
        if machine:
            checkbox = machine.find_element_by_class_name("ui-checkbox")
            checkbox.click()
            return

        sleep(2)
    assert False, u'Could not choose/tick %s machine' % name


@step(u'I should see the "{name}" machine added within {seconds} seconds')
def assert_machine_added(context, name, seconds):
    if context.mist_config.get(name):
        name = context.mist_config.get(name)

    end_time = time() + int(seconds)
    while time() < end_time:
        machine = get_machine(context, name)
        if machine:
            return
        sleep(2)

    assert False, u'%s is not added' % name


# @step(u'"{name}" machine state should be "{state}" within {seconds} seconds')
# def assert_machine_state(context, name, state, seconds):
#     if context.mist_config.get(name):
#         name = context.mist_config.get(name)
#
#     end_time = time() + int(seconds)
#     while time() < end_time:
#         machine = get_machine(context, name)
#         if machine:
#             try:
#                 if state in safe_get_element_text(machine):
#                     return
#             except NoSuchElementException:
#                 pass
#             except StaleElementReferenceException:
#                 pass
#         sleep(2)
#
#     assert False, u'%s state is not "%s"' % (name, state)
#
#
# @step(u'"{name}" machine should be probed within {seconds} seconds')
# def assert_machine_probed(context, name, seconds):
#     if context.mist_config.get(name):
#         name = context.mist_config.get(name)
#
#     end_time = time() + int(seconds)
#     while time() < end_time:
#         machine = get_machine(context, name)
#         if machine:
#             try:
#                 machine.find_element_by_class_name("probed")
#                 return
#             except NoSuchElementException:
#                 pass
#             except StaleElementReferenceException:
#                 pass
#             sleep(3)
#
#     assert False, u'%s machine is not probed within %s seconds' % (
#                     name, seconds)


def get_machine(context, name):
    try:
        placeholder = context.browser.find_element_by_id("machine-list-page")
        machines = placeholder.find_elements_by_tag_name("li")

        for machine in machines:
            machine_text = safe_get_element_text(machine)
            if name in machine_text:
                return machine

        return None
    except NoSuchElementException:
        return None
    except StaleElementReferenceException:
        return None


@step(u'I upload the ssh key with name "{new_key_name}"')
def upload_my_key(context, new_key_name):
    end_time = time() + 15
    while time() < end_time:
        try:
            key_add_popup = context.browser.find_element_by_id('key-add-popup')
            display = key_add_popup.value_of_css_property("display")
            width = key_add_popup.value_of_css_property("width")
            if 'block' in display:
                if width != '1px':
                    break
            raise NoSuchElementException
        except NoSuchElementException:
            assert time() + 1 < end_time, 'Key add popup has not appeared ' \
                                          'after 5 seconds'
            sleep(1)
    key_name = context.browser.find_element_by_id("key-add-id")
    key_name.send_keys(
        context.mist_config['CREDENTIALS'][new_key_name]['key_name'])
    upload = context.browser.find_element_by_id("key-add-upload")
    upload.send_keys(
        context.mist_config['CREDENTIALS'][new_key_name]['key_path'])
    context.execute_steps(u'When I click the button "Add"')


@step(u'I wait for probing to finish for {seconds} seconds max')
def wait_for_loader_to_finish(context, seconds):
    rows = context.browser.find_elements_by_tag_name('tr')
    for row in rows:
        cells = row.find_elements_by_tag_name('td')
        cells_text = safe_get_element_text(cells[0])
        if cells_text == 'Last probed':
            end_time = time() + int(seconds)
            while time() < end_time:
                try:
                    cells[1].find_element_by_class_name('ajax-loader')
                    sleep(1)
                except NoSuchElementException:
                    sleep(1)
                    return
            assert False, "Ajax loading hasn't finished after %s seconds" % seconds
    assert False, "Could not locate ajax loader"


@step(u'If the key addition was successful')
def success(context):
    try:
        popup = context.browser.find_element_by_id('machine-userPort-popup-popup')
        div = popup.find_element_by_class_name('message')
        div_text = safe_get_element_text(div)
        if div_text == 'Cannot connect as root on port 22':
            raise ValueError('Could not connect with server with ssh key')
    except NoSuchElementException:
        pass


@step(u'probing was successful')
def check_probing(context):
    rows = context.browser.find_elements_by_tag_name('tr')
    for row in rows:
        cells = row.find_elements_by_tag_name('td')
        cells_zero_text = safe_get_element_text(cells[0])
        if cells_zero_text == 'Last probed':
            cells_one_text = safe_get_element_text(cells[1])
            message = cells_one_text.split('\n')[0].lower()
            assert message == 'just now', "Probing of machine failed" \
                                          "(message is: %s)" % cells_one_text
            return
    assert False, "Could not find any line about probing"


@given(u'ssh key with name "{ssh_key_name}" is added')
def ssh_key_is_added(context, ssh_key_name):
    # first we have to find the keys button
    buttons = context.browser.find_elements_by_class_name('ui-btn')
    for button in buttons:
        button_text = safe_get_element_text(button)
        if 'add key' in button_text.lower():
            # if there no keys then it will be called "Add key"
            context.execute_steps(u"""
                Then I click the button "Add key"
                And I expect for "non-associated-keys-popup-popup" popup to appear within max 4 seconds
            """)
            # check if the key is already uploaded but not associated
            key_already_associated = False
            non_associated_keys = context.browser.find_element_by_id('non-associated-keys-popup').find_elements_by_tag_name('li')
            for non_associated_key in non_associated_keys:
                if context.mist_config['CREDENTIALS'][ssh_key_name]['key_name'].lower() in safe_get_element_text(non_associated_key).lower():
                    non_associated_key.click()
                    key_already_associated = True
                    break

            if not key_already_associated:
                context.execute_steps(u"""
                    When I click the "New key" button inside the "Add key" popup
                    Then I expect for "key-add-popup" popup to appear within max 2 seconds
                    And I upload the ssh key with name "%s"
                """ % ssh_key_name)

            context.execute_steps(u"""
                Then I expect for "machine-keys-panel" side panel to appear within max 4 seconds
                And I expect for "machine-associating-key-loader" loader to finish within max 100 seconds
                Then If the key addition was successful
            """)
            context.browser.find_elements_by_class_name('ui-panel-dismiss')[0].click()
            return
        elif 'keys' in button_text.lower():
            # otherwise it will be called "? keys" where ? is the number of
            # saved keys. before adding the key we need to check if it's already
            # saved
            context.execute_steps(u'''
                Then I click the button "%s"
                And I expect for "machine-keys-panel" side panel to appear within max 4 seconds
            ''' % safe_get_element_text(button))
            machine_keys_list = context.browser.find_element_by_id("machine-keys")
            machines_keys = machine_keys_list.find_elements_by_class_name(
                "small-list-item")
            checked_texts = []
            for machines_key in machines_keys:
                machines_key_text = safe_get_element_text(machines_key)
                if not machines_key_text or not machines_key_text.strip():
                    # sometimes the code checks for the texts too fast and they
                    # haven't been fetched yet so we do a sleep
                    sleep(1)
                checked_texts.append(machines_key_text)
                if context.mist_config['CREDENTIALS'][ssh_key_name]['key_name']\
                        in machines_key_text:
                    context.browser.find_elements_by_class_name('ui-panel-dismiss')[0].click()
                    context.execute_steps(u'Then I expect for '
                                          u'"machine-keys-panel" side panel '
                                          u'to disappear within max 4 seconds')
                    return
            context.execute_steps(u"""
                When I click the "New key" button inside the "Manage Keys" panel
                And I expect for "non-associated-keys-popup" popup to appear within max 4 seconds
            """)
            # check if the key is already uploaded but not associated
            key_already_associated = False
            non_associated_keys = context.browser.find_element_by_id('non-associated-keys-popup').find_elements_by_tag_name('li')
            for non_associated_key in non_associated_keys:
                if context.mist_config['CREDENTIALS'][ssh_key_name]['key_name'].lower() in safe_get_element_text(non_associated_key).lower():
                    non_associated_key.click()
                    key_already_associated = True
                    break

            if not key_already_associated:
                context.execute_steps(u"""
                    When I click the "New key" button inside the "Add Key" popup
                    Then I expect for "key-add-popup" popup to appear within max 2 seconds
                    And I upload the ssh key with name "%s"
                """ % ssh_key_name)

            context.execute_steps(u"""
                Then I expect for "key-generate-loader" loader to finish within max 5 seconds
                And I expect for "machine-associating-key-loader" loader to finish within max 100 seconds
                And If the key addition was successful
            """)
            context.browser.find_elements_by_class_name('ui-panel-dismiss')[0].click()
            context.execute_steps(u'Then I expect for "machine-keys-panel" '
                                  u'side panel to disappear within max 4 '
                                  u'seconds')


@step(u'I fill "{value}" as rule value')
def rule_value(context, value):
    value_input = context.browser.find_element_by_class_name("rule-value")
    value_input.send_keys(u'\ue003')
    value_input.send_keys(value)


@step(u"I enable monitoring if it's not enabled")
def enable_monitoring(context):
    button = context.browser.find_element_by_id("enable-monitoring-btn")
    clicketi_click(context, button)
    context.execute_steps("""
        Then I expect for "dialog-popup" modal to appear within max 4 seconds
        And I click the "Yes" button inside the "ENABLE MONITORING" modal
        And I expect for "dialog-popup" modal to disappear within max 4 seconds
    """)


@step(u'I give a default script for python script')
def fill_default_script(context):
    textfield = context.browser.find_element_by_id("custom-plugin-script")
    textfield.clear()
    my_script ="import time\n\ntry:\n    from urllib2 import urlopen \n\n" \
               "except ImportError:\n    from urllib import urlopen\n" \
               "URL = 'https://mist.io'\n\n" \
               "TEXT = 'GOVERN YOUR CLOUDS'\nCHECK_TIMES = 10\nRESULT = -1\n\n" \
               "def read():\n    global CHECK_TIMES\n    global RESULT\n" \
               "    if CHECK_TIMES < 10:\n        CHECK_TIMES += 1\n        return RESULT\n" \
               "    CHECK_TIMES = 0\n\n    start=time.time()\n    try:\n" \
               "        nf=urlopen(URL)\n    except:\n        RESULT = -1\n" \
               "        return RESULT\n    page=nf.read()\n    end=time.time()\n" \
               "    nf.close()\n    if TEXT in page:\n        RESULT = end - start\n" \
               "    else:\n        RESULT =  -1\n    return RESULT"
    for letter in my_script:
        textfield.send_keys(letter)


@step(u'I remove previous rules')
def remove_previous_rules(context):
    previous_rules = context.browser.find_elements_by_class_name('rule-box')
    rule_length = len(previous_rules)
    if rule_length > 0:
        context.execute_steps(u'Then I expect for buttons inside '
                              u'"basic-condition" to be clickable within max '
                              u'20 seconds')
        position = previous_rules[0].location['y']
        context.browser.execute_script("window.scrollTo(0, %s)" % position)
    while rule_length > 0:
        rule = previous_rules.pop()
        delete_rule_button = rule.find_element_by_class_name('delete-rule-button')
        clicketi_click(context, delete_rule_button)
        previous_rules = context.browser.find_elements_by_class_name('rule-box')
        sleeps = 0
        while len(previous_rules) == rule_length:
            assert sleeps != 10, "Rule hasn't been deleted after 10 seconds"
            sleep(1)
            sleeps += 1
            previous_rules = context.browser.find_elements_by_class_name('rule-box')
        rule_length = len(previous_rules)


@step(u'I wait for max {seconds} seconds for "{name}" machine from "{provider}"'
      u' to disappear')
def check_machine_deletion(context, name, provider, seconds):
    if provider == "EC2":
        context.execute_steps(u'Then %s machine state should be "terminated"'
                              u' within %s seconds' % (name, seconds))
    else:
        machines_elements = context.browser.find_elements_by_css_selector('#machine-list-container li .machine-name')
        machines_names_list = [safe_get_element_text(machine_element) for machine_element in machines_elements]
        end_time = time() + int(seconds)
        while time() < end_time:
            if name not in machines_names_list:
                break
