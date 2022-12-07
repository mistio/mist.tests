from behave import step
from selenium.webdriver.common.by import By

from misttests.integration.gui.steps.utils import get_page_element
from misttests.integration.gui.steps.utils import expand_shadow_root


@step('there should be {subnets} subnets visible in single network page')
def find_subnets_in_single_network_page(context, subnets):
    _, page = get_page_element(context, 'networks', 'network')
    page_shadow = expand_shadow_root(context, page)
    visible_subnets = page_shadow.find_elements(By.CSS_SELECTOR, 'subnet-item')
    assert int(subnets) == len(visible_subnets), \
        "There are %s visible subnets, but there should be %s" % (
            len(visible_subnets), len(subnets))


@step('the cidr of the subnet created should be "{cidr}"')
def find_subnet_cidr(context, cidr):
    _, page = get_page_element(context, 'networks', 'network')
    page_shadow = expand_shadow_root(context, page)
    subnet = page_shadow.find_element(By.CSS_SELECTOR, 'subnet-item')
    assert cidr in subnet.text, "Cidr %s is not visible to the user" % cidr
