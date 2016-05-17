from behave import step

from time import time
from time import sleep

from buttons import click_button_from_collection

from utils import safe_get_element_text

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


@step(u'I open the {kind} popup')
def open_login_popup(context, kind):
    if kind.lower() not in ['login', 'signup']:
        raise ValueError('No such popup in the landing page')
    if kind.lower() == 'login':
        popup_id = 'modalLogin'
    else:
        popup_id = 'modalRegister'
    if kind == 'login':
        button_collapse = context.browser.find_element_by_class_name('button-collapse')
        if button_collapse.is_displayed():
            button_collapse.click()
            timeout = time() + 3
            nav = context.browser.find_element_by_id("nav-mobile")
            while time() < timeout:
                if nav.value_of_css_property('right') == '0px':
                    break
                assert time() + 1 < timeout, "Right side nav menu hasn't " \
                                             "appeared after 3 seconds"
                sleep(1)

        button_collection = context.browser.find_elements_by_class_name("btn")
        click_button_from_collection(context, "sign in", button_collection,
                                     error_message="Could not find sign in "
                                                   "button in the landing page")

        try:
            WebDriverWait(context.browser, 10).until(
                EC.visibility_of_element_located((By.ID, popup_id)))
        except TimeoutException:
            raise TimeoutException("Sign in popup did not appear after 10 seconds")

        try:
            WebDriverWait(context.browser, 4).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                  "#%s .email-btn" % popup_id)))
        except TimeoutException:
            raise TimeoutException("Email button did not appear after 4 seconds")

        try:
            WebDriverWait(context.browser, 4).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#%s .email-btn" % popup_id)))
        except TimeoutException:
            raise TimeoutException("Email button did not become clickable "
                                   "after 4 seconds")
    else:
        button_collection = context.browser.find_elements_by_class_name("btn-large")
        click_button_from_collection(context, "get started", button_collection,
                                     error_message="Could not find get started "
                                                   "button in the landing page")

        try:
            WebDriverWait(context.browser, 10).until(
                EC.visibility_of_element_located((By.ID, popup_id)))
        except TimeoutException:
            raise TimeoutException("Sign up popup did not appear after 10"
                                   " seconds")

        try:
            WebDriverWait(context.browser, 4).until(
                EC.visibility_of_element_located((By.LINK_TEXT, "SIGN UP")))
        except TimeoutException:
            raise TimeoutException("Signup button did not appear after 4"
                                   " seconds")

        try:
            WebDriverWait(context.browser, 4).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "SIGN UP")))
        except TimeoutException:
            raise TimeoutException("Signup button did not become clickable"
                                   " after 4 seconds")
    sleep(1)


@step("I click the {text} button in the landing page popup")
def click_button_in_landing_page(context, text):
    if text.lower() not in ['email', 'google', 'github', 'sign in', 'sign up'
                            , 'submit', 'request demo', 'forgot password',
                            'reset_password_email_submit', 'reset_pass_submit']:
        raise ValueError('This button does not exist in the landing page popup')
    try:
        reg_popup = context.browser.find_element_by_id("modalRegister")
        if reg_popup.is_displayed():
            click_button_from_collection(context, text, reg_popup.find_elements_by_class_name('btn-large'))
            sleep(1)
            return
    except NoSuchElementException:
        pass
    try:
        login_popup = context.browser.find_element_by_id('modalLogin')
        if login_popup.is_displayed():
            if text.lower() == 'forgot password':
                click_button_from_collection(context, text,
                                             login_popup.find_elements_by_class_name('modal-trigger'))
            else:
                click_button_from_collection(context, text,
                                             login_popup.find_elements_by_class_name('btn-large'))
            sleep(1)
            return
    except NoSuchElementException:
        pass
    try:
        password_set_popup = context.browser.find_element_by_id('modalPasswordSet')
        if password_set_popup.is_displayed():
            click_button_from_collection(context, text,
                                         password_set_popup.find_elements_by_class_name('btn-large'))
            sleep(1)
            return
    except NoSuchElementException:
        pass
    try:
        if text == 'reset_password_email_submit':
            text = 'submit'
        password_reset_email_popup = context.browser.find_element_by_id('modalPasswordRequest')
        if password_reset_email_popup.is_displayed():
            click_button_from_collection(context, text,
                                         password_reset_email_popup.find_elements_by_class_name('btn-large'))
            sleep(1)
            return
    except NoSuchElementException:
        pass
    try:
        if text == 'reset_pass_submit':
            text = 'submit'
        password_reset_email_popup = context.browser.find_element_by_id('modalPasswordReset')
        if password_reset_email_popup.is_displayed():
            click_button_from_collection(context, text,
                                         password_reset_email_popup.find_elements_by_class_name('btn-large'))
            sleep(1)
            return
    except NoSuchElementException:
        pass
    assert False, "Could not find any popups in the landing page"


@step(u'I enter my {kind} credentials for {action}')
def enter_creds(context, kind, action):
    kind = kind.lower()
    action = action.lower()
    if action not in ['login', 'signup', 'signup_password_set',
                      'password_reset_request', 'password_reset',
                      'demo request']:
        raise ValueError("Cannot input %s credentials" % action)
    if kind not in ['standard', 'alt', 'rbac_owner', 'rbac_member'] and not kind.startswith('invalid'):
        raise ValueError("No idea what %s credentials are" % kind)
    if action == 'login':
        try:
            WebDriverWait(context.browser, 4).until(
                EC.visibility_of_element_located((By.ID, "signin-email")))
        except TimeoutException:
            raise TimeoutException("Email input did not appear after 4 seconds")
        email_input = context.browser.find_element_by_id("signin-email")
        if kind == 'invalid_email':
            clear_input_and_send_keys(email_input, 'tester')
        elif kind == 'rbac_owner':
            clear_input_and_send_keys(email_input,
                                      context.mist_config['RBAC_OWNER_EMAIL'])
        elif kind == 'rbac_member':
            clear_input_and_send_keys(email_input,
                                      context.mist_config['RBAC_MEMBER_EMAIL'])
        else:
            clear_input_and_send_keys(email_input, context.mist_config['EMAIL'])
        password_input = context.browser.find_element_by_id("signin-password")
        if kind == 'alt':
            clear_input_and_send_keys(password_input,
                                      context.mist_config['PASSWORD2'])
        elif kind == 'rbac_owner':
            clear_input_and_send_keys(password_input,
                                      context.mist_config['RBAC_OWNER_PASSWORD'])
        elif kind == 'rbac_member':
            clear_input_and_send_keys(password_input,
                                      context.mist_config['RBAC_MEMBER_PASSWORD'])
        elif kind == 'invalid_no_password':
            clear_input_and_send_keys(password_input, '')
        else:
            clear_input_and_send_keys(password_input,
                                      context.mist_config['PASSWORD1'])
    elif action == 'signup':
        try:
            WebDriverWait(context.browser, 4).until(
                EC.visibility_of_element_located((By.ID, "signup-email")))
        except TimeoutException:
            raise TimeoutException("Email input did not appear after 4 seconds")
        email_input = context.browser.find_element_by_id("signup-email")
        clear_input_and_send_keys(email_input, context.mist_config['EMAIL'])
        name_input = context.browser.find_element_by_id("signup-name")
        clear_input_and_send_keys(name_input, context.mist_config['NAME'])
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
            clear_input_and_send_keys(pass_input,
                                      context.mist_config['PASSWORD2'])
            clear_input_and_send_keys(pass_confirm_input,
                                      context.mist_config['PASSWORD2'])
        else:
            clear_input_and_send_keys(pass_input,
                                      context.mist_config['PASSWORD1'])
            clear_input_and_send_keys(pass_confirm_input,
                                      context.mist_config['PASSWORD1'])
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
            clear_input_and_send_keys(first_textfield,
                                      context.mist_config['PASSWORD2'])
            clear_input_and_send_keys(second_textfield,
                                      context.mist_config['PASSWORD2'])
        else:
            clear_input_and_send_keys(first_textfield,
                                      context.mist_config['PASSWORD1'])
            clear_input_and_send_keys(second_textfield,
                                      context.mist_config['PASSWORD1'])
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


def clear_input_and_send_keys(input_field, text):
    end_time = time() + 5
    while time() < end_time:
        while input_field.get_attribute('value') != '':
            input_field.send_keys(u'\ue003')
        if text == '':
            break
        input_field.send_keys(text)
        if input_field.get_attribute('value') != text:
            assert time() + 1 > end_time, "Could not input value %s" % text
            sleep(1)
        else:
            break


@step(u'there should be a message saying "{error_message}" for error in '
      u'"{type_of_error}"')
def check_error_message(context, error_message, type_of_error):
    assert type_of_error.lower() in ['authentication', 'email', 'password'],\
        "This type of message is not available in the login page"
    if type_of_error == 'email':
        text = safe_get_element_text(context.browser.find_element_by_id('signin-email-error'))
    elif type_of_error == 'password':
        text = safe_get_element_text(context.browser.find_element_by_id('signin-password-error'))
    elif type_of_error == 'authentication':
        text = safe_get_element_text(context.browser.
                                     find_element_by_id('modalLogin').
                                     find_element_by_class_name('error-msg'))
    assert error_message.lower() in text.lower(), "Error message was not %s " \
                                                  "but instead %s" % \
                                                  (error_message, text)


@step(u'I should get an already registered error')
def already_registered(context):
    text = safe_get_element_text(context.browser.find_element_by_id('registerForm').find_elements_by_class_name('center')[0])
    if text != 'Already registered!':
        raise ValueError("Expecting an Already registered! error message and "
                         "didn't get it")


# @step(u'I wait for some reaction for max {seconds} seconds')
# def wait_for_some_answer(context, seconds):
#     timeout = time() + int(seconds)
#     while time() < timeout:
#         try:
#             context.browser.find_element_by_id("splash")
#             return
#         except NoSuchElementException:
#             pass
#         try:
#             context.browser.find_element_by_id("signin-email-error")
#             return
#         except NoSuchElementException:
#             pass
#         try:
#             context.browser.find_element_by_id("signin-password-error")
#             return
#         except NoSuchElementException:
#             pass
#         try:
#             context.browser.find_element_by_id("signup-email-error")
#             return
#         except NoSuchElementException:
#             pass
#         try:
#             context.browser.find_element_by_id("signup-password-error")
#             return
#         except NoSuchElementException:
#             pass
#         try:
#             context.browser.find_element_by_class_name("error-msg")
#             return
#         except NoSuchElementException:
#             pass
#         sleep(1)
#     assert False, "Nothing has happened in the landing screen after %s seconds"\
#                   % seconds


@step(u'I should see the landing page within {seconds} seconds')
def wait_for_landing_page(context, seconds):
    try:
        WebDriverWait(context.browser, int(seconds)).until(
            EC.element_to_be_clickable((By.ID, "top-signup-button")))
    except TimeoutException:
        raise TimeoutException("Landing page has not appeared after %s seconds"
                               % seconds)
