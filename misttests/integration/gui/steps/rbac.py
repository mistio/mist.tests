import random
import string

from time import time
from time import sleep

from behave import step

from selenium.webdriver.common.by import By

from misttests.integration.gui.steps.utils import clear_input_and_send_keys

from misttests.integration.gui.steps.search import search_for_something

from misttests.integration.gui.steps.utils import safe_get_element_text

from misttests.integration.gui.steps.buttons import search_for_button

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver import ActionChains


@step('I switch to the {org} organization')
def switch_organization(context, org):
    user_button = context.browser.find_element(By.CSS_SELECTOR, "#me-btn")
    user_button.click()
    orgs_list = context.browser.find_element(By.CSS_SELECTOR, ".orgs-list")
    if orgs_list.find_element(By.CSS_SELECTOR, '.org-active').text == org:
        context.browser.find_element(By.CSS_SELECTOR, "#user-menu-popup-screen").click()
        return
    else:
        link = orgs_list.find_element(By.LINK_TEXT, org)
        link.click()


@step('I expect the {user} to appear on the team members within max {seconds}' 'seconds')
def user_in_team_members(context, user, seconds):
    if user == 'rbac_member1':
        email = context.mist_config.get('RBAC_MEMBER_EMAIL')
    elif user == 'reg_member1':
        email = context.mist_config.get('EMAIL')
    try:
        end_time = time() + int(seconds)
        while time() < end_time:
            placeholder = context.browser.find_element(By.CSS_SELECTOR, "#team-members-list")
            members = placeholder.find_elements(By.CSS_SELECTOR, "tr")
            for member in members:
                sections = member.find_elements(By.CSS_SELECTOR, "td")
                for section in sections:
                    if section.text == email:
                        return
            sleep(2)
    except NoSuchElementException:
        return None
    except StaleElementReferenceException:
        return None


def get_team(context, name):
    try:
        placeholder = context.browser.find_element(By.CSS_SELECTOR, "#team-list-page")
        teams = placeholder.find_elements(By.CSS_SELECTOR, "li")

        for team in teams:
            team_text = safe_get_element_text(team)
            if name in team_text:
                return team

        return None
    except NoSuchElementException:
        return None
    except StaleElementReferenceException:
        return None


@step('I switch to personal context')
def switch_personal(context):
    click_the_gravatar(context)
    context.execute_steps('''
        Then I wait for 2 seconds
    ''')
    user_menu = context.browser.find_element(By.CSS_SELECTOR, '#user-menu-popup')
    personal = search_for_button(context, 'personal',
                                 user_menu.find_elements(By.CSS_SELECTOR, '.ui-btn'))
    ActionChains(context.browser).move_to_element(personal).click().perform()


@step('I should get an Organization Name Exists error')
def already_exists(context):
    time.sleep(1)
    text = safe_get_element_text(context.browser.find_element(By.CSS_SELECTOR, '#notification-popup'))
    if text != 'Organization name exists':
        raise ValueError("Expecting an 'Organization name exists' error "
                         "message, but didn't get it.")


@step('I expect to see no pending member invitations')
def no_pending(context):
    try:
        context.browser.find_element(By.CSS_SELECTOR, '.label-pending')
        raise Exception("Pending status captured. Can't have that!")
    except NoSuchElementException:
        pass
