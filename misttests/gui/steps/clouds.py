import json

from behave import step

from misttests.config import safe_get_var
from time import time
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from .utils import safe_get_element_text

from .forms import set_value_to_field
from .forms import clear_input_and_send_keys

from .buttons import clicketi_click
from .buttons import click_button_from_collection


def set_azure_creds(context):
    subscription_id = safe_get_var('clouds/azure', 'subscription_id', context.mist_config['CREDENTIALS']['AZURE']['subscription_id'])
    certificate = safe_get_var('clouds/azure', 'certificate', context.mist_config['CREDENTIALS']['AZURE']['certificate'])
    context.execute_steps(u'''
            Then I set the value "Azure" to field "Title" in "cloud" add form
            And I set the value "%s" to field "Subscription ID" in "cloud" add form
            ''' % subscription_id)
    set_value_to_field(context, certificate, 'certificate', 'cloud', 'add')
    sleep(3)


def set_gce_creds(context):
    project_id = safe_get_var('clouds/gce/mist-dev', 'project_id', context.mist_config['CREDENTIALS']['GCE']['project_id'])
    private_key = safe_get_var('clouds/gce/mist-dev', 'private_key', context.mist_config['CREDENTIALS']['GCE']['private_key'])
    context.execute_steps(u'''
            Then I set the value "%s" to field "Title" in "cloud" add form
            Then I set the value "%s" to field "Project ID" in "cloud" add form
            Then I set the value "%s" to field "Private Key" in "cloud" add form
            And I click the "Enable DNS support" button with id "dns_enabled"
        ''' % ('GCE', project_id, json.dumps(private_key)))


def set_rackspace_creds(context):
    region = safe_get_var('clouds/rackspace', 'region', context.mist_config['CREDENTIALS']['RACKSPACE']['region'])
    username = safe_get_var('clouds/rackspace', 'username', context.mist_config['CREDENTIALS']['RACKSPACE']['username'])
    api_key = safe_get_var('clouds/rackspace', 'api_key', context.mist_config['CREDENTIALS']['RACKSPACE']['api_key'])
    context.execute_steps(u'''
        Then I open the "Region" drop down
        And I wait for 1 seconds
        When I click the button "%s" in the "Region" dropdown
        Then I set the value "Rackspace" to field "Title" in "cloud" add form
        Then I set the value "%s" to field "Username" in "cloud" add form
        Then I set the value "%s" to field "API Key" in "cloud" add form
    ''' % (region, username, api_key))


def set_softlayer_creds(context):
    username = safe_get_var('clouds/softlayer', 'username', context.mist_config['CREDENTIALS']['SOFTLAYER']['username'])
    api_key = safe_get_var('clouds/softlayer', 'api_key', context.mist_config['CREDENTIALS']['SOFTLAYER']['api_key'])
    context.execute_steps(u'''
        Then I set the value "%s" to field "Username" in "cloud" add form
        Then I set the value "%s" to field "API Key" in "cloud" add form
    ''' % (username, api_key))


def set_aws_creds(context):
    api_key = safe_get_var('clouds/aws', 'api_key', context.mist_config['CREDENTIALS']['EC2']['api_key'])
    api_secret = safe_get_var('clouds/aws', 'api_secret', context.mist_config['CREDENTIALS']['EC2']['api_secret'])
    region = safe_get_var('clouds/aws', 'region', context.mist_config['CREDENTIALS']['EC2']['region'])
    context.execute_steps(u'''
        Then I open the "Region" drop down
        And I wait for 1 seconds
        When I click the button "%s" in the "Region" dropdown
        And I wait for 1 seconds
        Then I set the value "AWS" to field "Title" in "cloud" add form
        And I set the value "%s" to field "API Key" in "cloud" add form
        And I set the value "%s" to field "API Secret" in "cloud" add form
    ''' % (region, api_key, api_secret))


def set_nepho_creds(context):
    username = safe_get_var('clouds/nephoscale', 'username', context.mist_config['CREDENTIALS']['NEPHOSCALE']['username'])
    password = safe_get_var('clouds/nephoscale', 'password', context.mist_config['CREDENTIALS']['NEPHOSCALE']['password'])
    context.execute_steps(u'''
            Then I set the value "%s" to field "Username" in "cloud" add form
            Then I set the value "%s" to field "Password" in "cloud" add form
        ''' % (username, password))


def set_linode_creds(context):
    api_key = safe_get_var('clouds/linode', 'api_key', context.mist_config['CREDENTIALS']['LINODE']['api_key'])
    context.execute_steps(u'Then I set the value "%s" to field "API Key" in'
                          u' "cloud" add form' % api_key)


def set_do_creds(context):
    token = safe_get_var('clouds/digitalocean', 'token', context.mist_config['CREDENTIALS']['DIGITALOCEAN']['token'])
    context.execute_steps(u'Then I set the value "%s" to field "Token" in '
                          u'"cloud" add form' % token)


def set_docker_orchestrator_creds(context):
    host = safe_get_var('clouds/docker_orchestrator', 'host', context.mist_config['CREDENTIALS']['DOCKER_ORCHESTRATOR']['host'])
    port = safe_get_var('clouds/docker_orchestrator', 'port', context.mist_config['CREDENTIALS']['DOCKER_ORCHESTRATOR']['port'])
    context.execute_steps(u'''
                Then I set the value "Docker_Orchestrator" to field "Title" in "cloud" add form
                Then I set the value "%s" to field "Host" in "cloud" add form
                Then I set the value "%s" to field "Port" in "cloud" add form
            ''' % (host, port))

def set_docker_creds(context):
    if context.mist_config['LOCAL']:
        host = context.mist_config['LOCAL_DOCKER']
        port = '2375'
        context.execute_steps(u'''
                Then I set the value "Docker" to field "Title" in "cloud" add form
                Then I set the value "%s" to field "Host" in "cloud" add form
                Then I set the value "%s" to field "Port" in "cloud" add form
        ''' % (host, port))
    else:
        host = safe_get_var('dockerhosts/godzilla', 'host', context.mist_config['CREDENTIALS']['DOCKER']['host'])
        authentication = safe_get_var('dockerhosts/godzilla', 'authentication', context.mist_config['CREDENTIALS']['DOCKER']['authentication'])
        port = safe_get_var('dockerhosts/godzilla', 'port', context.mist_config['CREDENTIALS']['DOCKER']['port'])
        context.execute_steps(u'''
                Then I set the value "Docker" to field "Title" in "cloud" add form
                Then I set the value "%s" to field "Host" in "cloud" add form
                Then I set the value "%s" to field "Port" in "cloud" add form
                Then I open the "Authentication" drop down
                And I wait for 1 seconds
                When I click the button "%s" in the "Authentication" dropdown
            ''' % (host, port, authentication))

        certificate = safe_get_var('dockerhosts/godzilla', 'cert', context.mist_config['CREDENTIALS']['DOCKER']['cert'])
        key = safe_get_var('dockerhosts/godzilla', 'key', context.mist_config['CREDENTIALS']['DOCKER']['key'])
        ca = safe_get_var('dockerhosts/godzilla', 'ca', context.mist_config['CREDENTIALS']['DOCKER']['ca'])

        set_value_to_field(context, key, 'key', 'cloud', 'add')
        set_value_to_field(context, certificate, 'certificate', 'cloud', 'add')
        set_value_to_field(context, ca, 'ca certificate', 'cloud', 'add')


def set_packet_creds(context):
    api_key = safe_get_var('clouds/packet', 'api_key', context.mist_config['CREDENTIALS']['PACKET']['api_key'])
    context.execute_steps(u'Then I set the value "%s" to field "API Key" in '
                          u'"cloud" add form' % api_key)


def set_openstack_creds(context):
    context.execute_steps(u'''
            Then I set the value "OpenStack" to field "Title" in "cloud" add form
            Then I set the value "%s" to field "Username" in "cloud" add form
            Then I set the value "%s" to field "Password" in "cloud" add form
            Then I set the value "%s" to field "Auth Url" in "cloud" add form
            Then I set the value "%s" to field "Tenant Name" in "cloud" add form
        ''' % (safe_get_var('clouds/openstack', 'username', context.mist_config['CREDENTIALS']['OPENSTACK']['username']),
               safe_get_var('clouds/openstack', 'password', context.mist_config['CREDENTIALS']['OPENSTACK']['password']),
               safe_get_var('clouds/openstack', 'auth_url', context.mist_config['CREDENTIALS']['OPENSTACK']['auth_url']),
               safe_get_var('clouds/openstack', 'tenant', context.mist_config['CREDENTIALS']['OPENSTACK']['tenant']),))


def set_hostvirtual_creds(context):
    api_key = safe_get_var('clouds/hostvirtual', 'api_key', context.mist_config['CREDENTIALS']['HOSTVIRTUAL']['api_key'])
    context.execute_steps(u'Then I set the value "%s" to field "API Key" in '
                          u'"cloud" add form' % api_key)


def set_vultr_creds(context):
    api_key = safe_get_var('clouds/vultr', 'apikey', context.mist_config['CREDENTIALS']['VULTR']['apikey'])
    context.execute_steps(u'Then I set the value "%s" to field "API Key" in '
                          u'"cloud" add form' % api_key)


def set_azure_arm_creds(context):
    context.execute_steps(u'''
                    Then I set the value "Azure ARM" to field "Title" in "cloud" add form
                    Then I set the value "%s" to field "Tenant ID" in "cloud" add form
                    Then I set the value "%s" to field "Subscription ID" in "cloud" add form
                    Then I set the value "%s" to field "Client Key" in "cloud" add form
                    Then I set the value "%s" to field "Client Secret" in "cloud" add form
                ''' % (safe_get_var('clouds/azure_arm', 'tenant_id', context.mist_config['CREDENTIALS']['AZURE_ARM']['tenant_id']),
                       safe_get_var('clouds/azure_arm', 'subscription_id', context.mist_config['CREDENTIALS']['AZURE_ARM']['subscription_id']),
                       safe_get_var('clouds/azure_arm', 'client_key', context.mist_config['CREDENTIALS']['AZURE_ARM']['client_key']),
                       safe_get_var('clouds/azure_arm', 'client_secret', context.mist_config['CREDENTIALS']['AZURE_ARM']['client_secret']),))


def set_kvm_creds(context):
    context.execute_steps(u'''
                    Then I set the value "KVM" to field "Title" in "cloud" add form
                    Then I set the value "%s" to field "KVM hostname" in "cloud" add form
                    And I wait for 1 seconds
                    And I open the "SSH Key" drop down
                    And I wait for 2 seconds
                    And I click the button "KVMKEY" in the "SSH Key" dropdown
                '''% (safe_get_var('clouds/other_server', 'hostname', context.mist_config['CREDENTIALS']['KVM']['hostname']),))


def set_other_server_creds(context):
    context.execute_steps(u'''
                    Then I set the value "Bare Metal" to field "Title" in "cloud" add form
                    Then I set the value "%s" to field "Hostname" in "cloud" add form
                    And I wait for 1 seconds
                    And I open the "SSH Key" drop down
                    And I wait for 2 seconds
                    And I click the button "KVMKEY" in the "SSH Key" dropdown
                    And I wait for 1 seconds
                    Then I set the value "user" to field "User" in "cloud" add form
                ''' % (safe_get_var('clouds/other_server', 'hostname', context.mist_config['CREDENTIALS']['KVM']['hostname']),))


def set_vmware_creds(context):
    context.execute_steps(u'''
                Then I set the value "VmWare" to field "Title" in "cloud" add form
                Then I set the value "%s" to field "Username" in "cloud" add form
                Then I set the value "%s" to field "Password" in "cloud" add form
                Then I set the value "%s" to field "Organization" in "cloud" add form
                Then I set the value "%s" to field "Hostname" in "cloud" add form
            ''' % (safe_get_var('clouds/vmware', 'username', context.mist_config['CREDENTIALS']['VMWARE']['username']),
                   safe_get_var('clouds/vmware', 'password', context.mist_config['CREDENTIALS']['VMWARE']['password']),
                   safe_get_var('clouds/vmware', 'organization', context.mist_config['CREDENTIALS']['VMWARE']['organization']),
                   safe_get_var('clouds/vmware', 'host', context.mist_config['CREDENTIALS']['VMWARE']['host']),))


def set_onapp_creds(context):
    context.execute_steps(u'''
                Then I set the value "%s" to field "Username" in "cloud" add form
                Then I set the value "%s" to field "Password" in "cloud" add form
                Then I set the value "%s" to field "Host" in "cloud" add form
                And I click the "Verify SSL certificate" button with id "verify"
            ''' % (safe_get_var('clouds/onapp', 'username', context.mist_config['CREDENTIALS']['ONAPP']['username']),
                   safe_get_var('clouds/onapp', 'password', context.mist_config['CREDENTIALS']['ONAPP']['password']),
                   safe_get_var('clouds/onapp', 'host', context.mist_config['CREDENTIALS']['ONAPP']['host']),))


def set_second_packet_creds(context):
    api_key = safe_get_var('clouds/packet_2', 'api_key', context.mist_config['CREDENTIALS']['PACKET_2']['api_key'])
    context.execute_steps(u'Then I set the value "%s" to field "API Key" in '
                          u'"cloud" edit form' % api_key)


def set_second_openstack_creds(context):
    context.execute_steps(u'''
                Then I set the value "%s" to field "Username" in "cloud" edit form
                Then I set the value "%s" to field "Password" in "cloud" edit form
                Then I set the value "%s" to field "Auth Url" in "cloud" edit form
                Then I set the value "%s" to field "Tenant Name" in "cloud" edit form
            ''' % (safe_get_var('clouds/openstack_2', 'username', context.mist_config['CREDENTIALS']['OPENSTACK_2']['username']),
                   safe_get_var('clouds/openstack', 'password', context.mist_config['CREDENTIALS']['OPENSTACK_2']['password']),
                   safe_get_var('clouds/openstack', 'auth_url', context.mist_config['CREDENTIALS']['OPENSTACK_2']['auth_url']),
                   safe_get_var('clouds/openstack_2', 'tenant', context.mist_config['CREDENTIALS']['OPENSTACK_2']['tenant']),))


cloud_creds_dict = {
    "azure": set_azure_creds,
    "gce": set_gce_creds,
    "rackspace": set_rackspace_creds,
    "softlayer": set_softlayer_creds,
    "aws": set_aws_creds,
    "nephoscale": set_nepho_creds,
    "linode": set_linode_creds,
    "digital ocean": set_do_creds,
    "docker": set_docker_creds,
    "packet": set_packet_creds,
    "openstack": set_openstack_creds,
    "hostvirtual": set_hostvirtual_creds,
    "vultr": set_vultr_creds,
    "azure arm": set_azure_arm_creds,
    "kvm (via libvirt)": set_kvm_creds,
    "other server": set_other_server_creds,
    "vmware": set_vmware_creds,
    "docker_orchestrator": set_docker_orchestrator_creds,
    "onapp": set_onapp_creds
}


cloud_second_creds_dict = {
    "packet": set_second_packet_creds,
    "openstack": set_second_openstack_creds
}


@step(u'I select the "{provider}" provider')
def select_provider_in_cloud_add_form(context, provider):
    provider_title = provider.lower()
    clouds_class = context.browser.find_element_by_class_name('providers')
    clouds = clouds_class.find_elements_by_tag_name('paper-item')
    for c in clouds:
            if safe_get_element_text(c).lower().strip() == provider_title:
                clicketi_click(context, c)
                return


@step(u'I use my "{provider}" credentials')
def cloud_creds(context, provider):
    provider = provider.strip().lower()
    if provider not in cloud_creds_dict.keys():
        raise Exception("Unknown cloud provider")
    cloud_creds_dict.get(provider)(context)


@step(u'I use my second "{provider}" credentials in cloud edit form')
def cloud_second_creds(context, provider):
    provider = provider.strip().lower()
    if provider not in cloud_second_creds_dict.keys():
        raise Exception("Unknown cloud provider")
    cloud_second_creds_dict.get(provider)(context)


@step(u'I should have {clouds} clouds added')
def check_error_message(context, clouds):
    cloud_chips = context.browser.find_elements_by_tag_name('cloud-chip')
    if len(cloud_chips) == int(clouds):
        return
    else:
        assert False, "There are %s clouds added, not %s"%(len(cloud_chips),clouds)


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
    end_time = time() + 10
    while time() < end_time:
        if find_cloud(context, cloud.lower()):
            return True
        sleep(2)


    context.execute_steps(u'''
        When I click the "new cloud" button with id "addBtn"
        Then I expect the "Cloud" add form to be visible within max 5 seconds''')

    if 'docker_orchestrator' in cloud.lower():
        cloud_type = 'docker'
    else:
        cloud_type = cloud

    context.execute_steps(u'''When I select the "%s" provider''' % cloud_type)

    context.execute_steps('''
        Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
        When I use my "%s" credentials
        And I focus on the button "Add Cloud" in "cloud" add form
        Then I click the button "Add Cloud" in "cloud" add form
        When I wait for the dashboard to load
        And I scroll the clouds list into view
        Then the "%s" provider should be added within 120 seconds
    ''' % (cloud, cloud))


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


@step(u'I add the key needed for Other Server')
def add_key_for_provider(context):

    context.execute_steps(u'''
        When I visit the Keys page
        When I click the button "+"
        Then I expect the "Key" add form to be visible within max 10 seconds
        When I set the value "KVMKey" to field "Name" in "key" add form
    ''')

    key = safe_get_var('clouds/other_server', 'key', context.mist_config['CREDENTIALS']['KVM']['key'])
    set_value_to_field(context, key, 'Private Key', 'key', 'add')

    context.execute_steps(u'''
        When I expect for the button "Add" in "key" add form to be clickable within 9 seconds
        And I focus on the button "Add" in "key" add form
        And I click the button "Add" in "key" add form
        Then I expect the "key" edit form to be visible within max 7 seconds
        And I visit the Home page
        When I visit the Keys page
        Then "KVMKey" key should be present within 15 seconds
        Then I visit the Home page
        When I wait for the dashboard to load
    ''')
