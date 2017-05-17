from behave import step
from behave import given

from time import time
from time import sleep

from random import randrange

from .utils import safe_get_element_text

from .buttons import clicketi_click

from selenium.webdriver.common.keys import Keys

from selenium.webdriver import ActionChains

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
    "docker": ["mist/ubuntu-14.04:latest"]
}


def set_values_to_create_machine_form(context,provider,machine_name):
    context.execute_steps(u'''
                Then I set the value "%s" to field "Machine Name" in "machine" add form
                When I open the "Image" drop down
                And I click the button "%s" in the "Image" dropdown
                And I open the "Key" drop down
                And I click the button "Key1" in the "Key" dropdown
            ''' % (machine_name,
                   machine_values_dict.get(provider)[0]))



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


@step(u'I clear the machines search bar')
def clear_machines_search_bar(context):
    clear_button = context.browser.find_element_by_xpath("//iron-icon[@icon='close']")
    clicketi_click(context, clear_button)


@step(u'I open the actions dialog')
def open_actions_dialog_from_list(context):
    button = context.browser.find_element_by_xpath("//iron-icon[@icon='more-vert']")
    clicketi_click(context, button)


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


def get_machine(context, name):
    try:
        placeholder = context.browser.find_element_by_tag_name("page-machines").find_element_by_id("items")
        machines = placeholder.find_elements_by_tag_name("div")

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


@step(u'I click the "{rule_class}" rule')
def click_rule_dropdown(context, rule_class):
    rule_element = context.browser.find_element_by_xpath('//paper-dropdown-menu[contains(@class, "%s")]' % rule_class)
    clicketi_click(context, rule_element)


@step(u'I save the rule')
def save_rule(context):
    container = context.browser.find_element_by_xpath('//div[contains(@class, "rule-actions")]')
    button = container.find_element_by_xpath('.//paper-button[contains(@class, "blue")]')
    clicketi_click(context, button)


@step(u'I remove previous rules')
def remove_previous_rules(context):
    previous_rules = context.browser.find_elements_by_tag_name('rules-item')
    rule_length = len(previous_rules)
    if rule_length > 0:
        position = previous_rules[0].location['y']
        context.browser.execute_script("window.scrollTo(0, %s)" % position)
    while rule_length > 0:
        rule = previous_rules.pop()
        delete_rule_button = rule.find_element_by_xpath(".//iron-icon[@icon='close']")
        clicketi_click(context, delete_rule_button)
        previous_rules = context.browser.find_elements_by_tag_name('rules-item')
        sleeps = 0
        while len(previous_rules) == rule_length:
            assert sleeps != 10, "Rule hasn't been deleted after 10 seconds"
            sleep(1)
            sleeps += 1
            previous_rules = context.browser.find_elements_by_tag_name('rules-item')
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


@step(u'I search for the machine "{name}"')
def search_for_mayday_machine(context, name):
    if context.mist_config.get(name):
        name = context.mist_config.get(name)
    search_bar = context.browser.find_element_by_css_selector("input.top-search")
    for letter in name:
        search_bar.send_keys(letter)
    sleep(2)


@step(u'"{key}" key should be associated with the machine "{machine}"')
def check_for_associated_key(context, key, machine):
    associated_key_class = context.browser.find_element_by_class_name('associatedKeys')
    associated_keys = associated_key_class.find_elements_by_class_name('machine-key')
    for element in associated_keys:
        if safe_get_element_text(element) == key:
            return
    assert False, "The key has not been associated with the machine!"


@step(u'I delete the associated key')
def disassociate_key(context):
    associated_key_class = context.browser.find_element_by_class_name('associatedKeys')
    associated_key = associated_key_class.find_element_by_class_name('machine-key')
    delete_btn = associated_key.find_element_by_class_name('delete')
    clicketi_click(context, delete_btn)


@step(u'there should be {keys} keys associated with the machine')
def keys_associated_with_machine(context, keys):
    associated_keys = context.browser.find_element_by_class_name('associatedKeys')
    machine_keys_class = associated_keys.find_elements_by_class_name('machine-key')
    associated_keys_with_machine = 0
    for element in machine_keys_class:
        try:
            element.find_element_by_tag_name('a')
            associated_keys_with_machine += 1
        except:
            pass

    assert associated_keys_with_machine == int(keys), "There are %s keys associated with the machine" % associated_keys_with_machine
