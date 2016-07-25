from behave import step

from time import time
from time import sleep

from .utils import safe_get_element_text

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


@step(u'"{expected_name}" {resource_type} should be present within {seconds}'
      u' seconds')
def wait_for_item_show(context, expected_name, resource_type, seconds):
    resource_type = resource_type.lower()
    expected_name = expected_name.lower()
    if resource_type not in ['machine', 'image', 'key', 'network',
                             'tunnel', 'script', 'template', 'stack',
                             'team']:
        raise ValueError('The resource type given is unknown')
    selector = 'page-items.%ss' % resource_type
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            list_of_items = context.browser.find_element_by_css_selector(selector)
            if list_of_items.is_displayed():
                items = list_of_items.find_elements_by_tag_name('list-item')
                for item in items:
                    name = safe_get_element_text(item.find_element_by_css_selector('div.name')).strip().lower()
                    if expected_name == name:
                        return True
        except NoSuchElementException, StaleElementReferenceException:
            pass
        sleep(1)
    assert False, 'Item has not appeared in the list after %s seconds' % seconds

