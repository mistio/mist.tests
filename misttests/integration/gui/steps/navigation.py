from behave import step, then

from time import time
from time import sleep

from misttests.integration.gui.steps.buttons import clicketi_click
from misttests.integration.gui.steps.buttons import click_the_user_icon
from misttests.integration.gui.steps.buttons import click_button_from_collection

from misttests.integration.gui.steps.forms import clear_input_and_send_keys

from misttests.integration.gui.steps.utils import safe_get_element_text, expand_shadow_root, get_page_element, add_credit_card_if_needed, check_page_is_visible

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import WebDriverException

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
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#top-signup-button")))
    except TimeoutException:
        raise TimeoutException("Signup button did not appear %s "
                               "seconds" % timeout)

    time_left -= time()
    try:
        WebDriverWait(context.browser, time_left).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#top-signup-button")))
    except TimeoutException:
        raise TimeoutException("Signup button did not become clickable after "
                               "%s seconds" % time_left)


@step('I visit mist')
def visit(context):
    if not i_am_in_homepage(context):
        context.browser.get(context.mist_config['MIST_URL'])
    timeout = time() + 4
    while time() < timeout:
        try:
            elements = context.browser.find_element(By.CSS_SELECTOR, "landing-app")
            return
        except NoSuchElementException:
            try:
                context.browser.find_element(By.XPATH, "//mist-app[@page='dashboard']")
                wait_for_dashboard(context)
                return
            except NoSuchElementException:
                pass
        sleep(1)
    assert False, "Do not know if I am at the landing page or the home page"


@step('I make sure the menu is open')
def make_sure_menu_is_open(context):
    end_time = time() + 15
    while time() < end_time:
        try:
            menu = context.browser.find_element(By.CSS_SELECTOR, '#sidebar')
            if menu.get_attribute('isclosed') == 'true':
                top_bar = context.browser.find_element(By.CSS_SELECTOR, '#topBar')
                button = top_bar.find_element(By.XPATH, './paper-icon-button["icon=menu"]')
                button.click()
                break
        except (NoSuchElementException, ValueError, AttributeError):
            assert time() + 1 < end_time, "Menu button has not" \
                                          " appeared after 10 seconds"
            sleep(1)


@step('I wait for the navigation menu to appear')
def wait_for_buttons_to_appear(context):
    #context.execute_steps(u'Then I make sure the menu is open')
    end_time = time() + 20
    sections = []
    while time() < end_time:
        try:
            mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
            mist_app_shadow = expand_shadow_root(context, mist_app)
            sidebar = mist_app_shadow.find_element(
                By.CSS_SELECTOR, 'mist-sidebar')
            sidebar_shadow = expand_shadow_root(context, sidebar)
            sections = sidebar_shadow.find_elements(By.CSS_SELECTOR, '.section')
            if len(sections) >= 2:
                break
        except (NoSuchElementException, ValueError, AttributeError):
            assert time() + 1 < end_time, "Links in the home page have not" \
                                          " appeared after 20 seconds"
            sleep(1)
    assert len(sections) >= 2, "Sidebar has no visible items after 20 seconds"

def filter_buttons(container, text):
    return [el for el in container.find_elements(By.CSS_SELECTOR, 'paper-button') if safe_get_element_text(el).strip().lower() == text]


@step('I wait for the dashboard to load')
def wait_for_dashboard(context):
    context.execute_steps('Then I wait for the navigation menu to appear')
    dashboard_page = get_page_element(context, 'dashboard')
    dashboard_shadow = expand_shadow_root(context, dashboard_page)
    timeout = 35
    try:
        WebDriverWait(dashboard_shadow, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              "div#content")))
    except TimeoutException:
        raise TimeoutException("Dashboard did not load after %s seconds"
                               % timeout)
    save_org = filter_buttons(dashboard_shadow, 'save organisation')
    if save_org:
        org_input = dashboard_shadow.find_element(By.CSS_SELECTOR, 'paper-input#orginput')
        context.organizational_context = org_input.get_attribute('value').strip().lower()
        clicketi_click(context, save_org[0])
        return True


@step('I visit the {title} page')
def go_to_some_page_without_waiting(context, title):
    title = title.lower()
    if title not in ['machines', 'images', 'keys', 'networks', 'tunnels',
                     'scripts', 'schedules', 'templates', 'stacks', 'teams',
                     'account', 'insights', 'home', 'zones', 'rules', 'volumes',
                     'signup']:
        raise ValueError('The page given is unknown')
    if title.lower() == 'home':
        context.execute_steps('When I click the mist logo')
    elif title.lower() == 'account':
        context.execute_steps('''
                When I click the button "Account" in the user menu
               ''')
        return
    elif title.lower() == 'signup':
        context.browser.get(context.mist_config['MIST_URL'] + '/sign-up')
    else:
        mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
        mist_app_shadow = expand_shadow_root(context, mist_app)
        sidebar = mist_app_shadow.find_element(
            By.CSS_SELECTOR, 'mist-sidebar')
        sidebar_shadow = expand_shadow_root(context, sidebar)
        button = sidebar_shadow.find_element(By.CSS_SELECTOR, '#' + title)
        sleep(1)
        try:
            button.click()
            check_page_is_visible(context, title, 10)
        except TimeoutException as WebDriverException:
            print('Second click required!')
            sleep(5)
            clicketi_click(context, button) # Sometimes it may need a second click, not sure why
            context.execute_steps('Then I expect for "%s" page to appear within '
                                  'max 10 seconds' % title)


@step('I visit the {title} page after the counter has loaded')
def go_to_some_page_after_loading(context, title):
    """
    WIll visit one of the basic pages(Machines, Images, Keys, Scripts ,Teams, Zones) and has
    the choice of waiting for the counter to load.
    For now the code will not be very accurate for keys page
    """
    context.execute_steps('When I visit the %s page after the %s counter has'
                          ' loaded' % (title, title))


@step('I visit the {title} page after the {counter_title} counter has loaded')
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
    context.execute_steps('''
        Then I wait for the navigation menu to appear
        Then %s counter should be greater than 0 within 80 seconds
        When I visit the %s page
    ''' % (counter_title, title))


@step('I expect the "{title}" page to be visible within max {timeout} seconds')
def expect_page_to_be_visible(context, title, timeout):
    title = title.lower()
    if title in ['key', 'machine', 'script', 'cloud', 'image', 'network', 'template', 'stack', 'zone', 'volume', 'team', 'schedule', 'tunnel', 'zone']:
        container_element = get_page_element(context, title + 's')
        container_shadow = expand_shadow_root(context, container_element)
        try:
            WebDriverWait(container_shadow, int(timeout)).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "%s-page" % title)))
        except TimeoutException:
            raise TimeoutException("Page `%s` did not appear within %s "
                                   "seconds" % (title, timeout))
    else:
        raise NotImplementedError('STEP: Then I expect the %s page to be visible within max 10 seconds' % title)


@step('I scroll to the element with id "{element_id}"')
def scroll_to_element(context, element_id):
    context.browser.execute_script(
        "document.querySelector('#" + element_id + "').scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'})"
    )


@step('I scroll to the bottom of the page')
def scroll_to_add_new_rule_btn(context):
    context.browser.execute_script("window.scrollTo(0, 2000)")


@step('I scroll to the rules section in the "machine" page')
def scroll_to_rules_section(context):
    _, page_element = get_page_element(context, "machines", "machine")
    page_shadow = expand_shadow_root(context, page_element)
    mist_rules = page_shadow.find_element(By.CSS_SELECTOR, 'mist-rules')
    context.browser.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'})", mist_rules)


@step('I scroll to the top of the page')
def scroll_to_top(context):
    context.browser.execute_script("window.scrollTo(0, 0)")


@step('I am logged in to mist')
def given_logged_in(context):
    try:
        context.browser.find_element(By.CSS_SELECTOR, "mist-app")
        return
    except:
        pass
    if not i_am_in_homepage(context):
        context.execute_steps('When I visit mist')

    context.execute_steps("""
        When I open the login popup
        And I enter my standard credentials for login
        And I click the sign in button in the landing page popup
        Then I wait for the navigation menu to appear
    """)


@step('I have given card details if needed')
def give_cc_details_if_necessary(context):
    mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    add_credit_card_if_needed(context, mist_app_shadow)


def found_one(context):
    success = 0
    timeout = time() + 30
    while time() < timeout:
        try:
            context.browser.find_element(By.CSS_SELECTOR, "#top-signup-button")
            success += 1
            if success == 2:
                return True
        except NoSuchElementException:
            try:
                context.browser.find_element(By.CSS_SELECTOR, "mist-app")
                success += 1
                if success == 2:
                    return True
            except NoSuchElementException:
                try:
                    context.browser.find_element(By.CSS_SELECTOR, "#splash")
                    success += 1
                    if success == 2:
                        return True
                except NoSuchElementException:
                    pass
        sleep(1)
    return False


@step('I am logged in to mist as {kind}')
def given_logged_in(context, kind):
    if kind in ['rbac_owner', 'rbac_member1', 'rbac_member2']:
        context.execute_steps("""
            When I open the login popup
            And I enter my %s credentials for login
            And I click the sign in button in the landing page popup
            And I wait for the navigation menu to appear
        """ % kind)
    elif kind == 'reg_member':
        context.execute_steps("""
            When I open the login popup
            And I enter my standard credentials for login
            And I click the sign in button in the landing page popup
            And I wait for the navigation menu to appear
        """)


@step('I am not logged in to mist')
def given_not_logged_in(context):
    if not i_am_in_homepage(context):
        context.execute_steps('When I visit mist')
    try:
        context.browser.find_element(By.CSS_SELECTOR, "landing-app")
        return
    except:
        try:
            context.execute_steps("""
                  When I visit the Home page
                  When I wait for the dashboard to load
                  And I logout
            """)
        except NoSuchElementException:
            pass


def get_user_menu(context):
    mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    mist_header = mist_app_shadow.find_element(By.CSS_SELECTOR, 'mist-header')
    mist_header_shadow = expand_shadow_root(context, mist_header)
    app_user_menu = mist_header_shadow.find_element(By.CSS_SELECTOR, 'app-user-menu')
    app_user_menu_shadow = expand_shadow_root(context, app_user_menu)
    return app_user_menu_shadow.find_element(By.CSS_SELECTOR, '.dropdown-content')


@step('I open the user menu')
def click_user_icon_and_wait_for_menu(context):
    """click the avatar icon and wait until the user menu starts opening"""
    for _ in range(2):
        click_the_user_icon(context)
        user_menu = get_user_menu(context)
        timeout = time() + 2
        while time() < timeout:
            if user_menu.size['width'] > 0 and user_menu.size['height'] > 0:
                return
            sleep(1)

    assert False, "Width or height or both of user menu are 0 after 2 clicks"


@step('the "{title}" navigation menu item should be hidden')
def go_to_some_page_without_waiting(context, title):
    title = title.lower()
    if title not in ['machines', 'images', 'keys', 'networks', 'tunnels',
                     'scripts', 'schedules', 'templates', 'stacks', 'teams',
                     'insights', 'zones', 'rules', 'volumes']:
        raise ValueError('The page given is unknown')
    mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    sidebar = mist_app_shadow.find_element(
        By.CSS_SELECTOR, 'mist-sidebar')
    sidebar_shadow = expand_shadow_root(context, sidebar)
    button = sidebar_shadow.find_element(By.CSS_SELECTOR, '#' + title)
    sleep(1)
    assert not button.is_displayed(), "Navigation menu item is not hidden!"

@step('the "{title}" navigation menu item should not exist')
def go_to_some_page_without_waiting(context, title):
    title = title.lower()
    if title not in ['clouds', 'machines', 'images', 'keys', 'networks',
                     'tunnels', 'scripts', 'schedules', 'templates', 'stacks',
                     'teams', 'insights', 'zones', 'rules', 'volumes']:
        raise ValueError('The page given is unknown')
    mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    sidebar = mist_app_shadow.find_element(
        By.CSS_SELECTOR, 'mist-sidebar')
    sidebar_shadow = expand_shadow_root(context, sidebar)
    buttons = sidebar_shadow.find_elements(By.CSS_SELECTOR, '#' + title)
    sleep(1)
    assert len(buttons) == 0, "Navigation menu item is not hidden!"

@step('I logout')
def logout(context):
    from misttests.integration.gui.steps.buttons import click_the_user_menu_button
    click_the_user_menu_button(context, 'logout')
