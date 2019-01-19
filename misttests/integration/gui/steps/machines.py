from behave import step
from behave import given

from time import time
from time import sleep

from random import randrange

from .utils import safe_get_element_text, get_page_element, expand_shadow_root, get_page

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
    "digital ocean": ["Ubuntu 14.04.5 x64", "512mb", "Amsterdam 2"],
    "packet": ["Ubuntu 14.04 LTS", "Type 0 - 8GB RAM", "Amsterdam, NL"],
    "openstack": ["CoreOS", "m1.tiny", "0"],
    "rackspace": ["Ubuntu 14.04 LTS (Trusty Tahr) (PV)", "512MB Standard Instance", "0"],
    "nephoscale": ["Ubuntu Server 14.04 LTS 64-bit", "CS05 - Cloud Server 0.5 GB RAM, 1 Core", "SJC-1"],
    "softlayer": ["Ubuntu - Latest (64 bit) ", "1 CPU, 1GB ram, 25GB ", "AMS01 - Amsterdam"],
    "azure": ["Ubuntu Server 14.04 LTS", "ExtraSmall (1 cores, 768 MB) ", "West Europe"],
    "docker": ["Ubuntu 14.04 - mist.io image"]
}

@step(u'I click the other server machine')
def click_bare_metal_machine(context):
    context.execute_steps(u'Then I click on list item "%s" machine' % context.mist_config['bare_metal_host'])


def set_values_to_create_machine_form(context,provider,machine_name):
    context.execute_steps(u'''
                Then I set the value "%s" to field "Machine Name" in the "machine" add form
                When I open the "Image" dropdown in the "machine" add form
                And I click the "%s" button in the "Image" dropdown in the "machine" add form
                And I open the "Key" dropdown in the "machine" add form
                And I click the "DummyKey" button in the "Key" dropdown in the "machine" add form
                And I wait for 1 seconds
            ''' % (machine_name,
                   machine_values_dict.get(provider)[0]))

    if 'digital ocean' in provider:
        context.execute_steps(u'''
                    When I open the "Size" drop down in the "machine" add form
                    And I click the "%s" button in the "Size" dropdown in the "machine" add form
                    When I open the "Location" drop down in the "machine" add form
                    And I click the "%s" button in the "Location" dropdown in the "machine" add form
                ''' % ( machine_values_dict.get(provider)[1],
                       machine_values_dict.get(provider)[2]))


@step(u'I select the proper values for "{provider}" to create the "{machine_name}" machine')
def cloud_creds(context, provider, machine_name):
    provider = provider.strip().lower()
    if provider not in machine_values_dict.keys():
        raise Exception("Unknown cloud provider")
    set_values_to_create_machine_form(context, provider, machine_name)


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


@step(u'I choose the "{name}" machine')
def choose_machine(context, name):
    if context.mist_config.get(name):
        name = context.mist_config.get(name)
    end_time = time() + 20
    while time() < end_time:
        machine = get_machine(context, name)
        if machine:
            checkbox = machine.find_element_by_tag_name("mist-check")
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
        machines = placeholder.find_elements_by_tag_name("vaadin-grid-table-row")

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


@step(u'rule "{rule}" should be {state} in the "{page}" page')
def verify_rule_is_present(context, rule, state, page):
    found = False
    state = state.lower()
    if state not in ['present', 'absent']:
        raise Exception('Unknown state %s' % state)
    page_element = get_page(context, page)
    page_shadow = expand_shadow_root(context, page_element)
    rules = page_shadow.find_element_by_css_selector('mist-rules').text.replace('\n','').replace(' ','').lower()
    rule = rule.replace(" ", "").lower()
    if rule in rules:
        found = True
    if state == 'present' and found:
        return True
    if state == 'absent' and not found:
        return True
    assert False, "Rule %s was not %s in existing rules for the monitored machine" % (rule, state)


@step(u'"{key}" key should be associated with the machine "{machine}"')
def check_for_associated_key(context, key, machine):
    page = get_page(context, "machine")
    page_shadow = expand_shadow_root(context, page)
    machine_keys_class = page_shadow.find_elements_by_css_selector('div.associatedKeys > div.machine-key')
    for element in machine_keys_class:
        if safe_get_element_text(element) == key:
            return
    assert False, "The key has not been associated with the machine!"


@step(u'I delete the associated key "{key}"')
def disassociate_key(context, key):
    _, page = get_page_element(context, "machines", "machine")
    page_shadow = expand_shadow_root(context, page)
    machine_keys_class = page_shadow.find_elements_by_css_selector('div.associatedKeys > div.machine-key')
    for element in machine_keys_class:
        if safe_get_element_text(element) == key:
            delete_btn = element.find_element_by_css_selector('.delete')
            clicketi_click(context, delete_btn)
            return


@step(u'there should be {keys} keys associated with the machine within {seconds} seconds')
def keys_associated_with_machine(context, keys, seconds):
    timeout = time() + int(seconds)
    _, page = get_page_element(context, "machines", "machine")
    page_shadow = expand_shadow_root(context, page)
    while time() < timeout:
        machine_keys_class = page_shadow.find_elements_by_css_selector('div.associatedKeys > div.machine-key')
        associated_keys_with_machine = 0
        for element in machine_keys_class:
            try:
                element.find_element_by_tag_name('a')
                associated_keys_with_machine += 1
            except:
                pass
        if associated_keys_with_machine == int(keys):
            return
    assert False, "There are %s keys associated with the machine" % associated_keys_with_machine
