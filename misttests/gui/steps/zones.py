from behave import step
from behave import given

from random import randrange
from time import sleep

@step(u'I fill in a "{name}" zone name')
def fill_zone_mame(context, name):
    """
    This step will create a random zone name and a suitable name and will update the context.
    """
    if 'random' in name or context.mist_config.get(name):
        if not context.mist_config.get(name):
            if 'random ' in name:
                name = name.lstrip('random ')
            zone_name = context.mist_config[name] = "testlikeapro%s" % randrange(10000)
        else:
            zone_name = context.mist_config[name]
    else:
        zone_name = name
    container = context.browser.find_element_by_tag_name("zone-add")
    textfield = container.find_element_by_id("input")
    textfield.send_keys(zone_name)
    sleep(1)
