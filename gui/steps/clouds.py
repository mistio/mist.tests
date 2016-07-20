import json

from behave import *

from time import time
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from .utils import wait_until_visible
from .utils import safe_get_element_text
from .utils import clear_input_and_send_keys

from .buttons import clicketi_click
from .buttons import click_button_from_collection


cloud_creds_dict = {
    "openstack": "OPENSTACK",
    "rackspace": "RACKSPACE",
    "azure": "AZURE",
    "softlayer": "SOFTLAYER",
    "hp": "HP",
    "ec2": "EC2",
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
    if "AZURE" in cloud:
        subscription_id = None
        for i in range(0, 2):
            try:
                subscription_id = context.browser.find_element_by_id("subscription_id")
                break
            except NoSuchElementException as e:
                if i == 2:
                    raise e
                sleep(1)
        subscription_id.send_keys(context.mist_config['CREDENTIALS']['AZURE']['subscription_id'])
        context.execute_steps(u'''
        When I click the "Add Certificate" button inside the "Add Cloud" panel
        Then I expect for "file-upload-popup" popup to appear within max 4 seconds
        ''')
        upload_area = context.browser.find_element_by_id("upload-area")
        upload_area.send_keys(context.mist_config['CREDENTIALS']['AZURE']['certificate'])
        context.execute_steps(u'''
        When I click the "Done" button inside the "Upload" popup
        Then I expect for "file-upload-popup" popup to disappear within max 4 seconds
        ''')
    elif "GCE" in cloud:
        title = context.browser.find_element_by_id("title")
        for i in range(1, 6):
            title.send_keys(u'\ue003')
        title.send_keys("GCE")
        project_id = context.browser.find_element_by_id("project_id")
        project_id.send_keys(context.mist_config['CREDENTIALS']['GCE']['project_id'])
        context.execute_steps(u'''
        When I click the "Add JSON Key" button inside the "Add Cloud" panel
        Then I expect for "file-upload-popup" popup to appear within max 4 seconds
        ''')
        # file_input = context.browser.find_element_by_id("file-upload-input")
        # file_input.send_keys(context.mist_config['CREDENTIALS']['GCE']['private_key'])
        json_input = context.browser.find_element_by_id("upload-area")
        json_input.send_keys(json.dumps(context.mist_config['CREDENTIALS']['GCE']['private_key']))
        context.execute_steps(u'''
            Then I expect for "file-upload-ok" to be clickable within max 4 seconds
            When I click the "Done" button inside the "Upload" popup
            Then I expect for "file-upload-popup" popup to disappear within max 4 seconds
        ''')
    elif "OPENSTACK" in cloud:
        username = context.browser.find_element_by_id("username")
        username.send_keys(context.mist_config['CREDENTIALS']['OPENSTACK']['username'])
        password = context.browser.find_element_by_id("password")
        password.send_keys(context.mist_config['CREDENTIALS']['OPENSTACK']['password'])
        auth_url = context.browser.find_element_by_id("auth_url")
        auth_url.send_keys(context.mist_config['CREDENTIALS']['OPENSTACK']['auth_url'])
        tenant_name = context.browser.find_element_by_id("tenant_name")
        tenant_name.send_keys(context.mist_config['CREDENTIALS']['OPENSTACK']['tenant_name'])
    elif "RACKSPACE" in cloud:
        context.execute_steps(u'''
            Then I open the "Region *" drop down
            And I wait for 1 seconds
            When I click the button "%s" in the "Region *" dropdown
        ''' % context.mist_config['CREDENTIALS']['RACKSPACE']['region'])
        cloud_add = context.browser.find_element_by_class_name("cloud-add")
        title = cloud_add.find_element_by_id("title").find_element_by_id('input')
        for i in range(20):
            title.send_keys(u'\ue003')
        title.send_keys("Rackspace")
        username = cloud_add.find_element_by_id("username").find_element_by_id('input')
        username.send_keys(context.mist_config['CREDENTIALS']['RACKSPACE']['username'])
        api_key = cloud_add.find_element_by_id("api_key").find_element_by_id('input')
        api_key.send_keys(context.mist_config['CREDENTIALS']['RACKSPACE']['api_key'])
    elif "SOFTLAYER" in cloud:
        username = context.browser.find_element_by_xpath("//label[contains(text(), 'Username')]").find_element_by_xpath("..").find_element_by_tag_name("input")
        username.send_keys(context.mist_config['CREDENTIALS']['SOFTLAYER']['username'])
        api_key = context.browser.find_element_by_xpath("//label[contains(text(), 'API Key')]").find_element_by_xpath("..").find_element_by_tag_name("input")
        api_key.send_keys(context.mist_config['CREDENTIALS']['SOFTLAYER']['api_key'])
    elif "EC2" in cloud:
        context.execute_steps(u'''
        When I click the button "Select Region"
        And I click the button "%s"''' % context.mist_config['CREDENTIALS']['EC2']['region'])
        title = context.browser.find_element_by_id("title")
        for i in range(20):
            title.send_keys(u'\ue003')
        title.send_keys("EC2")
        api_key = context.browser.find_element_by_id("api_key")
        api_key.send_keys(context.mist_config['CREDENTIALS']['EC2']['api_key'])
        api_secret = context.browser.find_element_by_id("api_secret")
        api_secret.send_keys(context.mist_config['CREDENTIALS']['EC2']['api_secret'])
    elif "NEPHOSCALE" in cloud:
        username = context.browser.find_element_by_xpath("//label[contains(text(), 'Username')]").find_element_by_xpath("..").find_element_by_tag_name("input")
        username.send_keys(context.mist_config['CREDENTIALS']['NEPHOSCALE']['username'])
        password =  context.browser.find_element_by_xpath("//label[contains(text(), 'Password')]").find_element_by_xpath("..").find_element_by_tag_name("input")
        password.send_keys(context.mist_config['CREDENTIALS']['NEPHOSCALE']['password'])
    elif "LINODE" in cloud:
        api_key = context.browser.find_element_by_id("api_key")
        api_key.send_keys(context.mist_config['CREDENTIALS']['LINODE']['api_key'])
    elif "DOCKER" in cloud:
        host = context.browser.find_element_by_id("docker_host")
        host.send_keys(context.mist_config['CREDENTIALS']['DOCKER']['host'])
        port = context.browser.find_element_by_id("docker_port")
        for i in range(6):
            port.send_keys(u'\ue003')
        port.send_keys(context.mist_config['CREDENTIALS']['DOCKER']['port'])
        if context.mist_config['CREDENTIALS']['DOCKER']['key_pem'] or \
           context.mist_config['CREDENTIALS']['DOCKER']['cert_pem']:
            advanced_button = context.browser.find_element_by_class_name("ui-slider-handle")
            advanced_button.click()
            sleep(1)
            key_file = context.browser.find_element_by_id("key_file")
            key_file.click()
            key_upload = context.browser.find_element_by_id("upload-area")
            key_upload.send_keys(context.mist_config['CREDENTIALS']['DOCKER']['key_pem'])
            sleep(1)
            if context.mist_config['CREDENTIALS']['DOCKER']['key_pem']:
                file_upload_ok = context.browser.find_element_by_id("file-upload-ok")
                file_upload_ok.click()
                sleep(2)
            else:
                cancel = context.browser.find_element_by_class("close")
                cancel.click()
                sleep(1)
            cert_file = context.browser.find_element_by_id("cert_file")
            cert_file.click()
            cert_upload = context.browser.find_element_by_id("upload-area")
            cert_upload.send_keys(context.mist_config['CREDENTIALS']['DOCKER']['cert_pem'])
            sleep(1)
            if context.mist_config['CREDENTIALS']['DOCKER']['cert_pem']:
                file_upload_ok = context.browser.find_element_by_id("file-upload-ok")
                file_upload_ok.click()
                sleep(2)
            else:
                cancel = context.browser.find_element_by_class("close")
                cancel.click()
                sleep(1)
        else:
            # in case key/cert are missing
            # and basic authentication is to be configured
            username = context.browser.find_element_by_id("auth_user")
            username.send_keys(context.mist_config['CREDENTIALS']['DOCKER']['username'])
            password = context.browser.find_element_by_id("auth_password")
            password.send_keys(context.mist_config['CREDENTIALS']['DOCKER']['password'])
    elif "DIGITALOCEAN" in cloud:
        token_input = context.browser.find_element_by_xpath("//label[contains(text(), 'Token')]").find_element_by_xpath("..").find_element_by_tag_name("input")
        token_input.send_keys(context.mist_config['CREDENTIALS']['DIGITALOCEAN']['token'])
    elif "VMWARE VCLOUD" in cloud:
        username = context.browser.find_element_by_id("username")
        username.send_keys(context.mist_config['CREDENTIALS']['VMWARE VCLOUD']['username'])
        password = context.browser.find_element_by_id("password")
        password.send_keys(context.mist_config['CREDENTIALS']['VMWARE VCLOUD']['password'])
        organization = context.browser.find_element_by_id("organization")
        organization.send_keys(context.mist_config['CREDENTIALS']['VMWARE VCLOUD']['organization'])
        host = context.browser.find_element_by_id("host")
        host.send_keys(context.mist_config['CREDENTIALS']['VMWARE VCLOUD']['host'])
    elif "INDONESIAN" in cloud:
        username = context.browser.find_element_by_id("username")
        username.send_keys(context.mist_config['CREDENTIALS']['INDONESIAN']['username'])
        password = context.browser.find_element_by_id("password")
        password.send_keys(context.mist_config['CREDENTIALS']['INDONESIAN']['password'])
        organization = context.browser.find_element_by_id("organization")
        organization.send_keys(context.mist_config['CREDENTIALS']['INDONESIAN']['organization'])
    elif "KVM (via libvirt)" in cloud:
        title = context.browser.find_element_by_id("title")
        for i in range(20):
            title.send_keys(u'\ue003')
        title.send_keys("KVM (via libvirt)")
        hostname = context.browser.find_element_by_id("machine_hostname")
        hostname.send_keys(context.mist_config['CREDENTIALS']['KVM']['hostname'])

        context.execute_steps(u'''
            When I click the "Select SSH Key" button inside the "Add Cloud" panel
            When I click the "Add Key" button inside the "Add Cloud" panel
            Then I expect for "key-add-popup" popup to appear within max 4 seconds
            When I fill "KVM Key" as key name
        ''')

        upload = context.browser.find_element_by_id("key-add-upload")
        upload.send_keys(context.mist_config['CREDENTIALS']['KVM']['key_path'])
        sleep(1)

        context.execute_steps(u'''
            When I click the "Add" button inside the "Add key" popup
            Then I expect for "key-add-popup" popup to disappear within max 4 seconds
        ''')
    elif "PACKET" in cloud:
        # cloud_add = context.browser.find_element_by_class_name("cloud-add")
        cloud_add = context.browser.find_element_by_css_selector("#content.cloud-add")
        api_key = filter(lambda el: el.is_displayed(),
                         cloud_add.find_elements_by_id("api_key"))[0].find_element_by_id("input")
        wait_until_visible(api_key, 4)
        clear_input_and_send_keys(api_key,
                                  context.mist_config['CREDENTIALS']['PACKET']['api_key'])


def find_cloud(context, cloud_title):
    clouds = context.browser.find_elements_by_tag_name('cloud-chip')
    clouds = filter(lambda el: el.is_displayed(), clouds)
    for c in clouds:
        try:
            title = c.find_element_by_class_name('cloud-title')
            if safe_get_element_text(title).lower().strip() == cloud_title:
                return c
        except NoSuchElementException, StaleElementReferenceException:
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
        When I click the mist.io button
        When I click the button by "addBtn" id_name
        Then I expect the page Clouds to be visible within max 10 seconds
        And I open the "Choose Provider" drop down
        And I wait for 1 seconds
        When I click the button "%s" in the "Choose Provider" dropdown
        Then I expect the label "Title *" to be visible within max 4 seconds
        When I use my provider "%s" credentials
        And I click the button "Add Cloud"
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
    seconds = 4
    end_time = time() + seconds
    while time() < end_time:
        cloud = find_cloud(context, provider.lower())
        cloud_menu = find_cloud_info(context, provider.lower())
        if not cloud and not cloud_menu:
            return True
        sleep(1)
    assert False, u'%s cloud had not been deleted after %s seconds' \
                  % (provider, seconds)


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


@step(u'I ensure "{title}" cloud is enabled')
def ensure_cloud_enabled(context, title):
    cloud = find_cloud(context, title.lower())
    assert cloud, "Cloud %s has not been added" % title
    return 'offline' in cloud.get_attibute('class')
