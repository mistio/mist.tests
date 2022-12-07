from behave import step

from selenium.webdriver.common.by import By

from time import time

from misttests.integration.gui.steps.utils import safe_get_element_text
from misttests.integration.gui.steps.utils import get_page_element
from misttests.integration.gui.steps.utils import expand_shadow_root
from misttests.integration.gui.steps.utils import get_list_filtered_items


def find_image(image, images_list):
    for check_image in images_list:
        if image in safe_get_element_text(check_image):
            return check_image.find_element(By.CSS_SELECTOR, 'strong.name')


@step('the "{image}" image should be "{state}" within {seconds} seconds')
def assert_starred_unstarred_image(context, image, state, seconds):
    state = state.lower()
    if state not in ['starred', 'unstarred']:
        raise Exception('Unknown type of state')
    images_page = get_page_element(context, 'images')
    images_page_shadow = expand_shadow_root(context, images_page)
    mist_list = images_page_shadow.find_element(By.CSS_SELECTOR, 'mist-list')
    end_time = time() + int(seconds)
    while time() < end_time:
        starred = get_list_filtered_items(context, mist_list)[0]['starred']
        if state == 'starred':
            assert starred, "Image is not starred"
        else:
            assert not starred, "Image is starred"
        return
    assert False, 'Image %s is not %s in the list after %s seconds' \
                  % (image, state, seconds)
