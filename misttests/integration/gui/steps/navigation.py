from behave import step

from time import time
from time import sleep

from .buttons import clicketi_click
from .buttons import click_the_gravatar
from .buttons import click_button_from_collection

from .forms import clear_input_and_send_keys

from .utils import safe_get_element_text

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException

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
    if not i_am_in_homepage(context):
        context.browser.get(context.mist_config['MIST_URL'])
    timeout = time() + 4
    while time() < timeout:
        try:
            elements = context.browser.find_element_by_tag_name("landing-app")
            return
        except NoSuchElementException:
            try:
                context.browser.find_element_by_xpath("//mist-app[@page='dashboard']")
                wait_for_dashboard(context)
                return
            except NoSuchElementException:
                pass
        sleep(1)
    assert False, "Do not know if I am at the landing page or the home page"


@step(u'I make sure the menu is open')
def make_sure_menu_is_open(context):
    end_time = time() + 15
    while time() < end_time:
        try:
            menu = context.browser.find_element_by_id('sidebar')
            if menu.get_attribute('isclosed') == 'true':
                top_bar = context.browser.find_element_by_id('topBar')
                button = top_bar.find_element_by_xpath('./paper-icon-button["icon=menu"]')
                button.click()
                break
        except (NoSuchElementException, ValueError, AttributeError):
            assert time() + 1 < end_time, "Menu button has not" \
                                          " appeared after 10 seconds"
            sleep(1)


@step(u'I wait for the links in homepage to appear')
def wait_for_buttons_to_appear(context):
    context.execute_steps(u'Then I make sure the menu is open')
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
    timeout = 20
    try:
        WebDriverWait(context.browser, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              "mist-app page-dashboard "
                                              "div#content")))
    except TimeoutException:
        raise TimeoutException("Dashboard did not load after %s seconds"
                               % timeout)
    context.execute_steps(u'Then I expect for "addBtn" to be clickable within '
                          u'max 20 seconds')
    save_org = filter_buttons(context, 'save organisation')
    if save_org:
        org_form = context.browser.find_element_by_id('orginput')
        org_input = org_form.find_element_by_id('input')
        context.organizational_context = org_input.get_attribute('value').strip().lower()
        clicketi_click(context, save_org[0])
        return True


@step(u'I visit the {title} page')
def go_to_some_page_without_waiting(context, title):
    title = title.lower()
    if title not in ['machines', 'images', 'keys', 'networks', 'tunnels',
                     'scripts', 'schedules', 'templates', 'stacks', 'teams',
                     'account', 'insights', 'home', 'zones', 'signup']:
        raise ValueError('The page given is unknown')
    if title.lower() == 'home':
        context.execute_steps(u'When I click the mist.io button')
    elif title.lower() == 'account':
        context.execute_steps(u'''
                When I click the gravatar
                And I wait for 2 seconds
                And I click the "Account" button with id "Account"
               ''')
        return
    elif title.lower() == 'signup':
        context.browser.get(context.mist_config['MIST_URL'] + '/sign-up')
    else:
        button = context.browser.find_element_by_id(
            'sidebar').find_element_by_id(title)
        clicketi_click(context, button)
        context.execute_steps(u'Then I expect for "%s" page to appear within '
                              u'max 10 seconds' % title)


@step(u'I visit the {title} page after the counter has loaded')
def go_to_some_page_after_loading(context, title):
    """
    WIll visit one of the basic pages(Machines, Images, Keys, Scripts ,Teams, Zones) and has
    the choice of waiting for the counter to load.
    For now the code will not be very accurate for keys page
    """
    context.execute_steps(u'When I visit the %s page after the %s counter has'
                          u' loaded' % (title, title))


@step(u'I visit the {title} page after the {counter_title} counter has loaded')
def go_to_some_page_after_counter_loading(context, title, counter_title):
    title = title.lower()
    counter_title = counter_title.lower()
    if title not in ['machines', 'images', 'keys', 'networks', 'tunnels',
                     'scripts', 'templates', 'stacks', 'teams', 'account',
                     'home', 'zones']:
        raise ValueError('The page given is unknown')
    if counter_title not in ['machines', 'images', 'keys', 'networks',
                             'tunnels', 'scripts', 'templates', 'stacks',
                             'teams', 'zones']:
        raise ValueError('The counter given is unknown')
    context.execute_steps(u'''
        Then I wait for the links in homepage to appear
        Then %s counter should be greater than 0 within 80 seconds
        When I visit the %s page
    ''' % (counter_title, title))


@step(u'I scroll to the bottom of the page')
def scroll_to_add_new_rule_btn(context):
    context.browser.execute_script("window.scrollTo(0, 2000)")


@step(u'I am logged in to mist.core')
def given_logged_in(context):
    try:
        context.browser.find_element_by_tag_name("mist-app")
        return
    except:
        pass
    if not i_am_in_homepage(context):
        context.execute_steps(u'When I visit mist.core')

    context.execute_steps(u"""
        When I open the login popup
        And I enter my standard credentials for login
        And I click the sign in button in the landing page popup
        Then I wait for the links in homepage to appear
    """)


@step(u'I have given card details if needed')
def give_cc_details_if_necessary(context):
    try:
        cc_required_dialog = context.browser.find_element_by_id('mistAppCcRequired')
        form = cc_required_dialog.find_element_by_id('inPlanPurchase')
        cc = form.find_element_by_id('cc')
        cc.send_keys(context.mist_config['CC_CC'])
        clear_input_and_send_keys(form.find_element_by_id('cvc'), 
                                  context.mist_config['CC_CVC'])
        clear_input_and_send_keys(form.find_element_by_id('expirationMonth'),
                                  context.mist_config['CC_EXPIRE_MONTH'])
        clear_input_and_send_keys(form.find_element_by_id('expirationYear'),
                                  context.mist_config['CC_EXPIRE_YEAR'])
        clear_input_and_send_keys(form.find_element_by_id('zipCode'),
                                  context.mist_config['CC_ZIP_CODE'])
        for button in cc_required_dialog.find_elements_by_tag_name('paper-button'):
            if button.text.lower() == 'enable':
                clicketi_click(context, button)
                sleep(5)

    except (NoSuchElementException, ElementNotVisibleException) as e:
        pass


def found_one(context):
    success = 0
    timeout = time() + 30
    while time() < timeout:
        try:
            context.browser.find_element_by_id("top-signup-button")
            success += 1
            if success == 2:
                return True
        except NoSuchElementException:
            try:
                context.browser.find_element_by_tag_name("mist-app")
                success += 1
                if success == 2:
                    return True
            except NoSuchElementException:
                try:
                    context.browser.find_element_by_id("splash")
                    success += 1
                    if success == 2:
                        return True
                except NoSuchElementException:
                    pass
        sleep(1)
    return False


@step(u'I am logged in to mist.core as {kind}')
def given_logged_in(context, kind):
    if kind in ['rbac_owner', 'rbac_member1', 'rbac_member2']:
        context.execute_steps(u"""
            When I open the login popup
            And I enter my %s credentials for login
            And I click the sign in button in the landing page popup
            And I wait for the links in homepage to appear
        """ % kind)
    elif kind == 'reg_member':
        context.execute_steps(u"""
            When I open the login popup
            And I enter my standard credentials for login
            And I click the sign in button in the landing page popup
            And I wait for the links in homepage to appear
        """)


@step(u'I am not logged in to mist.core')
def given_not_logged_in(context):
    if not i_am_in_homepage(context):
        context.execute_steps(u'When I visit mist.core')
    try:
        context.browser.find_element_by_tag_name("landing-app")
        return
    except:
        try:
            context.execute_steps(u"""
                  When I visit the Home page
                  And I am in the new UI
                  When I wait for the dashboard to load
                  And I logout
            """)
        except NoSuchElementException:
            pass


def get_user_menu(context):
    return context.browser.find_element_by_tag_name('app-user-menu'). \
        find_element_by_tag_name('iron-dropdown')


def click_and_wait_for_gravatar(context):
    """press the gravatar and wait until the user menu starts opening"""
    for _ in range(2):
        click_the_gravatar(context)
        user_menu = get_user_menu(context)
        timeout = time() + 2
        while time() < timeout:
            if user_menu.size['width'] > 0 and user_menu.size['height'] > 0:
                return
            sleep(1)

    assert False, "Width or height or both of user menu are 0 after 2 clicks"


@step(u'I logout')
def logout(context):
    click_and_wait_for_gravatar(context)
    user_menu = get_user_menu(context)
    timeout = time() + 5
    dimensions = None
    while time() < timeout:
        try:
            if dimensions is None:
                dimensions = user_menu.size
            elif dimensions['width'] == user_menu.size['width'] and \
                            dimensions['height'] == user_menu.size['height']:
                sleep(1)
                click_button_from_collection(context, 'Logout',
                                             user_menu.find_elements_by_tag_name(
                                                 'paper-item'))
                # sleep(2)
                return True
            else:
                dimensions = user_menu.size
        except NoSuchElementException:
            pass
        sleep(1)

    assert False, "User menu has not appeared yet"


def get_gravatar(context):
    return context.browser.find_element_by_css_selector(
        'paper-icon-button.gravatar')
