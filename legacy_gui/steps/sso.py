from behave import step
from behave import given

from tests import config

from selenium.common.exceptions import TimeoutException

from navigation import i_am_in_homepage

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@step(u'I input my "{email}" in the field with id "{element_id}"')
def give_input_to_a_field(context, email, element_id):
    email = context.mist_config.get(email, None)
    if not email:
        raise ValueError("No such email has been configured(%s)", email)
    try:
        WebDriverWait(context.browser, 10).until(
            EC.visibility_of_element_located((By.ID, element_id)))
    except TimeoutException:
        raise TimeoutException("Element with id %s did not appear "
                               "after 10 seconds" % element_id)
    field = context.browser.find_element_by_id(element_id)
    if not field:
        raise ValueError("Field with id %s has not been found", element_id)
    field.send_keys(email)


@step(u'I press the button with id "{button_id}"')
def press_button_with_id(context, button_id):
    """
    This is a function for the Google login form
    """
    button = context.browser.find_element_by_id(button_id)
    if not button:
        raise ValueError("Could not find any button with id %s", button_id)
    button.click()


@step(u'I click the Sign In button in the Github form')
def press_button_with_id(context):
    """
    This is a very specific method only for the Github sign in form
    """
    try:
        button = context.browser.find_element_by_css_selector('input.btn[type=submit]')
        button.click()
    except:
        raise ValueError("Could not find Sign In button in github form")


@step(u'I do the Google login')
def do_google_login(context):
    """
    this function will check whether or not the test has been forwarded to the
    google authentication page or to the mist plash page and act
    accordingly
    """
    if not i_am_in_homepage(context):
        try:
            context.browser.find_element_by_id("Passwd")
            context.execute_steps(u'''
                Then I input my "GOOGLE_TEST_EMAIL" in the field with id "Email"
                Then I input my "GOOGLE_TEST_PASSWORD" in the field with id "Passwd"
                And I press the button with id "signIn"
            ''')
        except:
            context.execute_steps(u'''
                Then I input my "GOOGLE_TEST_EMAIL" in the field with id "Email"
                And I press the button with id "next"
                Then I input my "GOOGLE_TEST_PASSWORD" in the field with id "Passwd"
                And I press the button with id "signIn"
            ''')

        context.execute_steps(u'When I wait for 5 seconds')

        try:
            context.browser.find_element_by_id("submit_approve_access")
            context.execute_steps(u'''
                Then I press the button with id "submit_approve_access"
                And I wait for 5 seconds
            ''')
        except:
            pass
        context.execute_steps(u'''
            Then I wait for the mist.io splash page to load
        ''')


@step(u'I do the Github login')
def do_github_login(context):
    """
    this function will check whether or not the test has been forwarded to the
    github authentication page or to the mist plash page and act
    accordingly
    """
    if not i_am_in_homepage(context):
        context.execute_steps(u'''
            Then I input my "GITHUB_TEST_EMAIL" in the field with id "login_field"
            Then I input my "GITHUB_TEST_PASSWORD" in the field with id "password"
            And I click the Sign In button in the Github form
            And I wait for 5 seconds
            Then I wait for the mist.io splash page to load
        ''')
    else:
        context.execute_steps(u'''
            Then I wait for 5 seconds
            And I wait for the mist.io splash page to load
        ''')


@given(u'special {service} account for registration testing')
def override_sso_creds(context, service):
    if service == 'Google':
        context.mist_config['GOOGLE_TEST_EMAIL'] = \
            config.GOOGLE_REGISTRATION_TEST_EMAIL
        context.mist_config['GOOGLE_TEST_PASSWORD'] = \
            config.GOOGLE_REGISTRATION_TEST_PASSWORD
    elif service == 'Github':
        context.mist_config['GITHUB_TEST_EMAIL'] = \
            config.GITHUB_REGISTRATION_TEST_EMAIL
        context.mist_config['GITHUB_TEST_PASSWORD'] = \
            config.GITHUB_REGISTRATION_TEST_PASSWORD
    else:
        raise ValueError("Unknown authentication provider")
