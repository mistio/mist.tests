import json

from behave import *

from time import time
from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@step(u'I refresh the page')
def refresh_page(context):
    context.browser.get(context.mist_config['MIST_URL'])

@step(u'I click the Add provider button')
def click_polymer_button(context):
    container = context.browser.find_element_by_xpath("//div[contains(@class, 'cloud-add')]")
    button = container.find_element_by_tag_name('paper-button')
    ActionChains(context.browser).move_to_element(button).click().perform()


@step(u'I open the Provider drop down')
def open_provider_drop_down(context):
    button = context.browser.find_element_by_xpath("//*[contains(text(), 'Choose Provider')]")
    ActionChains(context.browser).move_to_element(button).click().perform()


@step(u'I click the provider button {provider}')
def open_provider_drop_down(context, provider):
    button = context.browser.find_element_by_xpath('//span[contains(text(), "%s")]' %str(provider))
    ActionChains(context.browser).move_to_element(button).click().perform()


@step(u'I expect for "{element_text}" label to be visible within max {seconds} '
      u'seconds')
def element_label_become_visible_waiting_with_timeout(context, element_text, seconds):
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            context.browser.find_element_by_xpath('//label[contains(text(), "%s")]' %str(element_text))
            return
        except:
            pass
        assert time() + 1 < timeout, "label %s did not " \
                                     "become visible after %s seconds" % \
                                     (element_text, seconds)
        sleep(1)


@step(u'the "{cloud}" provider should be added within {seconds} seconds')
def cloud_added(context, cloud, seconds):
    end_time = time() + int(seconds)
    while time() < end_time:
        try:
            button = context.browser.find_element_by_xpath('//h1[contains(text(), "%s")]' %str(cloud))
            if button:
                return
        except:
            pass
        sleep(2)

    assert False, u'%s is not added within %s seconds' %(cloud, seconds)


@step(u'I expect for "{element_name}" element to be visible within max {seconds} '
      u'seconds')
def element_become_visible_waiting_with_timeout(context, element_name, seconds):
    try:
        WebDriverWait(context.browser, int(seconds)).until(EC.visibility_of_element_located((By.TAG_NAME, element_name)))
    except TimeoutException:
        raise TimeoutException("element %s did not become visible "
                               "after %s seconds" % (element_name, seconds))


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
        When I click the button "Select Region"
        And I click the button "%s"''' % context.mist_config['CREDENTIALS']['RACKSPACE']['region'])
        title = context.browser.find_element_by_id("title")
        for i in range(20):
            title.send_keys(u'\ue003')
        title.send_keys("Rackspace")
        username = context.browser.find_element_by_id("username")
        username.send_keys(context.mist_config['CREDENTIALS']['RACKSPACE']['username'])
        api_key = context.browser.find_element_by_id("api_key")
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
        api_key = context.browser.find_element_by_xpath("//label[contains(text(), 'API Key')]").find_element_by_xpath("..").find_element_by_tag_name("input")
        api_key.send_keys(context.mist_config['CREDENTIALS']['PACKET']['api_key'])
