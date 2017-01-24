from behave import step

from time import time
from time import sleep

from .utils import safe_get_element_text

import logging

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def find_starred_images(images_list):
    starred_images = []
    for image in images_list:
        try:
            starred_image = image.find_element_by_class_name('star')
            starred_images.append(starred_image)
        except:
            pass
    return starred_images


def find_image(image, images_list):
    for check_image in images_list:
        if image in safe_get_element_text(check_image):
            return check_image.find_element_by_tag_name('list-item')


@step(u'the "{image}" image should be "{state}" within {seconds} seconds')
def assert_starred_unstarred_image(context,image,state,seconds):
    state = state.lower()
    if state not in ['starred', 'unstarred']:
        raise Exception('Unknown type of state')
    images = context.browser.find_element_by_tag_name('item-list').find_element_by_tag_name('iron-list')
    images_list = images.find_element_by_id("items").find_elements_by_class_name("row")
    end_time = time() + int(seconds)
    image_to_check_state= find_image(image, images_list)
    while time() < end_time:
        starred_images = find_starred_images(images_list)
        if state == 'starred':
            log.info(len(starred_images))
            if image_to_check_state in starred_images:
                return
        elif state == 'unstarred':
            log.info(len(starred_images))
            if image_to_check_state not in starred_images:
                return
    assert False, 'Image %s is not %s in the list after %s seconds' \
                  % (image, state, seconds)


@step(u'I star the "{text}" image')
def star_image(context, text):
    images_list = context.browser.find_element_by_id("items")
    images = images_list.find_elements_by_class_name("row")
    for image in images:
        if text in safe_get_element_text(image):
            star_button = image.find_element_by_class_name("ui-checkbox")
            star_button.click()
            image = image.find_element_by_tag_name('h3')
            context.mist_config['the_image_name_i_starred'] = safe_get_element_text(image)
            return


def scroll_down_and_wait(context, wait_for_unstarred_images=False, wait=5):
    """
    Wait for a few seconds until new images are loaded
    :return: True if new images have been loaded, False otherwise
    """
    previous_scroll_height = context.browser.find_elements_by_class_name('checkbox-link')[-1].location['y']
    context.browser.execute_script("window.scrollTo(0, %s)"
                                   % previous_scroll_height)
    end_time = time() + wait
    while time() < end_time:
        sleep(1)
        last_image = context.browser.find_elements_by_class_name('checkbox-link')[-1]
        scroll_height = last_image.location['y']
        if previous_scroll_height != scroll_height:
            if not wait_for_unstarred_images and 'staroff' in last_image.get_attribute('class'):
                return False
            return True

    return False
