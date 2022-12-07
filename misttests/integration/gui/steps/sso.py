from behave import step

from misttests import config

from selenium.common.exceptions import TimeoutException

from misttests.integration.gui.steps.navigation import i_am_in_homepage

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@step('I type the username in the Google form')
def type_username_gmail(context):
    """
    This is a very specific method only for the Google sign in form
    """
    email = context.mist_config.get('GOOGLE_TEST_EMAIL', None)
    try:
        email_input = context.browser.find_element(By.CSS_SELECTOR, 'input[type=email]')
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)
    except:
        raise ValueError("Could not type username in google form")


@step('I type the password in the Google form')
def type_password_gmail(context):
    """
    This is a very specific method only for the Google sign in form
    """
    password = context.mist_config.get('GOOGLE_TEST_PASSWORD', None)
    try:
        password_input = context.browser.find_element(By.CSS_SELECTOR, 'input[type=password]')
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
    except:
        raise ValueError("Could not type password in google form")


@step('I click the Sign In button in the Github form')
def press_button_with_id(context):
    """
    This is a very specific method only for the Github sign in form
    """
    try:
        button = context.browser.find_element(By.CSS_SELECTOR, 'input.btn[type=submit]')
        button.click()
    except:
        raise ValueError("Could not find Sign In button in github form")
