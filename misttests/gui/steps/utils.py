from behave import step

from time import time
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains


def safe_get_element_text(check_element):
    try:
        return check_element.text
        #return check_element.get_attribute("innerText")
    except StaleElementReferenceException:
        return ""


@step(u'I type "{some_text}" in input with id "{element_id}"')
def give_some_input(context, some_text, element_id):
    input_element = context.browser.find_element_by_id(element_id)
    if context.mist_config.get(some_text):
        some_text = context.mist_config[some_text]
    actions = ActionChains(context.browser)
    actions.move_to_element(input_element)
    actions.click(input_element)
    actions.send_keys(some_text)
    actions.perform()


def focus_on_element(context, element):
    position = element.location
    from navigation import found_one
    assert found_one(context), "I have no idea where I am"
    try:
        context.browser.find_element_by_tag_name("mist-app")
        js = "document.querySelector('paper-header-panel').scroller.scrollTop = %s" % position['y']
        context.browser.execute_script(js)
    except:
        context.browser.execute_script("window.scrollTo(0, %s)" % position['y'])


@step(u'I focus on the "{name}" button')
def focus_on_add_rule(context, name):
    if context.mist_config.get(name):
        name = context.mist_config[name]
    if "add new rule" in name:
        container = context.browser.find_element_by_tag_name("mist-rules")
        focus_on_element(context, container)
    elif "Add Graph" in name:
        button = context.browser.find_element_by_id("add-metric-btn")
        focus_on_element(context, button)
    return


@step(u'I wait for {seconds} seconds')
def wait(context, seconds):
    sleep(int(seconds))


@step(u'the title should be "{text}"')
def assert_title_is(context, text):
    assert text == context.browser.title


@step(u'the title should contain "{text}"')
def assert_title_contains(context, text):
    assert text in context.browser.title


@step(u'{counter_title} counter should be greater than {counter_number} within '
      u'{seconds} seconds')
def some_counter_loaded(context, counter_title, counter_number, seconds):
    counter_title = counter_title.lower()
    if counter_title not in ['machines', 'images', 'keys', 'networks',
                             'tunnels', 'scripts', 'templates', 'stacks',
                             'teams']:
        raise ValueError('The counter given is unknown')
    try:
        counter = context.browser.find_element_by_css_selector('a#%s.app-sidebar'
                                                               % counter_title)
    except NoSuchElementException:
        raise NoSuchElementException("Counter with name %s has not been found"
                                     % counter_title)

    end_time = time() + int(seconds)
    while time() < end_time:
        counter_span = counter.find_element_by_css_selector("span.count")
        counter_span_text = safe_get_element_text(counter_span)
        counter_span_text = "0" if not counter_span_text else counter_span_text
        if int(counter_span_text) > int(counter_number):
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


def wait_for_element_to_be_visible(context, search_tuple, seconds, error_message):
    try:
        WebDriverWait(context.browser, int(seconds)).until(
            EC.visibility_of_element_located(search_tuple))
    except TimeoutException:
        raise TimeoutException(error_message)


@step(u'I expect for "{element_id}" to be visible within max {seconds} '
      u'seconds')
def become_visible_waiting_with_timeout(context, element_id, seconds):
    msg = "element with id %s did not become visible after %s seconds"\
          % (element_id, seconds)
    wait_for_element_to_be_visible(context, (By.ID, element_id),
                                   int(seconds), msg)


# @step(u'I expect for element with tag "{element_name}" element to be visible '
#       u'within max {seconds} seconds')
# def element_become_visible_waiting_with_timeout(context, element_name, seconds):
#     msg = "element %s did not become visible after %s seconds" % (element_name,
#                                                                   seconds)
#     wait_for_element_to_be_visible(context, (By.TAG_NAME, element_name),
#                                    int(seconds), msg)
#
#
# @step(u'I expect the label "{element_text}" to be visible within max {seconds} '
#       u'seconds')
# def element_label_become_visible_waiting_with_timeout(context, element_text, seconds):
#     msg = "Label %s did not become visible after %s seconds" % (element_text,
#                                                                 seconds)
#     wait_for_element_to_be_visible(context,
#                                    (By.XPATH,
#                                     '//label[contains(text(), "%s")]' % str(element_text)),
#                                    int(seconds), msg)


@step(u'I expect for "{page_title}" page to appear within max {seconds} seconds')
def check_page_is_visible(context, page_title, seconds):
    page = page_title.lower()
    if page not in ['machines', 'images', 'keys', 'networks', 'tunnels',
                    'scripts', 'schedules', 'templates', 'stacks', 'teams']:
        raise ValueError('The page given is unknown')
    element = 'page-%s > page-items > div#content.page-items' % page
    msg = "%s page is not visible after %s seconds" % (page, seconds)
    wait_for_element_to_be_visible(context, (By.CSS_SELECTOR, element),
                                   int(seconds), msg)


# @step(u'I expect for "{loader_name}" loader to finish within max {seconds} '
#       u'seconds')
# def loader_name_waiting_with_timeout(context, loader_name, seconds):
#     """
#     Function that wait for loader_name to finish for a maximum amount of time.
#     First it will wait for up to 2 seconds for loader to appear and then will
#     wait for {seconds} seconds for the loader to disappear.
#     If the loader name is key-generate-loader then as an extra precaution
#     it will check if the loader has already finished by checking the parent
#     container.
#     """
#     if loader_name == 'key-generate-loader':
#         container = context.browser.find_element_by_id("key-add-private-container")
#         if 'filled' in container.get_attribute('class'):
#             return
#
#     try:
#         WebDriverWait(context.browser, 2).until(EC.presence_of_element_located((By.ID, loader_name)))
#     except TimeoutException:
#         raise TimeoutException("loader %s did not appear after 2 seconds"
#                                % loader_name)
#
#     end = time() + int(seconds)
#     while time() < end:
#         try:
#             context.browser.find_element_by_id(loader_name)
#             sleep(1)
#         except NoSuchElementException:
#             return
#     assert False, 'Loader %s did not finish after %s seconds' % (loader_name,
#                                                                  seconds)
#
#
# @step(u'I should be in the machines page')
# def check_if_its_machines_page(context):
#     try:
#         context.browser.find_element_by_id('machine-list')
#         return True
#     except NoSuchElementException:
#         assert False, ''


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


def wait_until_visible(element, seconds):
    timeout = time() + seconds
    while time() < timeout:
        if element.is_displayed():
            return True
        sleep(1)
    raise TimeoutException("Element has not become visible after %s seconds"
                           % seconds)
