from behave import step

import logging

from time import time
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

@step(u'I wait for "{title}" list page to load')
def wait_for_some_list_page_to_load(context, title):
    if title not in ['Machines', 'Images', 'Keys', 'Networks', 'Scripts',
                     'Account', 'Teams']:
        raise ValueError('The page given is unknown')
    # Wait for the list page to appear
    end_time = time() + 5
    while time() < end_time:
        try:
            context.browser.find_element_by_id('%s-list-page' % title.lower().rpartition(title[-1])[0])
            break
        except NoSuchElementException:
            assert time() + 1 < end_time, "%s list page has not appeared " \
                                          "after 5 seconds" % title.lower()
            sleep(1)

    # this code will stop waiting after 5 seconds if nothing appears otherwise
    # it will stop as soon as a list is loaded
    end_time = time() + 5
    while time() < end_time:
        try:
            list_of_things = context.browser.find_element_by_id('%s-list' % title.lower().rpartition(title[-1])[0])
            lis = list_of_things.find_elements_by_tag_name('li')
            if len(lis) > 0:
                break
        except NoSuchElementException:
            pass
        sleep(1)


def safe_get_element_text(check_element):
    try:
        return check_element.text
    except StaleElementReferenceException:
        return ""


@step(u'I type "{some_text}" in input with id "{element_id}"')
def give_some_input(context, some_text, element_id):
    input_element = context.browser.find_element_by_id(element_id)
    if context.mist_config.get(some_text):
        some_text = context.mist_config[some_text]
    input_element.send_keys(some_text)


def focus_on_element(context, element):
    position = element.location
    context.browser.execute_script("window.scrollTo(0, %s)" % position['y'])


@step(u'I focus on the "{name}" button')
def focus_on_add_rule(context, name):
    if context.mist_config.get(name):
        name = context.mist_config[name]
    if "Add Rule" in name:
        button = context.browser.find_element_by_id("add-rule-button")
        focus_on_element(context, button)
    elif "Add Graph" in name:
        button = context.browser.find_element_by_id("add-metric-btn")
        focus_on_element(context, button)
    return


@step(u'I wait for {seconds} seconds')
def wait(context, seconds):
    sleep(int(seconds))


@step(u'I refresh the current page')
def refresh_the_page(context):
    context.browser.refresh()


@step(u'the title should be "{text}"')
def assert_title_is(context, text):
    assert text == context.browser.title


@step(u'the title should contain "{text}"')
def assert_title_contains(context, text):
    assert text in context.browser.title


@step(u'I wait for the links in homepage to appear')
def wait_for_buttons_to_appear(context):
    end_time = time() + 10
    while time() < end_time:
        try:
            images_button = context.browser.find_element_by_id('images')
            counter_span = images_button.find_element_by_class_name('count')
            int(safe_get_element_text(counter_span))
            break
        except (NoSuchElementException, ValueError, AttributeError):
            assert time() + 1 < end_time, "Links in the home page have not" \
                                          " appeared after 10 seconds"
            sleep(1)


@step(u'{counter_title} counter should be greater than {counter_number} within '
      u'{seconds} seconds')
def some_counter_loaded(context, counter_title, counter_number, seconds):
    from .buttons import search_for_button
    counter_found = search_for_button(context, counter_title)
    assert counter_found, "Counter with name %s has not been found" % counter_title

    end_time = time() + int(seconds)
    while time() < end_time:
        counter_span = counter_found.find_element_by_class_name("ui-li-count")
        counter_span_text = safe_get_element_text(counter_span)
        counter = int(counter_span_text)

        if counter > int(counter_number):
            return
        else:
            sleep(2)

    assert False, 'The counter did not say that more than %s images were ' \
                  'loaded' % counter_number


@step(u'I should see a header with title "{text}"')
def see_header_with_title(context, text):
    titles = context.browser.find_elements_by_class_name("ui-title")
    for title in titles:
        title_text = safe_get_element_text(title)
        if text in title_text:
            return

    assert False, u'Could not find title with text %s in the page' % text


@step(u'I expect for "{element_id}" to be visible within max {seconds} '
      u'seconds')
def become_visible_waiting_with_timeout(context, element_id, seconds):
    try:
        WebDriverWait(context.browser, int(seconds)).until(EC.visibility_of_element_located((By.ID, element_id)))
    except TimeoutException:
        raise TimeoutException("element with id %s did not become visible "
                               "after %s seconds" % (element_id, seconds))


@step(u'I expect for "{page_title}" page to appear within max {seconds} seconds')
def page_waiting_with_timeout(context, page_title, seconds):
    """
    Function that wait for page to appear but for a maximum amount of time
    """
    try:
        WebDriverWait(context.browser, int(seconds)).until(
            EC.presence_of_element_located((By.ID, page_title)))
    except TimeoutException:
        raise TimeoutException("Page %s did not appear after %s seconds"
                               % (page_title, seconds))


@step(u'I expect for "{loader_name}" loader to finish within max {seconds} '
      u'seconds')
def loader_name_waiting_with_timeout(context, loader_name, seconds):
    """
    Function that wait for loader_name to finish for a maximum amount of time.
    First it will wait for up to 2 seconds for loader to appear and then will
    wait for {seconds} seconds for the loader to disappear.
    If the loader name is key-generate-loader then as an extra precaution
    it will check if the loader has already finished by checking the parent
    container.
    """
    if loader_name == 'key-generate-loader':
        container = context.browser.find_element_by_id("key-add-private-container")
        if 'filled' in container.get_attribute('class'):
            return

    try:
        WebDriverWait(context.browser, 2).until(EC.presence_of_element_located((By.ID, loader_name)))
    except TimeoutException:
        raise TimeoutException("loader %s did not appear after 2 seconds"
                               % loader_name)

    end = time() + int(seconds)
    while time() < end:
        try:
            context.browser.find_element_by_id(loader_name)
            sleep(1)
        except NoSuchElementException:
            return
    assert False, 'Loader %s did not finish after %s seconds' % (loader_name,
                                                                 seconds)


@step(u'I refresh the browser')
def refresh(context):
    context.browser.refresh()


@step(u'I should be in the machines page')
def check_if_its_machines_page(context):
    try:
        context.browser.find_element_by_id('machine-list')
        return True
    except NoSuchElementException:
        assert False, ''


@step(u'my name should be "{my_name}"')
def check_user_name(context, my_name):
    user_span = context.browser.find_element_by_class_name('owner')
    user_span_text = safe_get_element_text(user_span)
    assert user_span_text.lower() == my_name.lower(), "Name appearing on the" \
                                                      " screen is not " \
                                                      "than %s" % my_name


@step(u'I should read "{something}" in input with id "{input_id}"')
def check_input_for_text(context, something, input_id):
    input = None
    try:
        input = context.browser.find_element_by_id(input_id)
    except NoSuchElementException:
        pass
    assert input, 'Could not find element with id %s' % input_id
    assert input.get_attribute('value').lower() == something.lower(), \
        "Input text did not match what was expected"
