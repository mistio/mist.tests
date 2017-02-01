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
    popup_id = modals[kind]
    landing_app = context.browser.find_element_by_tag_name("landing-app")
    shadow_root = get_shadow_root(context, landing_app)
    if kind == 'login':
        app_toolbar = shadow_root.find_element_by_css_selector("app-toolbar")
        sign_in_class = app_toolbar.find_element_by_class_name('signin-btn-container')
        a = sign_in_class.find_element_by_tag_name("a")
        sign_in_btn = a.find_element_by_tag_name("paper-button")
        # click_sign_in(context,sign_in_btn)
        #button_collapse = context.browser.find_element_by_class_name('button-collapse')
        # from .buttons import clicketi_click
        # clicketi_click(context,sign_in_btn)
        if sign_in_btn.is_displayed():
            sign_in_btn.click()
    elif kind == 'signup':
        iron_pages = shadow_root.find_element_by_css_selector('iron-pages')
        landing_home = iron_pages.find_element_by_tag_name("landing-home")
        inner_shadow_root = get_shadow_root(context, landing_home)
        div = inner_shadow_root.find_element_by_css_selector('div')
        a = div.find_element_by_tag_name("a")
        sign_up_btn = a.find_element_by_tag_name("paper-button")

        if sign_up_btn.is_displayed():
            sign_up_btn.click()
    # else:
    #     button_collection = context.browser.find_elements_by_class_name("btn-large")
    #     click_button_from_collection(context, "get started", button_collection,
    #                                  error_message="Could not find get started "
    #                                                "button in the landing page")
    # # then wait until the modal is displayed
    # timeout = time() + 10
    # dimensions = None
    # while time() < timeout:
    #     try:
    #         popup = context.browser.find_element_by_id(popup_id)
    #         if dimensions is None:
    #             dimensions = popup.size
    #         elif dimensions['width'] == popup.size['width'] and \
    #                 dimensions['height'] == popup.size['height']:
    #             sleep(1)
    #             return True
    #         else:
    #             dimensions = popup.size
    #     except NoSuchElementException:
    #         pass
    #     sleep(1)
    #
    # assert False, "Modal has not appeared yet on screen"


@step("I click the {text} button in the landing page popup")
def click_button_in_landing_page(context, text):
    from .buttons import clicketi_click
    text = text.lower()
    if text not in ['email', 'google', 'github', 'sign in', 'sign up'
                            , 'submit', 'request demo', 'forgot password',
                            'reset_password_email_submit', 'reset_pass_submit']:
        raise ValueError('This button does not exist in the landing page popup')
    landing_app = context.browser.find_element_by_tag_name("landing-app")
    shadow_root = get_shadow_root(context, landing_app)
    neon_animated_pages = shadow_root.find_element_by_css_selector("neon-animated-pages")

    if text == 'sign in':
            sign_in_class = neon_animated_pages.find_element_by_tag_name('landing-sign-in')
            shadow_root = get_shadow_root(context, sign_in_class)
            iron_form = shadow_root.find_element_by_css_selector('iron-form')
            form = iron_form.find_element_by_tag_name('form')
            login_popup = form.find_element_by_id('signInSubmit')
            clicketi_click(context, login_popup)
            return
    elif text.lower() == 'sign up':
            sign_in_class = neon_animated_pages.find_element_by_tag_name('landing-sign-up')
            shadow_root = get_shadow_root(context, sign_in_class)
            iron_form = shadow_root.find_element_by_css_selector('iron-form')
            form = iron_form.find_element_by_tag_name('form')
            signup_popup = form.find_element_by_id('signUpSubmit')
            clicketi_click(context, signup_popup)
            return

    # try:
    #     password_set_popup = context.browser.find_element_by_id('modalPasswordSet')
    #     if password_set_popup.is_displayed():
    #         click_button_from_collection(context, text,
    #                                      password_set_popup.find_elements_by_class_name('btn-large'))
    #         sleep(1)
    #         return
    # except NoSuchElementException:
    #     pass
    # try:
    #     if text == 'reset_password_email_submit':
    #         text = 'submit'
    #     password_reset_email_popup = context.browser.find_element_by_id('modalPasswordRequest')
    #     if password_reset_email_popup.is_displayed():
    #         click_button_from_collection(context, text,
    #                                      password_reset_email_popup.find_elements_by_class_name('btn-large'))
    #         sleep(1)
    #         return
    # except NoSuchElementException:
    #     pass
    # try:
    #     if text == 'reset_pass_submit':
    #         text = 'submit'
    #     password_reset_email_popup = context.browser.find_element_by_id('modalPasswordReset')
    #     if password_reset_email_popup.is_displayed():
    #         click_button_from_collection(context, text,
    #                                      password_reset_email_popup.find_elements_by_class_name('btn-large'))
    #         sleep(1)
    #         return
    # except NoSuchElementException:
    #     pass
    assert False, "Could not find any popups in the landing page"


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
    else:
        return context.mist_config['PASSWORD1']


@step(u'I enter my {kind} credentials for {action}')
def enter_creds(context, kind, action):
    from .forms import clear_input_and_send_keys

    kind = kind.lower()
    action = action.lower()
    if action not in ['login', 'signup', 'signup_password_set',
                      'password_reset_request', 'password_reset',
                      'demo request']:
        raise ValueError("Cannot input %s credentials" % action)
    if kind not in ['standard', 'alt', 'rbac_owner', 'rbac_member1',
                    'rbac_member2'] and not kind.startswith('invalid'):
        raise ValueError("No idea what %s credentials are" % kind)
    landing_app = context.browser.find_element_by_tag_name("landing-app")
    shadow_root = get_shadow_root(context, landing_app)
    neon_animated_pages = shadow_root.find_element_by_css_selector("neon-animated-pages")

    if action == 'login':
        sign_in_class = neon_animated_pages.find_element_by_tag_name('landing-sign-in')
        shadow_root = get_shadow_root(context, sign_in_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')

        email_input = form.find_element_by_id("signin-email")
        email_input.send_keys(get_mist_config_email(context, kind))

        password_input = form.find_element_by_id("signin-password")
        password_input.send_keys(get_mist_config_password(context, kind))

    elif action == 'signup':
        sign_up_class = neon_animated_pages.find_element_by_tag_name('landing-sign-up')
        shadow_root = get_shadow_root(context, sign_up_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')

        name_input = form.find_element_by_id("name")
        name_input.send_keys(context.mist_config['NAME'])

        email_input = form.find_element_by_id("email")
        email_input.send_keys(get_mist_config_email(context, kind))
        # try:
        #     WebDriverWait(context.browser, 4).until(
        #         EC.visibility_of_element_located((By.ID, "signup-email")))
        # except TimeoutException:
        #     raise TimeoutException("Email input did not appear after 4 seconds")
        # email_input = context.browser.find_element_by_id("signup-email")
        # if kind == 'rbac_owner':
        #     clear_input_and_send_keys(email_input, context.mist_config['EMAIL'])
        # elif kind == 'rbac_member1':
        #     clear_input_and_send_keys(email_input, context.mist_config['MEMBER1_EMAIL'])
        # else:
        #     clear_input_and_send_keys(email_input, context.mist_config['EMAIL'])
        # name_input = context.browser.find_element_by_id("signup-name")
        # clear_input_and_send_keys(name_input, context.mist_config['NAME'])
    elif action == 'password_reset_request':
        try:
            WebDriverWait(context.browser, 4).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#passwordRequestForm input")))
        except TimeoutException:
            raise TimeoutException("Email input did not appear after 4 seconds")
        email_input = context.browser.find_element_by_css_selector('#passwordRequestForm input')
        clear_input_and_send_keys(email_input, context.mist_config['EMAIL'])
    elif action == 'password_reset':
        try:
            WebDriverWait(context.browser, 4).until(
                EC.visibility_of_element_located((By.ID, "reset_password")))
        except TimeoutException:
            raise TimeoutException("Password input did not appear after 4 "
                                   "seconds")
        pass_input = context.browser.find_element_by_id('reset_password')
        pass_confirm_input = context.browser.find_element_by_id('reset_confirm_password')
        if kind == 'alt':
            password_to_use = context.mist_config['PASSWORD2']
        elif kind == 'standard':
            password_to_use = context.mist_config['PASSWORD1']
        else:
            raise Exception('No such type of creds')
        clear_input_and_send_keys(pass_input, password_to_use)
        clear_input_and_send_keys(pass_confirm_input, password_to_use)
    elif action == 'signup_password_set':
        try:
            WebDriverWait(context.browser, 4).until(
                EC.visibility_of_element_located((By.ID, "password")))
        except TimeoutException:
            raise TimeoutException("Password input did not appear after 4 "
                                   "seconds")
        first_textfield = context.browser.find_element_by_id("password")
        second_textfield = context.browser.find_element_by_id("confirm_password")
        if kind == 'alt':
            password_to_use = context.mist_config['PASSWORD2']
        elif kind == 'standard':
            password_to_use = context.mist_config['PASSWORD1']
        elif kind == 'rbac_owner':
            password_to_use = context.mist_config['PASSWORD1']
        elif kind == 'rbac_member1':
            password_to_use = context.mist_config['MEMBER1_PASSWORD']
        elif kind == 'rbac_member2':
            password_to_use = context.mist_config['MEMBER2_PASSWORD']
        else:
            raise Exception('No such type of creds')
        clear_input_and_send_keys(first_textfield, password_to_use)
        clear_input_and_send_keys(second_textfield, password_to_use)
    elif action == 'demo request':
        try:
            WebDriverWait(context.browser, 4).until(
                EC.visibility_of_element_located((By.ID, "demo-email")))
        except TimeoutException:
            raise TimeoutException("Email input did not appear after 4 seconds")
        email_input = context.browser.find_element_by_id("demo-email")
        if kind == 'standard':
            clear_input_and_send_keys(email_input, context.mist_config['EMAIL'])
        elif kind == 'alt':
            clear_input_and_send_keys(email_input, context.mist_config['DEMO_EMAIL'])
        name_input = context.browser.find_element_by_id("demo-name")
        clear_input_and_send_keys(name_input, context.mist_config['NAME'])


@step(u'there should be an "{error_message}" error message inside the "{button}" button')
def check_error_message(context, error_message, button):
    button = button.lower()
    error_message = error_message.lower()
    if button not in ['sign in']:
        raise Exception('Unknown type of button')
    if button == 'sign in':
        landing_app = context.browser.find_element_by_tag_name("landing-app")
        shadow_root = get_shadow_root(context, landing_app)
        neon_animated_pages = shadow_root.find_element_by_css_selector("neon-animated-pages")
        sign_in_class = neon_animated_pages.find_element_by_tag_name('landing-sign-in')
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
    import ipdb;ipdb.set_trace()
    state = state.lower()
    if state not in ['clickable', 'not clickable']:
        raise Exception('Unknown state of button')
    if button == 'sign in':
        landing_app = context.browser.find_element_by_tag_name("landing-app")
        shadow_root = get_shadow_root(context, landing_app)
        neon_animated_pages = shadow_root.find_element_by_css_selector("neon-animated-pages")
        sign_in_class = neon_animated_pages.find_element_by_tag_name('landing-sign-in')
        shadow_root = get_shadow_root(context, sign_in_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')
        login_popup = form.find_element_by_id('signInSubmit')
        is_not_clickable = login_popup.get_attribute('aria-disabled')

    if state == 'clickable' and not login_popup.get_attribute('aria-disabled'):
        return
    elif state == 'not clickable' and login_popup.get_attribute('aria-disabled'):
        return
    else:
        assert False, "Desired state of the button %s is %s, but it is not!"


@step(u'I should get an already registered error')
def already_registered(context):
    try:
        WebDriverWait(context.browser, int(1)).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'center')))
    except TimeoutException:
        raise TimeoutException("'Already Registered!' message did not appear.")


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
