from behave import step

from selenium.common.exceptions import NoSuchElementException


@step(u'there should be {subnets} subnets visible in single network page')
def find_subnets_in_single_network_page(context, subnets):
    import ipdb; ipdb.set_trace()
    visible_subnets = context.browser.find_elements_by_tag_name('subnet-item')
    assert int(subnets) == len(visible_subnets), "There are %s visible subnets, but there should be %s" \
                    % (len(visible_subnets), len(subnets))
