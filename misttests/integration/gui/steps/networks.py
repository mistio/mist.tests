from behave import step

from selenium.common.exceptions import NoSuchElementException


@step(u'there should be {subnets} subnets visible in single network page')
def find_subnets_in_single_network_page(context, subnets):
    visible_subnets = context.browser.find_elements_by_tag_name('subnet-item')
    assert int(subnets) == len(visible_subnets), "There are %s visible subnets, but there should be %s" \
                    % (len(visible_subnets), len(subnets))


@step('the cidr of the subnet created should be "{cidr}"')
def find_subnet_cidr(context, cidr):
    subnet = context.browser.find_element_by_tag_name('subnet-item')
    assert cidr in subnet.text, "Cidr %s is not visible to the user" %cidr
