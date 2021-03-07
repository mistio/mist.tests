import random
import string

from time import time
from time import sleep

from behave import step

from .landing import clear_input_and_send_keys

from .search import search_for_something

from .utils import safe_get_element_text

from .buttons import search_for_button

from .navigation import click_the_gravatar

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver import ActionChains


@step('I clear the search bar')
def clear_search_bar(context):
    input_field = context.browser.find_element_by_class_name('team-search')
    while input_field.get_attribute('value') != '':
        input_field.send_keys('\ue003')


@step('I switch to the {org} organization')
def switch_organization(context, org):
    user_button = context.browser.find_element_by_id("me-btn")
    user_button.click()
    orgs_list = context.browser.find_element_by_class_name("orgs-list")
    if orgs_list.find_element_by_class_name('org-active').text == org:
        context.browser.find_element_by_id("user-menu-popup-screen").click()
        return
    else:
        link = orgs_list.find_element_by_link_text(org)
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
            placeholder = context.browser.find_element_by_id("team-members-list")
            members = placeholder.find_elements_by_tag_name("tr")
            for member in members:
                sections = member.find_elements_by_tag_name("td")
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
        placeholder = context.browser.find_element_by_id("team-list-page")
        teams = placeholder.find_elements_by_tag_name("li")

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
    user_menu = context.browser.find_element_by_id('user-menu-popup')
    personal = search_for_button(context, 'personal',
                                 user_menu.find_elements_by_class_name('ui-btn'))
    ActionChains(context.browser).move_to_element(personal).click().perform()


@step('I should get an Organization Name Exists error')
def already_exists(context):
    time.sleep(1)
    text = safe_get_element_text(context.browser.find_element_by_id('notification-popup'))
    if text != 'Organization name exists':
        raise ValueError("Expecting an 'Organization name exists' error "
                         "message, but didn't get it.")


@step('I expect to see no pending member invitations')
def no_pending(context):
    try:
        context.browser.find_element_by_class_name('label-pending')
        raise Exception("Pending status captured. Can't have that!")
    except NoSuchElementException:
        pass
