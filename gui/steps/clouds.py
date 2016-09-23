import json

from behave import step

from time import time
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from .utils import wait_until_visible
from .utils import safe_get_element_text

from .forms import clear_input_and_send_keys

from .buttons import clicketi_click
from .buttons import click_button_from_collection


cloud_creds_dict = {
    "openstack": "OPENSTACK",
    "rackspace": "RACKSPACE",
    "azure": "AZURE",
    "softlayer": "SOFTLAYER",
    "hp": "HP",
    "ec2": "EC2",
    "aws": "AWS",
    "nepho": "NEPHOSCALE",
    "linode": "LINODE",
    "docker": "DOCKER",
    "digital ocean": "DIGITALOCEAN",
    "indonesian": "INDONESIAN",
    "kvm (via libvirt)": "KVM (via libvirt)",
    "packet": "PACKET",
    "gce": "GCE",
    "nephoscale": "NEPHOSCALE",
    "vmware vcloud": "VMWARE VCLOUD",
    "vsphere": "VMWARE VSPHERE"
}


@step(u'I use my provider "{cloud}" credentials')
def cloud_creds(context, cloud):
    from .forms import set_value_to_field
    if "AZURE" in cloud:
        subscription_id = context.mist_config['CREDENTIALS']['AZURE']['subscription_id']
        certificate = context.mist_config['CREDENTIALS']['AZURE']['certificate']
        context.execute_steps(u'''
            Then I set the value "Azure" to field "Title" in "cloud" add form
            And I set the value "%s" to field "Subscription ID" in "cloud" add form
            ''' % subscription_id)
        set_value_to_field(context, certificate, 'certificate', 'cloud', 'add')
        sleep(3)
    elif "GCE" in cloud:
        project_id = context.mist_config['CREDENTIALS']['GCE']['project_id']
        private_key = context.mist_config['CREDENTIALS']['GCE']['private_key']
        context.execute_steps(u'''
            Then I set the value "%s" to field "Title" in "cloud" add form
            Then I set the value "%s" to field "Project ID" in "cloud" add form
            Then I set the value "%s" to field "Private Key" in "cloud" add form
        ''' % ('GCE', project_id, json.dumps(private_key)))
    elif "RACKSPACE" in cloud:
        region = context.mist_config['CREDENTIALS']['RACKSPACE']['region']
        username = context.mist_config['CREDENTIALS']['RACKSPACE']['username']
        api_key = context.mist_config['CREDENTIALS']['RACKSPACE']['api_key']
        context.execute_steps(u'''
            Then I open the "Region" drop down
            And I wait for 1 seconds
            When I click the button "%s" in the "Region" dropdown
            Then I set the value "Rackspace" to field "Title" in "cloud" add form
            Then I set the value "%s" to field "Username" in "cloud" add form
            Then I set the value "%s" to field "API Key" in "cloud" add form
        ''' % (region, username, api_key))
    elif "SOFTLAYER" in cloud:
        username = context.mist_config['CREDENTIALS']['SOFTLAYER']['username']
        api_key = context.mist_config['CREDENTIALS']['SOFTLAYER']['api_key']
        context.execute_steps(u'''
            Then I set the value "%s" to field "Username" in "cloud" add form
            Then I set the value "%s" to field "API Key" in "cloud" add form
        ''' % (username, api_key))
    elif "AWS" in cloud:
        api_key = context.mist_config['CREDENTIALS']['AWS']['api_key']
        api_secret = context.mist_config['CREDENTIALS']['AWS']['api_secret']
        region = context.mist_config['CREDENTIALS']['AWS']['region']
        context.execute_steps(u'''
            Then I open the "Region" drop down
            And I wait for 1 seconds
            When I click the button "%s" in the "Region" dropdown
            And I wait for 1 seconds
            Then I set the value "AWS" to field "Title" in "cloud" add form
            And I set the value "%s" to field "API Key" in "cloud" add form
            And I set the value "%s" to field "API Secret" in "cloud" add form
        ''' % (region, api_key, api_secret))
    elif "NEPHOSCALE" in cloud:
        username = context.mist_config['CREDENTIALS']['NEPHOSCALE']['username']
        password =  context.mist_config['CREDENTIALS']['NEPHOSCALE']['password']
        context.execute_steps(u'''
            Then I set the value "%s" to field "Username" in "cloud" add form
            Then I set the value "%s" to field "Password" in "cloud" add form
        ''' % (username, password))
    elif "LINODE" in cloud:
        api_key = context.mist_config['CREDENTIALS']['LINODE']['api_key']
        context.execute_steps(u'Then I set the value "%s" to field "API Key" in "cloud" add form' % api_key)
    elif "DIGITALOCEAN" in cloud:
        token = context.mist_config['CREDENTIALS']['DIGITALOCEAN']['token']
        context.execute_steps(u'''
            Then I set the value "%s" to field "Token" in "cloud" add form
        ''' % token)
    elif "PACKET" in cloud:
        api_key = context.mist_config['CREDENTIALS']['PACKET']['api_key']
        context.execute_steps(u'''
            Then I set the value "%s" to field "API Key" in "cloud" add form
        ''' % api_key)
    elif "DOCKER" in cloud:
        host = context.mist_config['CREDENTIALS']['DOCKER']['host']
        authentication = context.mist_config['CREDENTIALS']['DOCKER']['authentication']
        port = context.mist_config['CREDENTIALS']['DOCKER']['port']
        context.execute_steps(u'''
            Then I set the value "Docker" to field "Title" in "cloud" add form
            Then I set the value "%s" to field "Host" in "cloud" add form
            Then I set the value "%s" to field "Port" in "cloud" add form
            Then I open the "Authentication" drop down
            And I wait for 1 seconds
            When I click the button "%s" in the "Authentication" dropdown
        ''' % (host, port, authentication))

        certificate = context.mist_config['CREDENTIALS']['DOCKER']['cert']
        key = context.mist_config['CREDENTIALS']['DOCKER']['key']
        ca = context.mist_config['CREDENTIALS']['DOCKER']['ca']

        set_value_to_field(context, key, 'key', 'cloud', 'add')
        set_value_to_field(context, certificate, 'certificate', 'cloud', 'add')
        set_value_to_field(context, ca, 'ca certificate', 'cloud', 'add')


def find_cloud(context, cloud_title):
    cloud_chips = context.browser.find_elements_by_tag_name('cloud-chip')
    clouds = []
    for cloud in cloud_chips:
        try:
            if cloud.is_displayed:
                clouds.append(cloud)
        except StaleElementReferenceException:
            pass
    for c in clouds:
        try:
            title = c.find_element_by_class_name('cloud-title')
            if safe_get_element_text(title).lower().strip() == cloud_title:
                return c
        except (NoSuchElementException, StaleElementReferenceException):
            pass
    return None


def find_cloud_info(context, cloud_title):
    clouds = context.browser.find_elements_by_tag_name('cloud-info')
    clouds = filter(lambda el: el.is_displayed(), clouds)
    for c in clouds:
        try:
            input_containers = c.find_elements_by_id('labelAndInputContainer')
            for container in input_containers:
                text = safe_get_element_text(container.find_element_by_tag_name('label')).lower().strip()
                if text == 'title':
                    text = container.find_element_by_tag_name('input').\
                            get_attribute('value').lower().strip()
                    if text == cloud_title:
                        return c
        except NoSuchElementException:
            pass
    return None


@step(u'"{cloud}" cloud has been added')
def given_cloud(context, cloud):
    if find_cloud(context, cloud.lower()):
        return True

    creds = cloud_creds_dict.get(cloud.lower())
    assert creds, u'Could not find credentials for %s' % cloud

    context.execute_steps(u'''
        When I click the new cloud button
        Then I expect the "Cloud" add form to be visible within max 10 seconds
        And I open the "Choose Provider" drop down
        And I wait for 1 seconds
        When I click the button "%s" in the "Choose Provider" dropdown
        Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
        When I use my provider "%s" credentials
        And I focus on the button "Add Cloud" in "cloud" add form
        Then I click the button "Add Cloud"
        And I click the mist.io button
        Then the "%s" provider should be added within 120 seconds
    ''' % (cloud, creds, cloud))


@step(u'I {action} the cloud menu for "{provider}"')
def open_cloud_menu(context, action, provider):
    action = action.lower()
    if action not in ['open', 'close']:
        raise Exception('Unrecognized action')
    if action == 'open':
        cloud = find_cloud(context, provider.lower())
        assert cloud, "Provider %s is not available" % provider
        clicketi_click(context, cloud)
    cloud_info = find_cloud_info(context, provider.lower())
    if action == 'close':
        close_button = cloud_info.find_element_by_id('close-btn')
        clicketi_click(context, close_button)
    seconds = 4
    end_time = time() + seconds
    while time() < end_time:
        cloud_menu = find_cloud_info(context, provider.lower())
        if action == 'open' and cloud_menu:
            return True
        if action == 'close' and not cloud_menu:
            return True
        sleep(1)
    assert False, u'%s menu did not %s after %s seconds' \
                  % (provider, action, seconds)


@step(u'I rename the cloud "{cloud}" to "{new_name}"')
def rename_cloud(context, cloud, new_name):
    cloud_info = find_cloud_info(context, cloud.lower())
    assert cloud_info, "Cloud menu has not been found"
    input_containers = cloud_info.find_elements_by_id('labelAndInputContainer')
    for container in input_containers:
        text = safe_get_element_text(container.find_element_by_tag_name('label')).lower().strip()
        if text == 'title':
            input = container.find_element_by_tag_name('input')
            clear_input_and_send_keys(input, new_name)
            buttons = cloud_info.find_elements_by_tag_name('paper-button')
            click_button_from_collection(context, 'save', buttons)
            return True
    return False


@step(u'I delete the "{provider}" cloud')
def delete_cloud(context, provider):
    cloud_info = find_cloud_info(context, provider.lower())
    assert cloud_info, "Cloud menu has not been found"
    cloud_menu_buttons = cloud_info.find_elements_by_tag_name('paper-button')
    click_button_from_collection(context, 'Delete Cloud', cloud_menu_buttons)


@step(u'the "{cloud}" provider should be added within {seconds} seconds')
def cloud_added(context, cloud, seconds):
    end_time = time() + int(seconds)
    while time() < end_time:
        if find_cloud(context, cloud.lower()):
            return True
        sleep(2)
    assert False, u'%s is not added within %s seconds' % (cloud, seconds)


@step(u'the "{cloud}" cloud should be deleted')
def cloud_deleted(context, cloud):
    if find_cloud(context, cloud.lower()):
        return False


@step(u'the "{cloud}" cloud should be deleted within "{seconds}" seconds')
def cloud_deleted(context, cloud, seconds):
    timeout = time() + int(seconds)
    while time() < timeout:
        if not find_cloud(context, cloud.lower()):
            return True
        sleep(1)
    assert False, "Cloud has not been deleted after %s seconds" % seconds


@step(u'I ensure "{title}" cloud is enabled')
def ensure_cloud_enabled(context, title):
    cloud = find_cloud(context, title.lower())
    assert cloud, "Cloud %s has not been added" % title
    return 'offline' in cloud.get_attibute('class')
