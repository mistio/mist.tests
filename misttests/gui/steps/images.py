from behave import step

from time import time
from time import sleep

from .utils import safe_get_element_text


@step(u'an image that contains "{text}" should be starred')
def assert_starred_image(context, text):
    images_list = context.browser.find_element_by_id("image-list")
    images = images_list.find_elements_by_tag_name("li")
    starred_images = filter(lambda li: 'staron' in li.get_attribute('class'), images)
    if context.mist_config.get(text):
        text = context.mist_config[text]
    starred_image = filter(lambda li: text in safe_get_element_text(li).lower(), starred_images)
    assert len(starred_image) == 1, \
        "Could not find starred image with name %s" % text


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


@step(u'I clear the images search bar')
def clear_image_search_bar(context):
    search_bar = context.browser.find_element_by_id("search-term-input")
    for i in range(20):
        search_bar.send_keys(u'\ue003')


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


@step(u'I scroll down until all starred images appear')
def get_all_starred_images(context):
    while scroll_down_and_wait(context):
        pass


@step(u'I scroll down until all images appear')
def get_all_images(context):
    while scroll_down_and_wait(context, wait_for_unstarred_images=True):
        pass
