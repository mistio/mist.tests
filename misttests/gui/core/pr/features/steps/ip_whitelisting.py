from behave import step

from misttests.gui.steps.buttons import clicketi_click
from misttests.gui.steps.forms import clear_input_and_send_keys



@step(u'I remove all whitelisted ips')
def remove_whitelisted_ips(context):
    whitelisted_ips_tag = context.browser.find_element_by_tag_name('multi-inputs')
    whitelisted_ips = whitelisted_ips_tag.find_elements_by_class_name('input')
    for whitelisted_ip in whitelisted_ips:
        remove_btn = whitelisted_ip.find_element_by_class_name('remove')
        clicketi_click(context, remove_btn)
        context.execute_steps(u'''
                    Then I expect the dialog "Remove Cidr" is open within 4 seconds
                    And I click the "Remove Cidr" button in the dialog "Remove Cidr"
                    And I expect the dialog "Remove Cidr" is closed within 4 seconds
                ''')

@step(u'I add the IP "{ip}" as whitelisted')
def add_whitelisted_ip(context,ip):
    import ipdb;ipdb.set_trace()
    whitelisted_ips_tag = context.browser.find_element_by_tag_name('multi-inputs')
    new_whitelisted_ip_field = whitelisted_ips_tag.find_element_by_tag_name('div')
    whitelisted_ip = new_whitelisted_ip_field.find_element_by_tag_name('paper-input')
    input = whitelisted_ip.find_element_by_id('input')
    clear_input_and_send_keys(input, ip)
