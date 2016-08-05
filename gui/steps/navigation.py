from behave import step

from time import time
from time import sleep

from .buttons import search_for_button
from .buttons import clicketi_click
from .buttons import click_the_gravatar
from .buttons import click_button_from_collection

from .utils import safe_get_element_text

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def i_am_in_homepage(context):
    possible_urls = [context.mist_config['MIST_URL']]
    if not possible_urls[0].endswith('/'):
        temp = possible_urls[0]
        possible_urls[0] = temp + '/'
        possible_urls.append(temp)
    possible_urls.append(possible_urls[0] + '#')
    possible_urls.append(possible_urls[0] + '#' + '/')
    return context.browser.current_url in possible_urls


def wait_for_log_in_page_to_load(context):
    time_left = time()
    timeout = 120 if context.mist_config['LOCAL'] else 160
    try:
        WebDriverWait(context.browser, timeout).until(
            EC.visibility_of_element_located((By.ID, "top-signup-button")))
    except TimeoutException:
        raise TimeoutException("Signup button did not appear %s "
                               "seconds" % timeout)

    time_left -= time()
    try:
        WebDriverWait(context.browser, time_left).until(
            EC.element_to_be_clickable((By.ID, "top-signup-button")))
    except TimeoutException:
        raise TimeoutException("Signup button did not become clickable after "
                               "%s seconds" % time_left)


@step(u'I visit mist.core')
def visit(context):
    """
    This method will visit the mist.core instance specified by MIST_URL in the
    settings file and if it lands on the sign in page then it will wait for
    the page to load, otherwise if it lands in the splash page then it will
    sleep for one second and then proceed. If you wish to wait for the splash
    page to load then you should use the "Then I wait for the mist.io splash
    page to load" rule.
    """
    if not i_am_in_homepage(context):
        context.browser.get(context.mist_config['MIST_URL'])

    timeout = time() + 4
    while time() < timeout:
        try:
            context.browser.find_element_by_id("top-signup-button")
            wait_for_log_in_page_to_load(context)
            return
        except NoSuchElementException:
            try:
                context.browser.find_element_by_id("splash")
                wait_for_splash_to_load(context)
                return
            except NoSuchElementException:
                pass
        sleep(1)
    assert False, "Do not know if I am at the landing page or the home page"


@step(u'I wait for the mist.io splash page to load')
def standard_splash_waiting(context):
    """
    Function that waits for the splash to load. The maximum time for the page
    to load is 60 seconds in this case
    """
    wait_for_splash_to_appear(context)
    wait_for_splash_to_load(context)


def wait_for_splash_to_appear(context, timeout=20):
    end = time() + timeout
    while time() < end:
        try:
            context.browser.find_element_by_id("splash")
            return
        except NoSuchElementException:
            try:
                context.browser.find_element_by_id("edit-org-form")
                return
            except:
                sleep(1)
    assert False, 'Splash did not appear after %s seconds' % timeout


def wait_for_splash_to_load(context, timeout=60):
    end = time() + timeout
    while time() < end:
        splash_page = context.browser.find_element_by_id("splash")
        display = splash_page.value_of_css_property("display")
        try:
            context.browser.find_element_by_id("edit-org-form")
            org_button = search_for_button(context, 'OK')
            org_button.click()
            return
        except:
            if 'none' in display:
                return
    assert False, 'Page took longer than %s seconds to load' % timeout


@step(u'I am in the new UI')
def am_in_new_UI(context):
    """
    Function that waits for the new UI to load. The maximum time for the page
    to load is 60 seconds in this case
    """
    try:
        context.browser.find_element_by_tag_name("app-main")
        return
    except:
        context.execute_steps(u'''
            Then I wait for the mist.io splash page to load
            When I click the gravatar
            When I click the button "BETA UI"
        ''')


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


def filter_buttons(context, text):
    return filter(lambda el: safe_get_element_text(el).strip().lower() == text,
                              context.browser.find_elements_by_tag_name('paper-button'))


@step(u'I wait for the dashboard to load')
def wait_for_dashboard(context):
    context.execute_steps(u'Then I wait for the links in homepage to appear')
    add_cloud_button = filter_buttons(context, 'add your clouds')
    if add_cloud_button:
        return True
    save_org = filter_buttons(context, 'save organisation')
    if save_org:
        # first save the name of the organizational context for future use then
        # press the button to save the name and finally return successfully
        org_form = context.browser.find_element_by_id('orginput')
        org_input = org_form.find_element_by_id('input')
        context.organizational_context = org_input.get_attribute('value').strip().lower()
        clicketi_click(context, save_org[0])
        return True
    timeout = 20
    try:
        WebDriverWait(context.browser, timeout).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "main-section")))
    except TimeoutException:
        raise TimeoutException("Dashboard did not load after %s seconds"
                               % timeout)
    context.execute_steps(u'Then I expect for "addBtn" to be clickable within '
                          u'max 20 seconds')


@step(u'I visit the {title} page')
def go_to_some_page_without_waiting(context, title):
    """
    WIll visit one of the basic pages(Machines, Images, Keys, Scripts) without
    waiting for the counter or the list on the page to load.
    For now the code will not be very accurate for keys page
    """
    title = title.lower()
    if title not in ['machines', 'images', 'keys', 'networks', 'tunnels',
                     'scripts', 'templates', 'stacks', 'teams', 'account',
                     'home']:
        raise ValueError('The page given is unknown')
    if title == 'Account':
        context.browser.get(context.mist_config['MIST_URL'] + '/account')
        return
    context.execute_steps(u'Then I wait for the links in homepage to appear')
    if title.lower() == 'home':
        context.execute_steps(u'When I click the mist.io button')
    elif title.lower() == 'account':
        # TODO implement account page visit
        return
    else:
        button = context.browser.find_element_by_id('sidebar').find_element_by_id(title)
        clicketi_click(context, button)
        context.execute_steps(u'Then I expect for "%s" page to appear within '
                              u'max 10 seconds' % title)


@step(u'I visit the {title} page after the counter has loaded')
def go_to_some_page_after_loading(context, title):
    """
    WIll visit one of the basic pages(Machines, Images, Keys, Scripts ,Teams) and has
    the choice of waiting for the counter to load.
    For now the code will not be very accurate for keys page
    """
    context.execute_steps(u'When I visit the %s page after the %s counter has'
                          u' loaded' % (title, title))


@step(u'I visit the {title} page after the {counter_title} counter has loaded')
def go_to_some_page_after_counter_loading(context, title, counter_title):
    """
    WIll visit one of the basic pages(Machines, Images, Keys, Scripts) and has
    the choice of waiting for some of the counters to load
    For now the code will not be very accurate for keys page
    """
    title = title.lower()
    counter_title = counter_title.lower()
    if title not in ['machines', 'images', 'keys', 'networks', 'tunnels',
                     'scripts', 'templates', 'stacks', 'teams', 'account',
                     'home']:
        raise ValueError('The page given is unknown')
    if counter_title not in ['machines', 'images', 'keys', 'networks',
                             'tunnels', 'scripts', 'templates', 'stacks',
                             'teams']:
        raise ValueError('The counter given is unknown')
    context.execute_steps(u'''
        Then I wait for the links in homepage to appear
        Then %s counter should be greater than 0 within 80 seconds
        When I visit the %s page
    ''' % (counter_title, title))


@step(u'I visit the machines page with a url')
def visit_machines_url(context):
    machines_url = context.mist_config['MIST_URL']
    if not machines_url.endswith('/'):
        machines_url += '/'
    machines_url += 'machines'
    context.browser.get(machines_url)


@step(u'I am logged in to mist.core')
def given_logged_in(context):
    try:
        context.browser.find_element_by_tag_name("app-main")
        #we're on the new UI
        return
    except:
        pass
    if not i_am_in_homepage(context):
        context.execute_steps(u'When I visit mist.core')

    try:
        context.browser.find_element_by_id("top-signup-button")
        context.execute_steps(u"""
            When I open the login popup
            Then I click the email button in the landing page popup
            And I enter my standard credentials for login
            And I click the sign in button in the landing page popup
        """)
    except NoSuchElementException:
        try:
            context.browser.find_element_by_id("splash")
        except NoSuchElementException:
            raise NoSuchElementException("I am not in the landing page or the"
                                         " home page")

    context.execute_steps(u'Then I wait for the mist.io splash page to load')


@step(u'I am logged in to mist.core as {kind}')
def given_logged_in(context, kind):
    if not i_am_in_homepage(context):
        context.execute_steps(u'When I visit mist.core')

    try:
        context.browser.find_element_by_id("top-signup-button")
        if kind == 'rbac_owner' or kind == 'rbac_member1':
            context.execute_steps(u"""
                When I open the login popup
                Then I click the email button in the landing page popup
                And I enter my %s credentials for login
                And I click the sign in button in the landing page popup
            """ % kind)
        elif kind == 'reg_member':
            context.execute_steps(u"""
                When I open the login popup
                Then I click the email button in the landing page popup
                And I enter my standard credentials for login
                And I click the sign in button in the landing page popup
            """)
    except NoSuchElementException:
        try:
            context.browser.find_element_by_id("splash")
        except NoSuchElementException:
            raise NoSuchElementException("I am not in the landing page or the"
                                         " home page")

    context.execute_steps(u'Then I wait for the mist.io splash page to load')


@step(u'I am not logged in to mist.core')
def given_not_logged_in(context):
    if not i_am_in_homepage(context):
        context.execute_steps(u'When I visit mist.core')

    try:
        context.browser.find_element_by_id("splash")
        context.execute_steps(u"""
              Then I wait for the mist.io splash page to load
              And I wait for the links in homepage to appear
              And I logout
        """)
    except NoSuchElementException:
        pass


@step(u'I logout')
def logout(context):
    click_the_gravatar(context)
    context.execute_steps(u'''
        Then I wait for 2 seconds
    ''')

    container = context.browser.find_element_by_id("user-menu-popup")
    container.find_element_by_class_name('icon-x').click()

    try:
        WebDriverWait(context.browser, 10).until(
            EC.element_to_be_clickable((By.ID, "top-signup-button")))
        return
    except TimeoutException:
        raise TimeoutException("Landing page has not appeared after 10 seconds")


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


def get_gravatar(context):
    return context.browser.find_element_by_css_selector(
        'paper-icon-button.gravatar')


def get_current_context(context):
    return safe_get_element_text(context.browser.find_element_by_css_selector(
            'div.current.context').find_element_by_tag_name('h4')).strip().lower()


@step(u'I ensure that I am in the "{organization}" organization context')
def ensure_organizational_context(context, organization):
    context.execute_steps(u'''
        Then I click the Gravatar
        And I wait for 1 seconds
    ''')
    organization = organization.strip().lower()
    if get_current_context(context) == organization:
        return True
    else:
        buttons = context.browser.find_element_by_id('topBar'). \
            find_element_by_id('dropdown').\
            find_elements_by_tag_name('paper-item')
        click_button_from_collection(context, organization, buttons)
        context.execute_steps(u'''
            Then I wait for the dashboard to load
            And I click the Gravatar
            And I wait for 1 seconds
        ''')
    assert get_current_context(context) == organization, \
        "Organizational context has not been changed"
