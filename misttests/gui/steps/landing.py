from behave import step

from time import time
from time import sleep

from .utils import safe_get_element_text

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


def get_shadow_root(context,web_element):
    shadow_root = context.browser.execute_script('return arguments[0].shadowRoot', web_element)
    return shadow_root


@step(u'I open the {kind} popup')
def open_login_popup(context, kind):
    kind = kind.lower()
    modals = {'login': 'modalLogin', 'signup': 'modalRegister'}
    if kind.lower() not in modals.keys():
        raise ValueError('No such popup in the landing page')
    landing_app = context.browser.find_element_by_tag_name("landing-app")
    shadow_root = get_shadow_root(context, landing_app)

    if kind == 'login':
        app_toolbar = shadow_root.find_element_by_css_selector("app-toolbar")
        sign_in_class = app_toolbar.find_element_by_class_name('signin-btn-container')
        a = sign_in_class.find_element_by_tag_name("a")
        button_to_click = a.find_element_by_tag_name("paper-button")

    elif kind == 'signup':
        landing_pages = shadow_root.find_element_by_css_selector('landing-pages')
        landing_home = landing_pages.find_element_by_tag_name("landing-home")
        inner_shadow_root = get_shadow_root(context, landing_home)
        div = inner_shadow_root.find_element_by_id('container')
        inner_div = div.find_element_by_css_selector('div')
        a = inner_div.find_element_by_tag_name("a")
        button_to_click = a.find_element_by_tag_name("paper-button")

    if button_to_click.is_displayed():
        button_to_click.click()


@step("I click the {text} button in the landing page popup")
def click_button_in_landing_page(context, text):
    from .buttons import clicketi_click
    text = text.lower()
    if text not in ['email', 'google', 'github', 'sign in', 'sign up',
                    'submit', 'forgot password', 'reset_password_email_submit',
                    'reset_pass_submit', 'go']:
        raise ValueError('This button does not exist in the landing page popup')

    landing_app = context.browser.find_element_by_tag_name("landing-app")
    shadow_root = get_shadow_root(context, landing_app)
    landing_pages = shadow_root.find_element_by_css_selector("landing-pages")

    if text == 'sign in' or text == 'forgot password':
        page = landing_pages.find_element_by_tag_name('landing-sign-in')
    elif text.lower() == 'sign up':
        page = landing_pages.find_element_by_tag_name('landing-sign-up')
    elif text.lower() == 'go':
        page = landing_pages.find_element_by_tag_name('landing-set-password')
    elif text.lower() == 'reset_password_email_submit':
        page = landing_pages.find_element_by_tag_name('landing-forgot-password')
    elif text.lower() == 'reset_pass_submit':
        page = landing_pages.find_element_by_tag_name('landing-reset-password')

    shadow_root = get_shadow_root(context, page)
    iron_form = shadow_root.find_element_by_css_selector('iron-form')
    form = iron_form.find_element_by_tag_name('form')

    if text == 'sign in':
        popup = form.find_element_by_id('signInSubmit')
    elif text == 'sign up':
        popup = form.find_element_by_id('signUpSubmit')
    elif text == 'go':
        popup = form.find_element_by_id('setPasswordSubmit')
    elif text == 'forgot password':
        popup = form.find_element_by_id('forgotPasswordLink')
    elif text == 'reset_password_email_submit':
        popup = form.find_element_by_id('forgotPasswordSubmit')
    elif text == 'reset_pass_submit':
        popup = form.find_element_by_id('resetPasswordSubmit')

    clicketi_click(context, popup)
    return


def get_mist_config_email(context,kind):
    if kind == 'invalid_email':
        return 'tester'
    elif kind == 'rbac_member1':
        return context.mist_config['MEMBER1_EMAIL']
    else:
        return context.mist_config['EMAIL']


def get_mist_config_password(context,kind):
    if kind == 'alt':
        return context.mist_config['PASSWORD2']
    elif kind == 'rbac_member1':
        return context.mist_config['MEMBER1_PASSWORD']
    elif kind == 'new_creds':
        return context.mist_config['GMAIL_FATBOY_PASSWORD']
    elif kind == 'rbac_member2':
        import ipdb;ipdb.set_trace()
        return context.mist_config['MEMBER2_PASSWORD']
    else:
        return context.mist_config['PASSWORD1']


@step(u'I enter my {kind} credentials for {action}')
def enter_credentials(context, kind, action):
    from .forms import clear_input_and_send_keys

    kind = kind.lower()
    action = action.lower()
    if action not in ['login', 'signup', 'signup_password_set',
                      'password_reset_request', 'password_reset',
                      'demo request']:
        raise ValueError("Cannot input %s credentials" % action)
    if kind not in ['standard', 'alt', 'rbac_owner', 'rbac_member1',
                    'rbac_member2', 'new_creds'] and not kind.startswith('invalid'):
        raise ValueError("No idea what %s credentials are" % kind)

    landing_app = context.browser.find_element_by_tag_name("landing-app")
    shadow_root = get_shadow_root(context, landing_app)
    landing_pages = shadow_root.find_element_by_css_selector("landing-pages")

    if action == 'login':
        sign_in_class = landing_pages.find_element_by_tag_name('landing-sign-in')
        shadow_root = get_shadow_root(context, sign_in_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')

        email_input = form.find_element_by_id("signin-email")
        email_input.send_keys(get_mist_config_email(context, kind))

        password_input = form.find_element_by_id("signin-password")
        password_input.send_keys(get_mist_config_password(context, kind))

    elif action == 'signup':
        sign_up_class = landing_pages.find_element_by_tag_name('landing-sign-up')
        shadow_root = get_shadow_root(context, sign_up_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')

        name_input = form.find_element_by_id("name")
        name_input.send_keys(context.mist_config['NAME'])

        email_input = form.find_element_by_id("signUp-email")
        email_input.send_keys(get_mist_config_email(context, kind))

    elif action == 'password_reset_request':
        password_reset_class = landing_pages.find_element_by_tag_name('landing-forgot-password')
        shadow_root = get_shadow_root(context, password_reset_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')

        email_input = form.find_element_by_id("forgotPassword-email")
        email_input.send_keys(get_mist_config_email(context, kind))

    elif action == 'password_reset':
        password_reset_class = landing_pages.find_element_by_tag_name('landing-reset-password')
        shadow_root = get_shadow_root(context, password_reset_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')

        mist_password = form.find_element_by_tag_name('mist-password')
        shadow_root = get_shadow_root(context, mist_password)

        pass_input = shadow_root.find_element_by_css_selector('paper-input')
        pass_input.send_keys(get_mist_config_password(context, kind))
        #clear_input_and_send_keys(pass_input, get_mist_config_password(context, kind))

    elif action == 'signup_password_set':
        set_password_class = landing_pages.find_element_by_tag_name('landing-set-password')

        shadow_root = get_shadow_root(context, set_password_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')
        mist_password = form.find_element_by_tag_name('mist-password')
        shadow_root = get_shadow_root(context, mist_password)

        pass_input = shadow_root.find_element_by_css_selector('paper-input')
        pass_input.send_keys(get_mist_config_password(context, kind))
        #clear_input_and_send_keys(pass_input, password_to_use)


@step(u'there should be an "{error_message}" error message inside the "{button}" button')
def check_error_message(context, error_message, button):
    button = button.lower()
    error_message = error_message.lower()
    if button not in ['sign in']:
        raise Exception('Unknown type of button')
    if button == 'sign in':
        landing_app = context.browser.find_element_by_tag_name("landing-app")
        shadow_root = get_shadow_root(context, landing_app)
        landing_pages = shadow_root.find_element_by_css_selector("landing-pages")
        sign_in_class = landing_pages.find_element_by_tag_name('landing-sign-in')
        shadow_root = get_shadow_root(context, sign_in_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')
        login_popup = form.find_element_by_id('signInSubmit')
        text = safe_get_element_text(login_popup).lower()

    if text == error_message:
        return
    assert False, "Error message was not %s but instead %s" % \
                                                  (error_message, text)


@step(u'the {button} button should be {state}')
def check_state_of_button(context, button, state):
    state = state.lower()
    if state not in ['clickable', 'not clickable']:
        raise Exception('Unknown state of button')
    if button == 'sign in':
        landing_app = context.browser.find_element_by_tag_name("landing-app")
        shadow_root = get_shadow_root(context, landing_app)
        landing_pages = shadow_root.find_element_by_css_selector("landing-pages")
        sign_in_class = landing_pages.find_element_by_tag_name('landing-sign-in')
        shadow_root = get_shadow_root(context, sign_in_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')
        login_popup = form.find_element_by_id('signInSubmit')
        is_not_clickable = login_popup.get_attribute('aria-disabled')

    if state == 'clickable' and is_not_clickable == 'false':
        return
    elif state == 'not clickable' and is_not_clickable == 'true':
        return
    else:
        assert False, "Desired state of the %s button is %s, but it is not!" % \
                                        (button, state)


@step(u'I should get a conflict error')
def already_registered(context):
    landing_app = context.browser.find_element_by_tag_name("landing-app")
    shadow_root = get_shadow_root(context, landing_app)
    landing_pages = shadow_root.find_element_by_css_selector("landing-pages")
    sign_up_class = landing_pages.find_element_by_tag_name('landing-sign-up')
    shadow_root = get_shadow_root(context, sign_up_class)
    iron_form = shadow_root.find_element_by_css_selector('iron-form')
    form = iron_form.find_element_by_tag_name('form')
    error_msg = form.find_element_by_id("signUpSubmit")
    if 'conflict' in safe_get_element_text(error_msg).lower():
        return
    assert False, 'No conflict message appeared'


@step(u'I should see the landing page within {seconds} seconds')
def wait_for_landing_page(context, seconds):
    try:
        WebDriverWait(context.browser, int(seconds)).until(
            EC.element_to_be_clickable((By.ID, "top-signup-button")))
    except TimeoutException:
        raise TimeoutException("Landing page has not appeared after %s seconds"
                               % seconds)


@step(u'that I am redirected within {seconds} seconds')
def ensure_redirection(context, seconds):
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            context.browser.find_element_by_id("top-signup-button")
            sleep(1)
        except NoSuchElementException:
            return True
    assert False, "I wasn't redirected to the app after waiting for %s seconds"\
                  % seconds
