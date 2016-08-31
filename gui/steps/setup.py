from behave import step

from tests.helpers.setup import setup_user_if_not_exists
from tests.helpers.setup import remove_user_if_exists

from selenium.common.exceptions import NoSuchElementException


@step(u'I setup user with email "{user_email}"')
def setup_user(context, user_email):
    if context.mist_config.get(user_email):
        user_email = context.mist_config.get(user_email)
    setup_user_if_not_exists(user_email)


@step(u'I make sure user with email "{user_email}" is absent')
def remove_user(context, user_email):
    if context.mist_config.get(user_email):
        user_email = context.mist_config.get(user_email)
    remove_user_if_exists(user_email)


@step(u'user with email "{user_email}" is registered')
def register_user(context, user_email):
    if context.mist_config.get(user_email):
        user_email = context.mist_config.get(user_email)

    try:
        # this means that we are currently logged in
        context.browser.find_element_by_id("user-menu-popup")
        return
    except NoSuchElementException:
        pass

    try:
        context.execute_steps(u"When I visit mist.core")
        context.browser.find_element_by_id("top-signup-button")
        context.execute_steps(u'''
            When I visit mist.core
            Given I am not logged in to mist.core
            And I open the login popup
            Then I click the email button in the landing page popup
            And I enter my standard credentials for login
            Then I click the sign in button in the landing page popup
            And I wait for 3 seconds
        ''')
        context.browser.find_element_by_id("splash")
        context.execute_steps(u'Then I wait for the mist.io splash page to load')
        # if we reach this line successfully it means that the user is already
        # registered
        return
    except NoSuchElementException:
        remove_user(context, user_email)
        context.execute_steps(u'''
            Then I refresh the page
            When I open the signup popup
            Then I click the sign up button in the landing page popup
            Then I click the email button in the landing page popup
            And I enter my standard credentials for signup
            And I click the sign up button in the landing page popup
            Then I should receive an email at the address "EMAIL" with subject "[mist.io] Confirm your registration" within 10 seconds
            And I follow the link contained in the email sent at the address "EMAIL" with subject "[mist.io] Confirm your registration"
            Then I enter my standard credentials for signup_password_set
            And I click the submit button in the landing page popup
            And I wait for the mist.io splash page to load
        ''')
