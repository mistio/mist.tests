import random
import string

from time import time
from time import sleep
from behave import step

from landing import clear_input_and_send_keys
from search import search_for_something
from utils import safe_get_element_text
from buttons import search_for_button
from navigation import click_the_gravatar

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver import ActionChains


@step(u'I give a random team name for {action} team')
def give_random_team_name(context, action):
    random_team_name = ''.join([random.choice(string.ascii_letters +
                                                string.digits) for _ in
                                  range(6)])
    if action == 'new':
        team_input = context.browser.find_element_by_id("team-name")
    elif action == 'edit':
        team_input = context.browser.find_element_by_id("team-edit-new-name")
    else:
        raise ValueError("Action can be either new or edit.")
    context.mist_config['random_team_name'] = random_team_name
    clear_input_and_send_keys(team_input, random_team_name)


@step(u'I search for the random team name i gave before')
def search_team(context):
    if context.mist_config.get('random_team_name'):
        text = context.mist_config.get('random_team_name')
    input_field = context.browser.find_element_by_class_name('team-search')
    while input_field.get_attribute('value') != '':
        input_field.send_keys(u'\ue003')
    search_for_something(context, text, 'team')


@step(u'I should see the team added within {seconds}' u'seconds')
def team_added(context, seconds):
    if context.mist_config.get('random_team_name'):
        name = context.mist_config.get('random_team_name')

    end_time = time() + int(seconds)
    while time() < end_time:
        team = get_team(context, name)
        if team:
            return
        sleep(2)

    assert False, u'%s is not added' % name


@step(u'I should see the team name changed within {seconds}' u'seconds')
def team_name_changed(context, seconds):
    if context.mist_config.get('random_team_name'):
        name = context.mist_config.get('random_team_name')

    end_time = time() + int(seconds)
    while time() < end_time:
        title = context.browser.find_element_by_class_name('ui-title').text
        if name == title:
            return
        sleep(2)

    assert False, u'%s is not added' % name


@step(u'I clear the search bar')
def clear_search_bar(context):
    input_field = context.browser.find_element_by_class_name('team-search')
    while input_field.get_attribute('value') != '':
        input_field.send_keys(u'\ue003')


@step(u'the random team should be deleted')
def random_team_deleted(context):
    if context.mist_config.get('random_team_name'):
        name = context.mist_config.get('random_team_name')

    teams = context.browser.find_elements_by_css_selector(".ui-listview li")
    for team in teams:
        if name in safe_get_element_text(team):
            assert False, u'%s Team is not deleted'


@step(u'I choose the randomly created team')
def choose_randomly_created_team(context):
    if context.mist_config.get('random_team_name'):
        name = context.mist_config.get('random_team_name')   

    end_time = time() + 20
    while time() < end_time:
        team = get_team(context, name)
        if team:
            checkbox = team.find_element_by_class_name("ui-checkbox")
            checkbox.click()
            return

        sleep(2)
    assert False, u'Could not choose/tick %s team' % name


@step(u'I choose the random team')
def choose_random_team(context):
    if context.mist_config.get('random_team_name'):
        name = context.mist_config.get('random_team_name')   

    end_time = time() + 20
    while time() < end_time:
        team = get_team(context, name)
        if team:
            link = team.find_element_by_class_name("team-name")
            link.click()
            return

        sleep(2)
    assert False, u'Could not click %s team' % name


@step(u'I give the {user} email')
def give_user_email(context, user):
    if user == 'rbac_member1':
        email = context.mist_config.get('RBAC_MEMBER_EMAIL')
    if user == 'reg_member1':
        email = context.mist_config.get('EMAIL')
    member_input = context.browser.find_element_by_id("member-email")
    clear_input_and_send_keys(member_input, email)


@step(u'I switch to the {org} organization')
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


@step(u'I expect the {user} to appear on the team members within max {seconds}' u'seconds')
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


@step(u'I expect for the {user} to be deleted after {seconds}' u'seconds')
def deleted_from_team(context, user, seconds):
    if user == 'rbac_member1':
        email = context.mist_config.get('RBAC_MEMBER_EMAIL')
    try:
        sleep(float(seconds))
        placeholder = context.browser.find_element_by_id("team-members-list")
        members = placeholder.find_elements_by_tag_name("tr")
        for member in members:
            sections = member.find_elements_by_tag_name("td")
            for section in sections:
                if section.text == email:
                    assert False, u'User %s was not deleted' % user
    except NoSuchElementException:
        return None
    except StaleElementReferenceException:
        return None


@step(u'I click the button to delete the {user}')
def user_in_team_members(context, user):
    if user == 'rbac_member1':
        email = context.mist_config.get('RBAC_MEMBER_EMAIL')

    try:
        placeholder = context.browser.find_element_by_id("team-members-list")
        members = placeholder.find_elements_by_tag_name("tr")
        for member in members:
            sections = member.find_elements_by_tag_name("td")
            for section in sections:
                if section.text == email:
                    link = section.find_elements_by_xpath("..")[0].find_elements_by_class_name("icon-xx")[0]
                    link.click()
                    return
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


@step(u'I switch to personal context')
def switch_personal(context):
    click_the_gravatar(context)
    context.execute_steps(u'''
        Then I wait for 2 seconds
    ''')
    user_menu = context.browser.find_element_by_id('user-menu-popup')
    personal = search_for_button(context, 'personal',
                                 user_menu.find_elements_by_class_name('ui-btn'))
    ActionChains(context.browser).move_to_element(personal).click().perform()


@step(u'I give the organization name')
def give_org_name(context):
    org_name = context.mist_config.get('ORG_NAME')
    org_field = context.browser.find_element_by_id("organization-name")
    clear_input_and_send_keys(org_field, org_name)


@step(u'I should get an Organization Name Exists error')
def already_exists(context):
    time.sleep(1)
    text = safe_get_element_text(context.browser.find_element_by_id('notification-popup'))
    if text != 'Organization name exists':
        raise ValueError("Expecting an 'Organization name exists' error "
                         "message, but didn't get it.")


@step(u'I expect to see no pending member invitations')
def no_pending(context):
    try:
        pending = context.browser.find_element_by_class_name('label-pending')
        raise Exception("Pending status captured. Can't have that!")
    except NoSuchElementException:
        pass
