from behave import step

from time import time
from time import sleep


@step(u'I expect the domain "{name}" to be populated within {seconds} seconds')
def domain_populated(context, name, seconds):
    if 'random' in name:
        if context.mist_config.get(name):
            domain_name = context.mist_config.get(name)
        else:
            assert False, "Got a name that contains random but can not find a value in the context"
    else:
        domain_name = name
    end_time = time() + int(seconds)
    while time() < end_time:
        textfield = context.browser.find_element_by_id("domain-name")
        if textfield.text[:-1] == domain_name:
            return
        sleep(1)
    assert False, u'%s domain was not populated after %s' % (name, seconds)
