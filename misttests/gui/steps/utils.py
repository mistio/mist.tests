from behave import step

from time import time
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains


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
        button = context.browser.find_element_by_tag_name("mist-rules")

    elif "Add Graph" in name:
        button = context.browser.find_element_by_xpath("//*[contains(text(), 'Add Graph')]")

    context.browser.execute_script("arguments[0].scrollIntoView();", button)
    
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
                             'teams', 'zones']:
        raise ValueError('The counter given is unknown')
    try:
        counter = context.browser.find_element_by_css_selector('a#%s.mist-sidebar'
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


@step(u'I expect for "{page_title}" page to appear within max {seconds} seconds')
def check_page_is_visible(context, page_title, seconds):
    page = page_title.lower()
    if page not in ['machines', 'images', 'keys', 'networks', 'tunnels',
                    'scripts', 'schedules', 'templates', 'stacks', 'insights', 'teams', 'zones']:
        raise ValueError('The page given is unknown')
    if page in ['machines', 'teams','keys', 'networks', 'scripts', 'schedules', 'templates', 'stacks', 'zones']:
        element = 'page-%s > mist-list' % page
    elif page in ['insights']:
        element = 'page-%s' % page
    else: 
        element = 'page-%s > page-items > div#content.page-items' % page
    msg = "%s page is not visible after %s seconds" % (page, seconds)
    wait_for_element_to_be_visible(context, (By.CSS_SELECTOR, element),
                                   int(seconds), msg)


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
